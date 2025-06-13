import pytest

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


@pytest.mark.parametrize('fx_load_db',
                         ['./test/sqlite3_data/full.db.sql'],
                         indirect=True)
def test_select_all(fx_load_db):
    from SQL import query
    res = query("select * from threshold;").fetchall()
    assert len(res) == 2
    r2 = res.pop()
    r1 = res.pop()
    assert r1.id == 1
    assert r1.direction == 'UNDER_OK'
    assert r1.level == 5
    assert r1.message == 'Supervisor not updating its metric'

    assert r2.id == 2
    assert r2.direction == 'ABOVE_OK'
    assert r2.level == 0.5
    assert r2.message == 'Temperature on core to high'
