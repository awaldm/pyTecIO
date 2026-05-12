import pathlib

import pandas as pd

import pytecio


TESTDATA = pathlib.Path(__file__).parent / "testdata"


def test_public_api_exports_reader_functions():
    assert pytecio.read_ascii is not None
    assert pytecio.read1D is not None
    assert pytecio.read_1d is pytecio.read1D


def test_find_test_data():
    assert TESTDATA.is_dir()


def test_read_1d_returns_numeric_dataframe():
    testfile = TESTDATA / "testdata_1D.dat"

    frame = pytecio.read1D(testfile, to_pandas=True)

    assert list(frame.columns[:3]) == ["X", "Y", "Z"]
    assert frame.shape == (45, 12)
    assert all(pd.api.types.is_float_dtype(dtype) for dtype in frame.dtypes)


def test_read_ascii_existing_sample_is_numeric():
    testfile = TESTDATA / "testdata_1D.dat"

    zones, dfs, elements = pytecio.read_ascii(testfile)

    assert zones == ["snapshot 1"]
    assert len(dfs) == 1
    assert elements == []
    assert list(dfs[0].columns[:3]) == ["X", "Y", "Z"]
    assert dfs[0].shape == (45, 12)
    assert all(pd.api.types.is_float_dtype(dtype) for dtype in dfs[0].dtypes)


def test_read_ascii_supports_lowercase_keywords_without_dt():
    testfile = TESTDATA / "structured_lowercase.dat"

    zones, dfs, elements = pytecio.read_ascii(testfile)

    assert zones == ["surface"]
    assert elements == []
    assert dfs[0].to_dict(orient="records") == [
        {"x": 0.0, "y": 1.0},
        {"x": 1.5, "y": 2.5},
    ]


def test_read_ascii_supports_multiline_variables_and_datasetaux():
    testfile = TESTDATA / "multiline_variables.dat"

    zones, dfs, elements = pytecio.read_ascii(testfile)

    assert zones == ["vars"]
    assert elements == []
    assert list(dfs[0].columns) == ["x", "y"]
    assert dfs[0].iloc[-1].to_dict() == {"x": 1.0, "y": 2.0}


def test_read_ascii_returns_unstructured_connectivity():
    testfile = TESTDATA / "unstructured_zone.dat"

    zones, dfs, elements = pytecio.read_ascii(testfile)

    assert zones == ["tri"]
    assert dfs[0].shape == (3, 3)
    assert list(dfs[0].columns) == ["x", "y", "p"]
    assert len(elements) == 1
    assert elements[0].shape == (1, 3)
    assert elements[0].iloc[0].tolist() == [1, 2, 3]


def test_read_ascii_reads_multiple_zones():
    testfile = TESTDATA / "multiple_zones.dat"

    zones, dfs, elements = pytecio.read_ascii(testfile)

    assert zones == ["zone a", "zone b"]
    assert elements == []
    assert [df["value"].tolist() for df in dfs] == [[10, 20], [30, 40]]
