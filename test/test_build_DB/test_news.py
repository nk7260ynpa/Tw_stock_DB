import os
import shutil
import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.news import BuildNEWS, BuildNEWSTABLE, BuildNEWSTABLECTEE


class TestBuildNEWS:
    """測試 BuildNEWS 資料庫建構類別。"""

    def test_name(self):
        """BuildNEWS 的名稱應為 'NEWS'。"""
        build_news = BuildNEWS()
        assert build_news.name == "NEWS"

    def test_typeclass(self):
        """BuildNEWS 的 typeclass 應為 BuildNEWSTABLE。"""
        build_news = BuildNEWS()
        assert build_news.typeclass is BuildNEWSTABLE

    def test_build_db(self, mocker):
        """應正確呼叫 BuildEmptyDB 建立 NEWS 資料庫。"""
        build_news = BuildNEWS()
        mock_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)

        build_news.build_db(mock_conn_server)

        mock_build_empty_db.build.assert_called_once_with(mock_conn_server)

    def test_build_table_discovers_subclasses(self, mocker):
        """build_table 應自動發現並建構 BuildNEWSTABLE 的子類別。"""
        build_news = BuildNEWS()
        mock_conn = mocker.Mock()

        subclasses = BuildNEWSTABLE.__subclasses__()
        assert len(subclasses) >= 1
        assert BuildNEWSTABLECTEE in subclasses

        # mock 每個子類別的 build 方法
        for subclass in subclasses:
            mocker.patch.object(subclass, 'build', return_value=None)

        build_news.build_table(mock_conn)

        for subclass in subclasses:
            subclass.build.assert_called_once()


class TestBuildNEWSTABLE:
    """測試 BuildNEWSTABLE 資料表基類。"""

    def test_is_subclass_of_base(self):
        """BuildNEWSTABLE 應繼承自 BaseBuildTABLE。"""
        assert issubclass(BuildNEWSTABLE, BaseBuildTABLE)


class TestBuildNEWSTABLECTEE:
    """測試 BuildNEWSTABLECTEE 資料表建構類別。"""

    def test_table_name(self):
        """CTEE 資料表名稱應為 'CTEE'。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert build_ctee.table_name == "CTEE"

    def test_sql_file_path(self):
        """CTEE 的 SQL 檔案路徑應正確。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert build_ctee.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "CTEE.sql"
        )

    def test_sql_content(self):
        """CTEE 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert "CREATE TABLE" in build_ctee.sql
        assert "`NEWS`.`CTEE`" in build_ctee.sql
        assert "`Date`" in build_ctee.sql
        assert "`url`" in build_ctee.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLECTEE 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLECTEE, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CTEE SQL 中所有欄位名稱。"""
        build_ctee = BuildNEWSTABLECTEE()
        columns = build_ctee._get_defined_columns()

        expected_columns = {'Date', 'Time', 'Author', 'Head', 'SubHead', 'HashTag', 'url'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CTEE 欄位的型別與約束。"""
        build_ctee = BuildNEWSTABLECTEE()
        columns = build_ctee._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['Time'] == 'TIME DEFAULT NULL'
        assert columns['Author'] == 'VARCHAR(100) DEFAULT NULL'
        assert columns['Head'] == 'VARCHAR(500) NOT NULL'
        assert columns['SubHead'] == 'TEXT DEFAULT NULL'
        assert columns['HashTag'] == 'VARCHAR(500) DEFAULT NULL'
        assert columns['url'] == 'VARCHAR(1000) NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=False)
        mocker.patch.object(build_ctee, 'post_process')

        build_ctee.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_ctee.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ctee, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_ctee, 'post_alter')

        build_ctee.build(mock_conn)

        build_ctee._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_ctee.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        missing = {'HashTag'}
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ctee, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_ctee, 'post_alter')

        build_ctee.build(mock_conn)

        build_ctee.post_alter.assert_called_once_with(mock_conn, missing)
