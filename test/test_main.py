import pytest
from unittest.mock import call

from sqlalchemy import text

from main import (migrate_mgts_to_twse, consolidate_mgts_tables,
                  MGTS_MIGRATION_MAP,
                  migrate_faoi_to_twse, consolidate_faoi_tables,
                  FAOI_MIGRATION_MAP)


class TestMigrateMgtsToTwse:
    """測試 MGTS 資料遷移至 TWSE 的函式。"""

    def _mock_execute(self, mocker, responses):
        """建立依序回傳指定結果的 mock connection。

        Args:
            mocker: pytest-mock 的 mocker 物件。
            responses: 每次 execute 呼叫的回傳值列表。

        Returns:
            mock_conn: 設定好的 mock connection 物件。
        """
        mock_conn = mocker.Mock()
        mock_results = []
        for resp in responses:
            mock_result = mocker.Mock()
            if isinstance(resp, tuple) and resp[0] == 'fetchone':
                mock_result.fetchone.return_value = resp[1]
            elif isinstance(resp, tuple) and resp[0] == 'scalar':
                mock_result.scalar.return_value = resp[1]
            mock_results.append(mock_result)
        mock_conn.execute.side_effect = mock_results
        return mock_conn

    def test_skip_when_mgts_not_exists(self, mocker):
        """舊 MGTS 資料庫不存在時，應跳過遷移且不執行任何 INSERT/DROP。"""
        mock_conn = mocker.Mock()
        mock_result = mocker.Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        migrate_mgts_to_twse(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_migrate_data(self, mocker):
        """舊 MGTS 資料庫存在且有資料時，應執行 INSERT 並 DROP。"""
        # execute 呼叫順序：
        # 1. SCHEMA check
        # 每張表依序：source count → (INSERT IGNORE 或 target count → INSERT)
        # 最後 DROP DATABASE
        responses = [
            ('fetchone', ('MGTS',)),
        ]
        for old_table, new_table in MGTS_MIGRATION_MAP.items():
            responses.append(('scalar', 10))    # source count = 10
            if old_table == new_table:
                responses.append(('scalar', None))  # INSERT IGNORE
            else:
                responses.append(('scalar', 0))     # target count = 0
                responses.append(('scalar', None))   # INSERT
        responses.append(('scalar', None))      # DROP DATABASE

        mock_conn = self._mock_execute(mocker, responses)

        migrate_mgts_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 驗證有 INSERT INTO 語句（含 INSERT IGNORE）
        insert_sqls = [s for s in executed_sqls if 'INSERT' in s]
        assert len(insert_sqls) == len(MGTS_MIGRATION_MAP)

        for old_table, new_table in MGTS_MIGRATION_MAP.items():
            if old_table == new_table:
                assert any(
                    'INSERT IGNORE' in s and f'`TWSE`.`{new_table}`' in s
                    and f'`MGTS`.`{old_table}`' in s
                    for s in insert_sqls
                )
            else:
                assert any(
                    f'`TWSE`.`{new_table}`' in s and f'`MGTS`.`{old_table}`' in s
                    for s in insert_sqls
                )

        # 驗證有 DROP DATABASE
        assert any('DROP DATABASE' in s for s in executed_sqls)

    def test_skip_table_when_target_has_data(self, mocker):
        """目標表已有資料時，應跳過該表的遷移（INSERT IGNORE 表仍會執行）。"""
        responses = [
            ('fetchone', ('MGTS',)),   # MGTS 存在
        ]
        for old_table, new_table in MGTS_MIGRATION_MAP.items():
            responses.append(('scalar', 10))   # source count = 10
            if old_table == new_table:
                responses.append(('scalar', None))  # INSERT IGNORE 仍執行
            else:
                responses.append(('scalar', 5))     # target count = 5（已有資料）
        # DROP
        responses.append(('scalar', None))

        mock_conn = self._mock_execute(mocker, responses)

        migrate_mgts_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 一般 INSERT 不應存在（被 target count > 0 跳過）
        normal_inserts = [
            s for s in executed_sqls
            if 'INSERT INTO' in s and 'INSERT IGNORE' not in s
        ]
        assert len(normal_inserts) == 0

        # INSERT IGNORE 仍會執行（Translate）
        ignore_inserts = [s for s in executed_sqls if 'INSERT IGNORE' in s]
        assert len(ignore_inserts) == 1

    def test_skip_table_when_source_empty(self, mocker):
        """來源表無資料時，應跳過該表的遷移。"""
        responses = [
            ('fetchone', ('MGTS',)),   # MGTS 存在
        ]
        for _ in MGTS_MIGRATION_MAP:
            responses.append(('scalar', 0))    # source count = 0
        # DROP
        responses.append(('scalar', None))

        mock_conn = self._mock_execute(mocker, responses)

        migrate_mgts_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 不應有任何 INSERT
        insert_sqls = [s for s in executed_sqls if 'INSERT' in s]
        assert len(insert_sqls) == 0

    def test_migration_map_has_three_entries(self):
        """MGTS_MIGRATION_MAP 應有 3 個項目。"""
        assert len(MGTS_MIGRATION_MAP) == 3
        assert "DailyPrice" in MGTS_MIGRATION_MAP
        assert "Translate" in MGTS_MIGRATION_MAP
        assert "UploadDate" in MGTS_MIGRATION_MAP
        assert "StockName" not in MGTS_MIGRATION_MAP

    def test_translate_maps_to_same_name(self):
        """Translate 應映射至自己（使用 INSERT IGNORE 合併）。"""
        assert MGTS_MIGRATION_MAP["Translate"] == "Translate"


class TestConsolidateMgtsTables:
    """測試合併 MGTS 冗餘資料表的函式。"""

    def _mock_execute(self, mocker, responses):
        """建立依序回傳指定結果的 mock connection。

        Args:
            mocker: pytest-mock 的 mocker 物件。
            responses: 每次 execute 呼叫的回傳值列表。

        Returns:
            mock_conn: 設定好的 mock connection 物件。
        """
        mock_conn = mocker.Mock()
        mock_results = []
        for resp in responses:
            mock_result = mocker.Mock()
            if isinstance(resp, tuple) and resp[0] == 'fetchone':
                mock_result.fetchone.return_value = resp[1]
            elif isinstance(resp, tuple) and resp[0] == 'scalar':
                mock_result.scalar.return_value = resp[1]
            mock_results.append(mock_result)
        mock_conn.execute.side_effect = mock_results
        return mock_conn

    def test_skip_when_twse_not_exists(self, mocker):
        """TWSE 資料庫不存在時，應跳過合併。"""
        mock_conn = mocker.Mock()
        mock_result = mocker.Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        consolidate_mgts_tables(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_widen_english_column(self, mocker):
        """English 欄位長度不足 45 時，應執行 ALTER TABLE。"""
        responses = [
            ('fetchone', ('TWSE',)),       # TWSE 存在
            ('fetchone', (20,)),           # English 長度為 20
            ('scalar', None),              # ALTER TABLE
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # INSERT IGNORE
            ('fetchone', ('MGTSStockName',)),  # MGTSStockName 存在
            ('scalar', None),              # DROP MGTSStockName
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # DROP MGTSTranslate
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_mgts_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]
        assert any('ALTER TABLE' in s and 'VARCHAR(45)' in s for s in executed_sqls)

    def test_skip_alter_when_already_wide(self, mocker):
        """English 欄位已為 45 時，不應執行 ALTER TABLE。"""
        responses = [
            ('fetchone', ('TWSE',)),       # TWSE 存在
            ('fetchone', (45,)),           # English 長度已為 45
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # INSERT IGNORE
            ('fetchone', ('MGTSStockName',)),  # MGTSStockName 存在
            ('scalar', None),              # DROP MGTSStockName
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # DROP MGTSTranslate
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_mgts_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]
        assert not any('ALTER TABLE' in s for s in executed_sqls)

    def test_merge_and_drop_tables(self, mocker):
        """MGTSTranslate 存在時，應合併資料並刪除 MGTSStockName、MGTSTranslate。"""
        responses = [
            ('fetchone', ('TWSE',)),       # TWSE 存在
            ('fetchone', (45,)),           # English 已夠寬
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # INSERT IGNORE
            ('fetchone', ('MGTSStockName',)),  # MGTSStockName 存在
            ('scalar', None),              # DROP MGTSStockName
            ('fetchone', ('MGTSTranslate',)),  # MGTSTranslate 存在
            ('scalar', None),              # DROP MGTSTranslate
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_mgts_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 驗證 INSERT IGNORE 合併
        assert any('INSERT IGNORE' in s and 'MGTSTranslate' in s for s in executed_sqls)

        # 驗證 DROP TABLE
        assert any('DROP TABLE' in s and 'MGTSStockName' in s for s in executed_sqls)
        assert any('DROP TABLE' in s and 'MGTSTranslate' in s for s in executed_sqls)

    def test_skip_drop_when_tables_not_exist(self, mocker):
        """MGTSStockName 和 MGTSTranslate 不存在時，不應執行 DROP。"""
        responses = [
            ('fetchone', ('TWSE',)),       # TWSE 存在
            ('fetchone', (45,)),           # English 已夠寬
            ('fetchone', None),            # MGTSTranslate 不存在
            ('fetchone', None),            # MGTSStockName 不存在（迴圈第一項）
            ('fetchone', None),            # MGTSTranslate 不存在（迴圈第二項）
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_mgts_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]
        assert not any('DROP TABLE' in s for s in executed_sqls)
        assert not any('INSERT IGNORE' in s for s in executed_sqls)


class TestMigrateFaoiToTwse:
    """測試 FAOI 資料遷移至 TWSE 的函式。"""

    def _mock_execute(self, mocker, responses):
        """建立依序回傳指定結果的 mock connection。

        Args:
            mocker: pytest-mock 的 mocker 物件。
            responses: 每次 execute 呼叫的回傳值列表。

        Returns:
            mock_conn: 設定好的 mock connection 物件。
        """
        mock_conn = mocker.Mock()
        mock_results = []
        for resp in responses:
            mock_result = mocker.Mock()
            if isinstance(resp, tuple) and resp[0] == 'fetchone':
                mock_result.fetchone.return_value = resp[1]
            elif isinstance(resp, tuple) and resp[0] == 'scalar':
                mock_result.scalar.return_value = resp[1]
            mock_results.append(mock_result)
        mock_conn.execute.side_effect = mock_results
        return mock_conn

    def test_skip_when_faoi_not_exists(self, mocker):
        """舊 FAOI 資料庫不存在時，應跳過遷移且不執行任何 INSERT/DROP。"""
        mock_conn = mocker.Mock()
        mock_result = mocker.Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        migrate_faoi_to_twse(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_migrate_data(self, mocker):
        """舊 FAOI 資料庫存在且有資料時，應執行 INSERT 並 DROP。"""
        responses = [
            ('fetchone', ('FAOI',)),
        ]
        for old_table, new_table in FAOI_MIGRATION_MAP.items():
            responses.append(('scalar', 10))    # source count = 10
            if old_table == new_table:
                responses.append(('scalar', None))  # INSERT IGNORE
            else:
                responses.append(('scalar', 0))     # target count = 0
                responses.append(('scalar', None))   # INSERT
        responses.append(('scalar', None))      # DROP DATABASE

        mock_conn = self._mock_execute(mocker, responses)

        migrate_faoi_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        insert_sqls = [s for s in executed_sqls if 'INSERT' in s]
        assert len(insert_sqls) == len(FAOI_MIGRATION_MAP)

        for old_table, new_table in FAOI_MIGRATION_MAP.items():
            if old_table == new_table:
                assert any(
                    'INSERT IGNORE' in s and f'`TWSE`.`{new_table}`' in s
                    and f'`FAOI`.`{old_table}`' in s
                    for s in insert_sqls
                )
            else:
                assert any(
                    f'`TWSE`.`{new_table}`' in s and f'`FAOI`.`{old_table}`' in s
                    for s in insert_sqls
                )

        assert any('DROP DATABASE' in s for s in executed_sqls)

    def test_skip_table_when_target_has_data(self, mocker):
        """目標表已有資料時，應跳過該表的遷移（INSERT IGNORE 表仍會執行）。"""
        responses = [
            ('fetchone', ('FAOI',)),
        ]
        for old_table, new_table in FAOI_MIGRATION_MAP.items():
            responses.append(('scalar', 10))   # source count = 10
            if old_table == new_table:
                responses.append(('scalar', None))  # INSERT IGNORE 仍執行
            else:
                responses.append(('scalar', 5))     # target count = 5（已有資料）
        responses.append(('scalar', None))

        mock_conn = self._mock_execute(mocker, responses)

        migrate_faoi_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        normal_inserts = [
            s for s in executed_sqls
            if 'INSERT INTO' in s and 'INSERT IGNORE' not in s
        ]
        assert len(normal_inserts) == 0

        ignore_inserts = [s for s in executed_sqls if 'INSERT IGNORE' in s]
        assert len(ignore_inserts) == 1

    def test_skip_table_when_source_empty(self, mocker):
        """來源表無資料時，應跳過該表的遷移。"""
        responses = [
            ('fetchone', ('FAOI',)),
        ]
        for _ in FAOI_MIGRATION_MAP:
            responses.append(('scalar', 0))    # source count = 0
        responses.append(('scalar', None))

        mock_conn = self._mock_execute(mocker, responses)

        migrate_faoi_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        insert_sqls = [s for s in executed_sqls if 'INSERT' in s]
        assert len(insert_sqls) == 0

    def test_migration_map_has_three_entries(self):
        """FAOI_MIGRATION_MAP 應有 3 個項目。"""
        assert len(FAOI_MIGRATION_MAP) == 3
        assert "DailyPrice" in FAOI_MIGRATION_MAP
        assert "Translate" in FAOI_MIGRATION_MAP
        assert "UploadDate" in FAOI_MIGRATION_MAP
        assert "StockName" not in FAOI_MIGRATION_MAP

    def test_translate_maps_to_same_name(self):
        """Translate 應映射至自己（使用 INSERT IGNORE 合併）。"""
        assert FAOI_MIGRATION_MAP["Translate"] == "Translate"


class TestConsolidateFaoiTables:
    """測試合併 FAOI 冗餘資料表的函式。"""

    def _mock_execute(self, mocker, responses):
        """建立依序回傳指定結果的 mock connection。

        Args:
            mocker: pytest-mock 的 mocker 物件。
            responses: 每次 execute 呼叫的回傳值列表。

        Returns:
            mock_conn: 設定好的 mock connection 物件。
        """
        mock_conn = mocker.Mock()
        mock_results = []
        for resp in responses:
            mock_result = mocker.Mock()
            if isinstance(resp, tuple) and resp[0] == 'fetchone':
                mock_result.fetchone.return_value = resp[1]
            elif isinstance(resp, tuple) and resp[0] == 'scalar':
                mock_result.scalar.return_value = resp[1]
            mock_results.append(mock_result)
        mock_conn.execute.side_effect = mock_results
        return mock_conn

    def test_skip_when_twse_not_exists(self, mocker):
        """TWSE 資料庫不存在時，應跳過合併。"""
        mock_conn = mocker.Mock()
        mock_result = mocker.Mock()
        mock_result.fetchone.return_value = None
        mock_conn.execute.return_value = mock_result

        consolidate_faoi_tables(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_merge_and_drop_tables(self, mocker):
        """FAOITranslate 存在時，應合併資料並刪除 FAOIStockName、FAOITranslate。"""
        responses = [
            ('fetchone', ('TWSE',)),           # TWSE 存在
            ('fetchone', ('FAOITranslate',)),  # FAOITranslate 存在
            ('scalar', None),                  # INSERT IGNORE
            ('fetchone', ('FAOIStockName',)),  # FAOIStockName 存在
            ('scalar', None),                  # DROP FAOIStockName
            ('fetchone', ('FAOITranslate',)),  # FAOITranslate 存在
            ('scalar', None),                  # DROP FAOITranslate
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_faoi_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        assert any('INSERT IGNORE' in s and 'FAOITranslate' in s for s in executed_sqls)
        assert any('DROP TABLE' in s and 'FAOIStockName' in s for s in executed_sqls)
        assert any('DROP TABLE' in s and 'FAOITranslate' in s for s in executed_sqls)

    def test_skip_drop_when_tables_not_exist(self, mocker):
        """FAOIStockName 和 FAOITranslate 不存在時，不應執行 DROP。"""
        responses = [
            ('fetchone', ('TWSE',)),   # TWSE 存在
            ('fetchone', None),        # FAOITranslate 不存在
            ('fetchone', None),        # FAOIStockName 不存在（迴圈第一項）
            ('fetchone', None),        # FAOITranslate 不存在（迴圈第二項）
        ]
        mock_conn = self._mock_execute(mocker, responses)

        consolidate_faoi_tables(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]
        assert not any('DROP TABLE' in s for s in executed_sqls)
        assert not any('INSERT IGNORE' in s for s in executed_sqls)
