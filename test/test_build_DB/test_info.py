import os

import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.info import (BuildINFO, BuildINFOTABLE,
                            BuildINFOTABLEKnowledge)


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
        assert len(subclasses) >= 1
        assert BuildINFOTABLEKnowledge in subclasses

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
