def test_import_module():
    from SQL import query
    res = query("select 1;")
    assert res == [[1]]
