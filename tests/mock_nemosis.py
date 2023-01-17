import pandas as pd

mock_tables = {
    "DISPATCHPRICE": pd.DataFrame(
        columns=["REGIONID", "SETTLEMENTDATE", "RRP", "INTERVENTION"],
        data=[
            ("SA1", "2020/01/01 01:00:00", 55.4, 0),
            ("SA1", "2020/01/01 01:00:00", 65.4, 1),
            ("TAS1", "2020/01/01 01:00:00", 75.4, 0),
            ("TAS1", "2020/01/01 01:00:00", 85.4, 1),
        ],
    ),
    "DISPATCHREGIONSUM": pd.DataFrame(
        columns=["REGIONID", "SETTLEMENTDATE", "TOTALDEMAND", "INTERVENTION"],
        data=[
            ("SA1", "2020/01/01 01:00:00", 1000.0, 0),
            ("SA1", "2020/01/01 01:00:00", 1001.0, 1),
            ("TAS1", "2020/01/01 01:00:00", 2000.0, 0),
            ("TAS1", "2020/01/01 01:00:00", 2001.0, 1),
        ],
    ),
    "DAILY_REGION_SUMMARY": pd.DataFrame(
        columns=["REGIONID", "SETTLEMENTDATE", "TOTALDEMAND", "RRP", "INTERVENTION"],
        data=[
            ("SA1", "2020/01/01 05:00:00", 1010.0, 80.1, 0),
            ("SA1", "2020/01/01 05:00:00", 1011.0, 80.0, 1),
            ("TAS1", "2020/01/01 05:00:00", 2010.0, 90.0, 0),
            ("TAS1", "2020/01/01 05:00:00", 2011.0, 90.1, 1),
        ],
    ),
    "DISPATCHLOAD": pd.DataFrame(
        columns=[
            "SETTLEMENTDATE",
            "INTERVENTION",
            "DUID",
            "AVAILABILITY",
            "TOTALCLEARED",
            "INITIALMW",
            "RAMPDOWNRATE",
            "RAMPUPRATE",
        ],
        data=[
            ("2020/01/01 01:00:00", 0, "A", 100.0, 80.0, 70.0, 121.0, 125.0),
            ("2020/01/01 01:00:00", 1, "A", 101.0, 81.0, 71.0, 122.0, 426.0),
            ("2020/01/01 01:00:00", 0, "B", 200.0, 90.0, 60.0, 123.0, 127.0),
            ("2020/01/01 01:00:00", 1, "B", 201.0, 91.0, 61.0, 124.0, 128.0),
            ("2020/01/01 01:05:00", 0, "A", 100.0, 80.0, 70.0, 121.0, 125.0),
            ("2020/01/01 01:05:00", 1, "A", 101.0, 81.0, 71.0, 122.0, 426.0),
            ("2020/01/01 01:05:00", 0, "B", 200.0, 90.0, 60.0, 123.0, 127.0),
            ("2020/01/01 01:05:00", 1, "B", 201.0, 91.0, 61.0, 124.0, 128.0),
        ],
    ),
    "NEXT_DAY_DISPATCHLOAD": pd.DataFrame(
        columns=[
            "SETTLEMENTDATE",
            "INTERVENTION",
            "DUID",
            "AVAILABILITY",
            "TOTALCLEARED",
            "INITIALMW",
            "RAMPDOWNRATE",
            "RAMPUPRATE",
        ],
        data=[
            ("2020/01/01 05:00:00", 0, "A", 102.0, 81.0, 71.0, 241.0, 245.0),
            ("2020/01/01 05:00:00", 1, "A", 103.0, 82.0, 72.0, 1000.0, 246.0),
            ("2020/01/01 05:00:00", 0, "B", 202.0, 91.0, 61.0, 243.0, 247.0),
            ("2020/01/01 05:00:00", 1, "B", 203.0, 92.0, 62.0, 244.0, 248.0),
            ("2020/01/01 05:05:00", 0, "A", 102.0, 81.0, 71.0, 241.0, 245.0),
            ("2020/01/01 05:05:00", 1, "A", 103.0, 82.0, 72.0, 1000.0, 246.0),
            ("2020/01/01 05:05:00", 0, "B", 202.0, 91.0, 61.0, 243.0, 247.0),
            ("2020/01/01 05:05:00", 1, "B", 203.0, 92.0, 62.0, 244.0, 248.0),
        ],
    ),
    "BIDPEROFFER_D": pd.DataFrame(
        columns=[
            "INTERVAL_DATETIME",
            "SETTLEMENTDATE",
            "DUID",
            "BIDTYPE",
            "BANDAVAIL1",
            "BANDAVAIL2",
            "BANDAVAIL3",
            "BANDAVAIL4",
            "BANDAVAIL5",
            "BANDAVAIL6",
            "BANDAVAIL7",
            "BANDAVAIL8",
            "BANDAVAIL9",
            "BANDAVAIL10",
            "MAXAVAIL",
            "ROCUP",
            "ROCDOWN",
            "PASAAVAILABILITY",
        ],
        data=[
            (
                "2020/01/01 01:00:00",
                "2019/12/31 00:00:00",
                "A",
                "ENERGY",
                0,
                0,
                0,
                70,
                0,
                0,
                0,
                0,
                0,
                40,
                101,
                50,
                1,
                110,
            ),
            (
                "2020/01/01 05:00:00",
                "2020/01/01 00:00:00",
                "A",
                "ENERGY",
                0,
                0,
                70,
                0,
                0,
                0,
                0,
                0,
                12,
                0,
                102,
                1,
                50,
                120,
            ),
            (
                "2020/01/01 01:00:00",
                "2019/12/31 00:00:00",
                "B",
                "ENERGY",
                0,
                0,
                0,
                0,
                100,
                0,
                0,
                0,
                10,
                0,
                103,
                2,
                60,
                130,
            ),
            (
                "2020/01/01 05:00:00",
                "2020/01/01 00:00:00",
                "B",
                "ENERGY",
                0,
                0,
                0,
                100,
                0,
                0,
                0,
                100,
                10,
                0,
                104,
                60,
                20,
                140,
            ),
            (
                "2020/01/01 01:05:00",
                "2019/12/31 00:00:00",
                "A",
                "ENERGY",
                0,
                0,
                0,
                70,
                0,
                0,
                0,
                0,
                0,
                40,
                101,
                50,
                1,
                110,
            ),
            (
                "2020/01/01 05:05:00",
                "2020/01/01 00:00:00",
                "A",
                "ENERGY",
                0,
                0,
                70,
                0,
                0,
                0,
                0,
                0,
                12,
                0,
                102,
                1,
                50,
                120,
            ),
            (
                "2020/01/01 01:05:00",
                "2019/12/31 00:00:00",
                "B",
                "ENERGY",
                0,
                0,
                0,
                0,
                100,
                0,
                0,
                0,
                10,
                0,
                103,
                2,
                60,
                130,
            ),
            (
                "2020/01/01 05:05:00",
                "2020/01/01 00:00:00",
                "B",
                "ENERGY",
                0,
                0,
                0,
                100,
                0,
                0,
                0,
                100,
                10,
                0,
                104,
                60,
                20,
                140,
            ),
        ],
    ),
    "BIDDAYOFFER_D": pd.DataFrame(
        columns=[
            "SETTLEMENTDATE",
            "DUID",
            "BIDTYPE",
            "PRICEBAND1",
            "PRICEBAND2",
            "PRICEBAND3",
            "PRICEBAND4",
            "PRICEBAND5",
            "PRICEBAND6",
            "PRICEBAND7",
            "PRICEBAND8",
            "PRICEBAND9",
            "PRICEBAND10",
        ],
        data=[
            (
                "2019/12/31 00:00:00",
                "A",
                "ENERGY",
                1.1,
                2.1,
                3.1,
                4.1,
                5.1,
                6.1,
                7.1,
                8.1,
                9.1,
                10.1,
            ),
            (
                "2020/01/01 00:00:00",
                "A",
                "ENERGY",
                1.2,
                2.2,
                3.2,
                4.2,
                5.2,
                6.2,
                7.2,
                8.2,
                9.2,
                10.2,
            ),
            (
                "2019/12/31 00:00:00",
                "B",
                "ENERGY",
                1.3,
                2.3,
                3.3,
                4.3,
                5.3,
                6.3,
                7.3,
                8.3,
                9.3,
                10.3,
            ),
            (
                "2020/01/01 00:00:00",
                "B",
                "ENERGY",
                1.4,
                2.4,
                3.4,
                4.4,
                5.4,
                6.4,
                7.4,
                8.4,
                9.4,
                10.4,
            ),
        ],
    ),
    "Generators and Scheduled Loads": pd.read_csv("tests/test_duid_data.csv"),
}


def dynamic_data_compiler(
    start_time,
    end_time,
    table_name,
    raw_data_location,
    select_columns=None,
    filter_cols=None,
    filter_values=None,
    fformat="feather",
    keep_csv=True,
    parse_data_types=True,
    **kwargs
):

    data = mock_tables[table_name]

    if "SETTLEMENTDATE" in data.columns and table_name not in [
        "BIDDAYOFFER_D",
        "BIDPEROFFER_D",
    ]:
        data["SETTLEMENTDATE"] = pd.to_datetime(data["SETTLEMENTDATE"])

    if "INTERVAL_DATETIME" in data.columns:
        data["INTERVAL_DATETIME"] = pd.to_datetime(data["INTERVAL_DATETIME"])

    return data


def static_table(table_name, raw_data_location, select_columns=None):

    data = mock_tables[table_name]

    return data