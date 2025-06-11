def test_import_module():
    """
    Simple test example for an SQLite3 Query

    Important Notes:
    The "as A" is required to be able to access
    the results by column name. Selecting from a
    real table will automatically populate the
    result column names as attributes
    """
    from SQL import query
    res = query("select 1 as A;").fetchall()
    a = res.pop()
    assert a.A == 1
