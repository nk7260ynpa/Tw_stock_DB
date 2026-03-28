import os

import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.info import (BuildINFO, BuildINFOTABLE,
                            BuildINFOTABLEKnowledge,
                            BuildINFOTABLETradingCalendar)


class TestBuildINFO:
    """測試 BuildINFO 資料庫建構類別。"""

    def test_name(self):
        """BuildINFO 的名稱應為 'INFO'。"""
        build_info = BuildINFO()
        assert build_info.name == "INFO"

    def test_typeclass(self):
        """BuildINFO 的 typeclass 應為 BuildINFOTABLE。"""
        build_info = BuildINFO()
        assert build_info.typeclass is BuildINFOTABLE

    def test_build_db(self, mocker):
        """應正確呼叫 BuildEmptyDB 建立 INFO 資料庫。"""
        build_info = BuildINFO()
        mock_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)

        build_info.build_db(mock_conn_server)

        mock_build_empty_db.build.assert_called_once_with(mock_conn_server)

    def test_build_table_discovers_subclasses(self, mocker):
        """build_table 應自動發現並建構 BuildINFOTABLE 的子類別。"""
        build_info = BuildINFO()
        mock_conn = mocker.Mock()

        subclasses = BuildINFOTABLE.__subclasses__()
        assert len(subclasses) >= 2
        assert BuildINFOTABLEKnowledge in subclasses
        assert BuildINFOTABLETradingCalendar in subclasses

        # mock 每個子類別的 build 方法
        for subclass in subclasses:
            mocker.patch.object(subclass, 'build', return_value=None)

        build_info.build_table(mock_conn)

        for subclass in subclasses:
            subclass.build.assert_called_once()


class TestBuildINFOTABLE:
    """測試 BuildINFOTABLE 資料表基類。"""

    def test_is_subclass_of_base(self):
        """BuildINFOTABLE 應繼承自 BaseBuildTABLE。"""
        assert issubclass(BuildINFOTABLE, BaseBuildTABLE)


class TestBuildINFOTABLEKnowledge:
    """測試 BuildINFOTABLEKnowledge 資料表建構類別。"""

    def test_table_name(self):
        """Knowledge 資料表名稱應為 'Knowledge'。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        assert build_knowledge.table_name == "Knowledge"

    def test_sql_file_path(self):
        """Knowledge 的 SQL 檔案路徑應正確。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        assert build_knowledge.sql_file_path == os.path.join(
            "build_DB", "INFO_sql", "Knowledge.sql"
        )

    def test_sql_content(self):
        """Knowledge 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        assert "CREATE TABLE" in build_knowledge.sql
        assert "`INFO`.`Knowledge`" in build_knowledge.sql
        assert "`id`" in build_knowledge.sql
        assert "`category`" in build_knowledge.sql
        assert "`term`" in build_knowledge.sql
        assert "`description`" in build_knowledge.sql

    def test_is_subclass(self):
        """BuildINFOTABLEKnowledge 應繼承自 BuildINFOTABLE。"""
        assert issubclass(BuildINFOTABLEKnowledge, BuildINFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 Knowledge SQL 中所有欄位名稱。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        columns = build_knowledge._get_defined_columns()

        expected_columns = {'id', 'category', 'term', 'description'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 Knowledge 欄位的型別與約束。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        columns = build_knowledge._get_defined_columns()

        assert columns['id'] == 'INT AUTO_INCREMENT'
        assert columns['category'] == 'VARCHAR(50) NOT NULL'
        assert columns['term'] == 'VARCHAR(100) NOT NULL'
        assert columns['description'] == 'TEXT NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_knowledge, 'check_table_exists', return_value=False)
        mocker.patch.object(build_knowledge, 'post_process')

        build_knowledge.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_knowledge.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_knowledge, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_knowledge, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_knowledge, 'post_alter')

        build_knowledge.build(mock_conn)

        build_knowledge._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_knowledge.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_knowledge = BuildINFOTABLEKnowledge()
        mock_conn = mocker.Mock()
        missing = {'description'}
        mocker.patch.object(build_knowledge, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_knowledge, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_knowledge, 'post_alter')

        build_knowledge.build(mock_conn)

        build_knowledge.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildINFOTABLETradingCalendar:
    """測試 BuildINFOTABLETradingCalendar 資料表建構類別。"""

    def test_table_name(self):
        """TradingCalendar 資料表名稱應為 'TradingCalendar'。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        assert build_calendar.table_name == "TradingCalendar"

    def test_sql_file_path(self):
        """TradingCalendar 的 SQL 檔案路徑應正確。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        assert build_calendar.sql_file_path == os.path.join(
            "build_DB", "INFO_sql", "TradingCalendar.sql"
        )

    def test_sql_content(self):
        """TradingCalendar 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        assert "CREATE TABLE" in build_calendar.sql
        assert "`INFO`.`TradingCalendar`" in build_calendar.sql
        assert "`Date`" in build_calendar.sql
        assert "`IsOpen`" in build_calendar.sql
        assert "`Description`" in build_calendar.sql

    def test_is_subclass(self):
        """BuildINFOTABLETradingCalendar 應繼承自 BuildINFOTABLE。"""
        assert issubclass(BuildINFOTABLETradingCalendar, BuildINFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 TradingCalendar SQL 中所有欄位名稱。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        columns = build_calendar._get_defined_columns()

        expected_columns = {'Date', 'IsOpen', 'Description'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 TradingCalendar 欄位的型別與約束。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        columns = build_calendar._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['IsOpen'] == 'TINYINT(1) NOT NULL DEFAULT 1'
        assert columns['Description'] == 'VARCHAR(100) DEFAULT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_calendar, 'check_table_exists', return_value=False)
        mocker.patch.object(build_calendar, 'post_process')

        build_calendar.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_calendar.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_calendar, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_calendar, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_calendar, 'post_alter')

        build_calendar.build(mock_conn)

        build_calendar._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_calendar.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_calendar = BuildINFOTABLETradingCalendar()
        mock_conn = mocker.Mock()
        missing = {'Description'}
        mocker.patch.object(build_calendar, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_calendar, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_calendar, 'post_alter')

        build_calendar.build(mock_conn)

        build_calendar.post_alter.assert_called_once_with(mock_conn, missing)

    def test_csv_data_exists(self):
        """trading_calendar_data.csv 應存在且包含 365 筆資料。"""
        import pandas as pd
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        assert os.path.exists(csv_path)
        df = pd.read_csv(csv_path)
        assert len(df) == 365

    def test_csv_data_columns(self):
        """CSV 資料應包含 Date、IsOpen、Description 三個欄位。"""
        import pandas as pd
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        df = pd.read_csv(csv_path)
        assert set(df.columns) == {'Date', 'IsOpen', 'Description'}

    def test_csv_data_values(self):
        """CSV 資料的 IsOpen 欄位應只有 0 和 1。"""
        import pandas as pd
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        df = pd.read_csv(csv_path)
        assert set(df['IsOpen'].unique()) == {0, 1}

    def test_csv_data_date_range(self):
        """CSV 資料日期範圍應為 2026-01-01 至 2026-12-31。"""
        import pandas as pd
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        df = pd.read_csv(csv_path)
        assert df['Date'].iloc[0] == '2026-01-01'
        assert df['Date'].iloc[-1] == '2026-12-31'

    def test_csv_weekends_closed(self):
        """CSV 資料中所有週六日應標記為休市。"""
        import pandas as pd
        from datetime import datetime
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        df = pd.read_csv(csv_path)
        df['DateObj'] = pd.to_datetime(df['Date'])
        df['Weekday'] = df['DateObj'].dt.weekday
        weekends = df[df['Weekday'].isin([5, 6])]
        assert (weekends['IsOpen'] == 0).all()

    def test_csv_national_holidays_closed(self):
        """CSV 資料中國定假日應標記為休市。"""
        import pandas as pd
        csv_path = os.path.join(
            "build_DB", "INFO_sql", "trading_calendar_data.csv"
        )
        df = pd.read_csv(csv_path)
        national_holidays = [
            '2026-01-01', '2026-01-02', '2026-01-26', '2026-01-27',
            '2026-01-28', '2026-01-29', '2026-01-30', '2026-02-02',
            '2026-02-23', '2026-04-03', '2026-04-06', '2026-05-01',
            '2026-05-25', '2026-06-19', '2026-09-29', '2026-10-05',
            '2026-10-09',
        ]
        for holiday in national_holidays:
            row = df[df['Date'] == holiday]
            assert len(row) == 1, f"缺少日期 {holiday}"
            assert row['IsOpen'].iloc[0] == 0, f"{holiday} 應標記為休市"
