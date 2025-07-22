#update, delete, insert

def get_size():
    from SQL import query
    size = query("select * from test_table;").fetchall()
    return len(size)

def insert_into():
    from SQL import query
    from databasebuild import random_string
    query("insert into test_table (first_name, last_name, address, city) values (?, ?, ?, ?);",
          (random_string(10), random_string(10), random_string(20), random_string(15)))

def get_one():
    from SQL import query
    res = query("select * from test_table limit 1;").fetchall()
    return len(res)   

def get_some():
    from SQL import query
    res = query("select * from test_table limit 10;").fetchall()
    return len(res)

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

def test_select_all():
    from SQL import query
    res = get_size()
    assert res > 0

def test_insert_into():
    from SQL import query
    count = get_size()
    insert_into()
    count2 = get_size()
    assert count2 == count + 1
    
def test_select_one():
    from SQL import query
    res = get_one()
    assert res == 1

def test_select_some():
    from SQL import query
    res = get_some()
    assert res == 10

