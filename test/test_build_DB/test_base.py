import os
import shutil
import pytest
import tempfile

from sqlalchemy import create_engine

from build_DB.base import BuildEmptyDB, BaseBuildTABLE, BaseBuild

@pytest.fixture
def build_db():
    # Create a temporary file with the desired content
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write("CREATE DATABASE IF NOT EXISTS `BASE`")
        temp_file_path = temp_file.name
    return BuildEmptyDB(temp_file_path)

class TestBuildEmptyDB:
    def test_read_sql_file(self, build_db):
        sql = build_db.read_sql_file()
        assert "CREATE DATABASE IF NOT EXISTS `BASE`" == sql

    def test_get_db_name(self, build_db):
        db_name = build_db.get_db_name()
        assert db_name == "BASE"

    def test_check_db_exists(self, build_db, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchall.return_value = [["BASE"]]
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_db_exists
        exists = build_db.check_db_exists(mock_conn)
        
        # Assert that the database exists
        assert exists is True

    def test_check_db_not_exists(self, build_db, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchall.return_value = []
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_db_exists
        exists = build_db.check_db_exists(mock_conn)
        
        # Assert that the database does not exist
        assert exists is False

    def test_build_pass(self, build_db, mocker):
        """資料庫不存在時，應執行 CREATE DATABASE 並 commit。"""
        mocker_conn_server = mocker.Mock()
        mocker.patch.object(build_db, 'check_db_exists', return_value=False)

        build_db.build(mocker_conn_server)

        mocker_conn_server.execute.assert_called_once()
        mocker_conn_server.commit.assert_called_once()

    def test_build_fail(self, build_db, mocker):
        """資料庫已存在時，不應執行 CREATE DATABASE。"""
        mocker_conn_server = mocker.Mock()
        mocker.patch.object(build_db, 'check_db_exists', return_value=True)

        build_db.build(mocker_conn_server)

        mocker_conn_server.execute.assert_not_called()
        mocker_conn_server.commit.assert_not_called()
        
class BuildTEMPTABLETemp(BaseBuildTABLE):
    def post_process(self, conn):
        """
        No post-processing steps are defined in this class.
        """
        pass

@pytest.fixture
def build_temp_table():
    temp_file_path = "build_DB/TEMP_sql/Temp.sql"
    # Ensure the directory exists before creating the file
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    
    # Create and write to the file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("CREATE TABLE IF NOT EXISTS `TEMP` (id INT PRIMARY KEY, name VARCHAR(50))")
    build_obj = BuildTEMPTABLETemp()

    # Remove the build_DB/TEMP_sql directory and its contents if it exists
    temp_dir_path = "build_DB/TEMP_sql"
    if os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    return build_obj

class TestBaseBuildTABLE:
    def test_read_sql_file(self, build_temp_table):
        sql = build_temp_table.sql
        assert "CREATE TABLE IF NOT EXISTS `TEMP` (id INT PRIMARY KEY, name VARCHAR(50))" == sql

    def test_check_table_exists(self, build_temp_table, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()

        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchone.return_value = [1]
        mock_conn.execute.return_value = mock_results

        # Use the mocked connection to test check_table_exists
        exists = build_temp_table.check_table_exists(mock_conn)

        # Assert that the table exists
        assert exists is True

    def test_check_table_not_exists(self, build_temp_table, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()

        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchone.return_value = [0]
        mock_conn.execute.return_value = mock_results

        # Use the mocked connection to test check_table_exists
        exists = build_temp_table.check_table_exists(mock_conn)

        # Assert that the table does not exist
        assert exists is False

    def test_build_pass(self, build_temp_table, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        mocker_conn_server = mocker.Mock()
        mocker.patch.object(build_temp_table, 'check_table_exists', return_value=False)
        mocker.patch.object(build_temp_table, 'post_process')

        build_temp_table.build(mocker_conn_server)

        mocker_conn_server.execute.assert_called_once()
        mocker_conn_server.commit.assert_called_once()
        build_temp_table.post_process.assert_called_once_with(mocker_conn_server)

    def test_build_existing_table_calls_alter(self, build_temp_table, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns。"""
        mocker_conn_server = mocker.Mock()
        mocker.patch.object(build_temp_table, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_temp_table, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_temp_table, 'post_alter')

        build_temp_table.build(mocker_conn_server)

        build_temp_table._alter_table_add_columns.assert_called_once_with(mocker_conn_server)
        build_temp_table.post_alter.assert_not_called()

    def test_build_existing_table_calls_post_alter(self, build_temp_table, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        mocker_conn_server = mocker.Mock()
        missing = {'NewCol'}
        mocker.patch.object(build_temp_table, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_temp_table, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_temp_table, 'post_alter')

        build_temp_table.build(mocker_conn_server)

        build_temp_table.post_alter.assert_called_once_with(mocker_conn_server, missing)


@pytest.fixture
def build_stockname_table():
    """建立使用多欄位 SQL 的 BaseBuildTABLE 實例，用於測試欄位解析。"""
    temp_file_path = "build_DB/TESTDB_sql/StockName.sql"
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

    sql_content = (
        "CREATE TABLE `TESTDB`.`StockName` (\n"
        "    `SecurityCode` VARCHAR(10) NOT NULL,\n"
        "    `StockName` VARCHAR(15) NOT NULL,\n"
        "    PRIMARY KEY (`SecurityCode`)\n"
        ")"
    )
    with open(temp_file_path, 'w') as f:
        f.write(sql_content)

    build_obj = BuildTESTDBTABLEStockName()

    temp_dir_path = "build_DB/TESTDB_sql"
    if os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    return build_obj


class BuildTESTDBTABLEStockName(BaseBuildTABLE):
    def post_process(self, conn):
        pass


class TestGetDefinedColumns:
    def test_parse_all_columns(self, build_stockname_table):
        """應正確解析 SQL 中所有欄位名稱與定義。"""
        columns = build_stockname_table._get_defined_columns()
        assert 'SecurityCode' in columns
        assert 'StockName' in columns
        assert len(columns) == 2

    def test_column_definitions(self, build_stockname_table):
        """應正確解析欄位的型別與約束。"""
        columns = build_stockname_table._get_defined_columns()
        assert columns['SecurityCode'] == 'VARCHAR(10) NOT NULL'
        assert columns['StockName'] == 'VARCHAR(15) NOT NULL'

    def test_excludes_primary_key(self, build_stockname_table):
        """不應將 PRIMARY KEY 解析為欄位。"""
        columns = build_stockname_table._get_defined_columns()
        for col_name in columns:
            assert 'PRIMARY' not in col_name


class TestGetExistingColumns:
    def test_returns_column_set(self, build_stockname_table, mocker):
        """應從 information_schema 查詢結果回傳欄位名稱的集合。"""
        mock_conn = mocker.Mock()
        mock_result = mocker.Mock()
        mock_result.fetchall.return_value = [
            ('SecurityCode',), ('StockName',)
        ]
        mock_conn.execute.return_value = mock_result

        columns = build_stockname_table._get_existing_columns(mock_conn)

        assert columns == {'SecurityCode', 'StockName'}
        mock_conn.execute.assert_called_once()


class TestAlterTableAddColumns:
    def test_add_missing_columns(self, build_stockname_table, mocker):
        """有缺少欄位時，應對每個欄位執行 ALTER TABLE ADD COLUMN。"""
        mock_conn = mocker.Mock()
        mocker.patch.object(
            build_stockname_table, '_get_existing_columns',
            return_value={'SecurityCode'}
        )

        result = build_stockname_table._alter_table_add_columns(mock_conn)

        # 應執行 1 次 ALTER（StockName）
        assert mock_conn.execute.call_count == 1
        mock_conn.commit.assert_called_once()

        # 驗證回傳缺少的欄位集合
        assert result == {'StockName'}

        # 驗證 ALTER SQL 內容
        executed_sqls = [
            str(call.args[0].text) for call in mock_conn.execute.call_args_list
        ]
        assert any('StockName' in sql for sql in executed_sqls)

    def test_no_missing_columns(self, build_stockname_table, mocker):
        """欄位完整時，不應執行任何 ALTER 操作。"""
        mock_conn = mocker.Mock()
        mocker.patch.object(
            build_stockname_table, '_get_existing_columns',
            return_value={'SecurityCode', 'StockName'}
        )

        result = build_stockname_table._alter_table_add_columns(mock_conn)

        assert result == set()
        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()

@pytest.fixture
def build_temp(mocker):
    mocker_typeclass = mocker.Mock()
    name = "TEMP"
    return BaseBuild(mocker_typeclass, name)

class TestBaseBuild:
    def test_build_db(self, build_temp, mocker):
        mocker_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)
        build_temp.build_db(mocker_conn_server)
