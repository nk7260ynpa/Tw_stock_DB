import pytest
from unittest.mock import call

from sqlalchemy import text

from main import migrate_mgts_to_twse, MGTS_MIGRATION_MAP


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
        # execute 呼叫順序（交錯式）：
        # 1. SCHEMA check
        # 每張表依序：source count → target count → INSERT
        # 最後 DROP DATABASE
        responses = [
            ('fetchone', ('MGTS',)),
        ]
        for _ in MGTS_MIGRATION_MAP:
            responses.append(('scalar', 10))    # source count = 10
            responses.append(('scalar', 0))     # target count = 0
            responses.append(('scalar', None))  # INSERT
        responses.append(('scalar', None))      # DROP DATABASE

        mock_conn = self._mock_execute(mocker, responses)

        migrate_mgts_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 驗證有 INSERT INTO 語句
        insert_sqls = [s for s in executed_sqls if 'INSERT INTO' in s]
        assert len(insert_sqls) == len(MGTS_MIGRATION_MAP)

        for old_table, new_table in MGTS_MIGRATION_MAP.items():
            assert any(
                f'`TWSE`.`{new_table}`' in s and f'`MGTS`.`{old_table}`' in s
                for s in insert_sqls
            )

        # 驗證有 DROP DATABASE
        assert any('DROP DATABASE' in s for s in executed_sqls)

    def test_skip_table_when_target_has_data(self, mocker):
        """目標表已有資料時，應跳過該表的遷移。"""
        responses = [
            ('fetchone', ('MGTS',)),   # MGTS 存在
        ]
        for _ in MGTS_MIGRATION_MAP:
            responses.append(('scalar', 10))   # source count = 10
            responses.append(('scalar', 5))    # target count = 5（已有資料）
        # DROP
        responses.append(('scalar', None))

        mock_conn = self._mock_execute(mocker, responses)

        migrate_mgts_to_twse(mock_conn)

        executed_sqls = [
            str(c.args[0].text) for c in mock_conn.execute.call_args_list
        ]

        # 不應有任何 INSERT
        insert_sqls = [s for s in executed_sqls if 'INSERT INTO' in s]
        assert len(insert_sqls) == 0

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
        insert_sqls = [s for s in executed_sqls if 'INSERT INTO' in s]
        assert len(insert_sqls) == 0
