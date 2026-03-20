import os

import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.special_info import (BuildSPECIAL_INFO, BuildSPECIAL_INFOTABLE,
                                    BuildSPECIAL_INFOTABLEOilPrice,
                                    BuildSPECIAL_INFOTABLEOilPriceUploaded,
                                    BuildSPECIAL_INFOTABLEGoldPrice,
                                    BuildSPECIAL_INFOTABLEGoldPriceUploaded,
                                    BuildSPECIAL_INFOTABLEBitcoinPrice,
                                    BuildSPECIAL_INFOTABLEBitcoinPriceUploaded,
                                    BuildSPECIAL_INFOTABLECurrencyPrice,
                                    BuildSPECIAL_INFOTABLECurrencyPriceUploaded,
                                    BuildSPECIAL_INFOTABLEIndicesPrice,
                                    BuildSPECIAL_INFOTABLEIndicesPriceUploaded)


class TestBuildSPECIAL_INFO:
    """測試 BuildSPECIAL_INFO 資料庫建構類別。"""

    def test_name(self):
        """BuildSPECIAL_INFO 的名稱應為 'SPECIAL_INFO'。"""
        build_special_info = BuildSPECIAL_INFO()
        assert build_special_info.name == "SPECIAL_INFO"

    def test_typeclass(self):
        """BuildSPECIAL_INFO 的 typeclass 應為 BuildSPECIAL_INFOTABLE。"""
        build_special_info = BuildSPECIAL_INFO()
        assert build_special_info.typeclass is BuildSPECIAL_INFOTABLE

    def test_build_db(self, mocker):
        """應正確呼叫 BuildEmptyDB 建立 SPECIAL_INFO 資料庫。"""
        build_special_info = BuildSPECIAL_INFO()
        mock_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)

        build_special_info.build_db(mock_conn_server)

        mock_build_empty_db.build.assert_called_once_with(mock_conn_server)

    def test_build_table_discovers_subclasses(self, mocker):
        """build_table 應自動發現並建構 BuildSPECIAL_INFOTABLE 的子類別。"""
        build_special_info = BuildSPECIAL_INFO()
        mock_conn = mocker.Mock()

        subclasses = BuildSPECIAL_INFOTABLE.__subclasses__()
        assert len(subclasses) >= 10
        assert BuildSPECIAL_INFOTABLEOilPrice in subclasses
        assert BuildSPECIAL_INFOTABLEOilPriceUploaded in subclasses
        assert BuildSPECIAL_INFOTABLEGoldPrice in subclasses
        assert BuildSPECIAL_INFOTABLEGoldPriceUploaded in subclasses
        assert BuildSPECIAL_INFOTABLEBitcoinPrice in subclasses
        assert BuildSPECIAL_INFOTABLEBitcoinPriceUploaded in subclasses
        assert BuildSPECIAL_INFOTABLECurrencyPrice in subclasses
        assert BuildSPECIAL_INFOTABLECurrencyPriceUploaded in subclasses
        assert BuildSPECIAL_INFOTABLEIndicesPrice in subclasses
        assert BuildSPECIAL_INFOTABLEIndicesPriceUploaded in subclasses

        # mock 每個子類別的 build 方法
        for subclass in subclasses:
            mocker.patch.object(subclass, 'build', return_value=None)

        build_special_info.build_table(mock_conn)

        for subclass in subclasses:
            subclass.build.assert_called_once()


class TestBuildSPECIAL_INFOTABLE:
    """測試 BuildSPECIAL_INFOTABLE 資料表基類。"""

    def test_is_subclass_of_base(self):
        """BuildSPECIAL_INFOTABLE 應繼承自 BaseBuildTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLE, BaseBuildTABLE)


class TestBuildSPECIAL_INFOTABLEOilPrice:
    """測試 BuildSPECIAL_INFOTABLEOilPrice 資料表建構類別。"""

    def test_table_name(self):
        """OilPrice 資料表名稱應為 'OilPrice'。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert build_oil_price.table_name == "OilPrice"

    def test_sql_file_path(self):
        """OilPrice 的 SQL 檔案路徑應正確。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert build_oil_price.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "OilPrice.sql"
        )

    def test_sql_content(self):
        """OilPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert "CREATE TABLE" in build_oil_price.sql
        assert "`SPECIAL_INFO`.`OilPrice`" in build_oil_price.sql
        assert "`Date`" in build_oil_price.sql
        assert "`Product`" in build_oil_price.sql
        assert "`Open`" in build_oil_price.sql
        assert "`High`" in build_oil_price.sql
        assert "`Low`" in build_oil_price.sql
        assert "`Close`" in build_oil_price.sql
        assert "`Volume`" in build_oil_price.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEOilPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEOilPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 OilPrice SQL 中所有欄位名稱。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        columns = build_oil_price._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 OilPrice 欄位的型別與約束。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        columns = build_oil_price._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '原油類型: WTI, Brent'"
        assert columns['Open'] == "DECIMAL(10, 2) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(10, 2) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(10, 2) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(10, 2) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=False)
        mocker.patch.object(build_oil_price, 'post_process')

        build_oil_price.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_oil_price.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_oil_price, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_oil_price, 'post_alter')

        build_oil_price.build(mock_conn)

        build_oil_price._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_oil_price.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_oil_price, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_oil_price, 'post_alter')

        build_oil_price.build(mock_conn)

        build_oil_price.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLEOilPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLEOilPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """OilPriceUploaded 資料表名稱應為 'OilPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert build_uploaded.table_name == "OilPriceUploaded"

    def test_sql_file_path(self):
        """OilPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "OilPriceUploaded.sql"
        )

    def test_sql_content(self):
        """OilPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`OilPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEOilPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEOilPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 OilPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 OilPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()


class TestBuildSPECIAL_INFOTABLEGoldPrice:
    """測試 BuildSPECIAL_INFOTABLEGoldPrice 資料表建構類別。"""

    def test_table_name(self):
        """GoldPrice 資料表名稱應為 'GoldPrice'。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        assert build_gold.table_name == "GoldPrice"

    def test_sql_file_path(self):
        """GoldPrice 的 SQL 檔案路徑應正確。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        assert build_gold.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "GoldPrice.sql"
        )

    def test_sql_content(self):
        """GoldPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        assert "CREATE TABLE" in build_gold.sql
        assert "`SPECIAL_INFO`.`GoldPrice`" in build_gold.sql
        assert "`Date`" in build_gold.sql
        assert "`Product`" in build_gold.sql
        assert "`Open`" in build_gold.sql
        assert "`High`" in build_gold.sql
        assert "`Low`" in build_gold.sql
        assert "`Close`" in build_gold.sql
        assert "`Volume`" in build_gold.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEGoldPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEGoldPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 GoldPrice SQL 中所有欄位名稱。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        columns = build_gold._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 GoldPrice 欄位的型別與約束。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        columns = build_gold._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '黃金類型: XAU'"
        assert columns['Open'] == "DECIMAL(10, 2) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(10, 2) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(10, 2) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(10, 2) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_gold, 'check_table_exists', return_value=False)
        mocker.patch.object(build_gold, 'post_process')

        build_gold.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_gold.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_gold, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_gold, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_gold, 'post_alter')

        build_gold.build(mock_conn)

        build_gold._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_gold.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_gold = BuildSPECIAL_INFOTABLEGoldPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_gold, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_gold, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_gold, 'post_alter')

        build_gold.build(mock_conn)

        build_gold.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLEGoldPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLEGoldPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """GoldPriceUploaded 資料表名稱應為 'GoldPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        assert build_uploaded.table_name == "GoldPriceUploaded"

    def test_sql_file_path(self):
        """GoldPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "GoldPriceUploaded.sql"
        )

    def test_sql_content(self):
        """GoldPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`GoldPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEGoldPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEGoldPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 GoldPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 GoldPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLEGoldPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()


class TestBuildSPECIAL_INFOTABLEBitcoinPrice:
    """測試 BuildSPECIAL_INFOTABLEBitcoinPrice 資料表建構類別。"""

    def test_table_name(self):
        """BitcoinPrice 資料表名稱應為 'BitcoinPrice'。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        assert build_btc.table_name == "BitcoinPrice"

    def test_sql_file_path(self):
        """BitcoinPrice 的 SQL 檔案路徑應正確。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        assert build_btc.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "BitcoinPrice.sql"
        )

    def test_sql_content(self):
        """BitcoinPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        assert "CREATE TABLE" in build_btc.sql
        assert "`SPECIAL_INFO`.`BitcoinPrice`" in build_btc.sql
        assert "`Date`" in build_btc.sql
        assert "`Product`" in build_btc.sql
        assert "`Open`" in build_btc.sql
        assert "`High`" in build_btc.sql
        assert "`Low`" in build_btc.sql
        assert "`Close`" in build_btc.sql
        assert "`Volume`" in build_btc.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEBitcoinPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEBitcoinPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 BitcoinPrice SQL 中所有欄位名稱。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        columns = build_btc._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 BitcoinPrice 欄位的型別與約束（DECIMAL(12,2)）。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        columns = build_btc._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '加密貨幣類型: BTC'"
        assert columns['Open'] == "DECIMAL(12, 2) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(12, 2) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(12, 2) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(12, 2) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_btc, 'check_table_exists', return_value=False)
        mocker.patch.object(build_btc, 'post_process')

        build_btc.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_btc.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_btc, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_btc, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_btc, 'post_alter')

        build_btc.build(mock_conn)

        build_btc._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_btc.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_btc = BuildSPECIAL_INFOTABLEBitcoinPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_btc, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_btc, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_btc, 'post_alter')

        build_btc.build(mock_conn)

        build_btc.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLEBitcoinPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLEBitcoinPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """BitcoinPriceUploaded 資料表名稱應為 'BitcoinPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        assert build_uploaded.table_name == "BitcoinPriceUploaded"

    def test_sql_file_path(self):
        """BitcoinPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "BitcoinPriceUploaded.sql"
        )

    def test_sql_content(self):
        """BitcoinPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`BitcoinPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEBitcoinPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEBitcoinPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 BitcoinPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 BitcoinPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLEBitcoinPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()


class TestBuildSPECIAL_INFOTABLECurrencyPrice:
    """測試 BuildSPECIAL_INFOTABLECurrencyPrice 資料表建構類別。"""

    def test_table_name(self):
        """CurrencyPrice 資料表名稱應為 'CurrencyPrice'。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        assert build_currency.table_name == "CurrencyPrice"

    def test_sql_file_path(self):
        """CurrencyPrice 的 SQL 檔案路徑應正確。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        assert build_currency.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "CurrencyPrice.sql"
        )

    def test_sql_content(self):
        """CurrencyPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        assert "CREATE TABLE" in build_currency.sql
        assert "`SPECIAL_INFO`.`CurrencyPrice`" in build_currency.sql
        assert "`Date`" in build_currency.sql
        assert "`Product`" in build_currency.sql
        assert "`Open`" in build_currency.sql
        assert "`High`" in build_currency.sql
        assert "`Low`" in build_currency.sql
        assert "`Close`" in build_currency.sql
        assert "`Volume`" in build_currency.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLECurrencyPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLECurrencyPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CurrencyPrice SQL 中所有欄位名稱。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        columns = build_currency._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CurrencyPrice 欄位的型別與約束（DECIMAL(10,4)）。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        columns = build_currency._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '匯率類型: USDTWD, USDJPY 等'"
        assert columns['Open'] == "DECIMAL(10, 4) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(10, 4) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(10, 4) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(10, 4) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_currency, 'check_table_exists', return_value=False)
        mocker.patch.object(build_currency, 'post_process')

        build_currency.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_currency.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_currency, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_currency, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_currency, 'post_alter')

        build_currency.build(mock_conn)

        build_currency._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_currency.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_currency = BuildSPECIAL_INFOTABLECurrencyPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_currency, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_currency, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_currency, 'post_alter')

        build_currency.build(mock_conn)

        build_currency.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLECurrencyPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLECurrencyPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """CurrencyPriceUploaded 資料表名稱應為 'CurrencyPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        assert build_uploaded.table_name == "CurrencyPriceUploaded"

    def test_sql_file_path(self):
        """CurrencyPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "CurrencyPriceUploaded.sql"
        )

    def test_sql_content(self):
        """CurrencyPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`CurrencyPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLECurrencyPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLECurrencyPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CurrencyPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CurrencyPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLECurrencyPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()


class TestBuildSPECIAL_INFOTABLEIndicesPrice:
    """測試 BuildSPECIAL_INFOTABLEIndicesPrice 資料表建構類別。"""

    def test_table_name(self):
        """IndicesPrice 資料表名稱應為 'IndicesPrice'。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        assert build_indices.table_name == "IndicesPrice"

    def test_sql_file_path(self):
        """IndicesPrice 的 SQL 檔案路徑應正確。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        assert build_indices.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "IndicesPrice.sql"
        )

    def test_sql_content(self):
        """IndicesPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        assert "CREATE TABLE" in build_indices.sql
        assert "`SPECIAL_INFO`.`IndicesPrice`" in build_indices.sql
        assert "`Date`" in build_indices.sql
        assert "`Product`" in build_indices.sql
        assert "`Open`" in build_indices.sql
        assert "`High`" in build_indices.sql
        assert "`Low`" in build_indices.sql
        assert "`Close`" in build_indices.sql
        assert "`Volume`" in build_indices.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEIndicesPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEIndicesPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 IndicesPrice SQL 中所有欄位名稱。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        columns = build_indices._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 IndicesPrice 欄位的型別與約束。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        columns = build_indices._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '指數類型: DowJones, Nasdaq'"
        assert columns['Open'] == "DECIMAL(10, 2) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(10, 2) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(10, 2) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(10, 2) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_indices, 'check_table_exists', return_value=False)
        mocker.patch.object(build_indices, 'post_process')

        build_indices.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_indices.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_indices, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_indices, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_indices, 'post_alter')

        build_indices.build(mock_conn)

        build_indices._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_indices.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_indices = BuildSPECIAL_INFOTABLEIndicesPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_indices, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_indices, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_indices, 'post_alter')

        build_indices.build(mock_conn)

        build_indices.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLEIndicesPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLEIndicesPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """IndicesPriceUploaded 資料表名稱應為 'IndicesPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        assert build_uploaded.table_name == "IndicesPriceUploaded"

    def test_sql_file_path(self):
        """IndicesPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "IndicesPriceUploaded.sql"
        )

    def test_sql_content(self):
        """IndicesPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`IndicesPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEIndicesPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEIndicesPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 IndicesPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 IndicesPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLEIndicesPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()
