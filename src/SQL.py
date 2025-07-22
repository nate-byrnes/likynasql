import apsw
import apsw.ext
import apsw.bestpractice
import os
import importlib
import importlib.resources
import time
from support.log import simplog

apsw.bestpractice.apply(apsw.bestpractice.recommended)

dbfname = os.environ.get("TMMDBFILE", "minermgr.db")
_max_q_attempts = 25
_conn = None


def _open(defaultdbfname="minermgr.db"):
    global _conn, dbfname
    dbfname = os.environ.get("TMMDBFILE", defaultdbfname)
    cnt = 0
    while cnt < _max_q_attempts:
        cnt += 1
        try:
            _conn = apsw.Connection(dbfname)
            _conn.pragma("foreign_keys", True)
            _conn.row_trace = apsw.ext.DataClassRowFactory()  # to access row fields by name  # noqa: E501
        except apsw.BusyError:
            time.sleep(cnt**2 * 0.1)
            print("Database locked, attempting re-connect")
        except apsw.ReadOnlyError:
            time.sleep(cnt**2 * 0.1)
            print("Database read-only, attempting re-connect")


_open()


def re_open(defaultdbfname="minermgr.db"):
    global _conn, dbfname
    if _conn:
        _conn.close()
    _open(defaultdbfname)


def build_db(dbfilename, recreate=False):
    global _conn, dbfname
    if dbfilename == dbfname:
        _conn.close()
    # builds an empty database file
    if recreate:
        try:
            os.unlink(dbfilename)
        except:  # noqa: E722
            pass
    c = apsw.Connection(dbfilename)
    c.pragma("foreign_keys", True)
    c.row_trace = apsw.ext.DataClassRowFactory()

    for fname in importlib.resources.files('db').iterdir():
        if not str(fname).endswith('.sql'):
            continue
        with open(fname, 'r') as f:
            sql = f.read()
            c.execute(sql)
    if dbfilename == dbfname:
        _conn = apsw.Connection(dbfname)
        _conn.pragma("foreign_keys", True)
        _conn.row_trace = apsw.ext.DataClassRowFactory()
    return c


def import_sql(sqlfile, c=_conn):
    c.pragma("foreign_keys", False)
    tc = 0
    for r in c.execute('PRAGMA table_list;'):
        tc += 1
    if tc < 3:
        c = build_db(dbfname)
        c.pragma("foreign_keys", False)
        c.row_trace = apsw.ext.DataClassRowFactory()

    # This assumes the input file fits in memory
    with open(sqlfile, 'r') as f:
        sqls = f.read()
        # this assumes no embedded semicolons
        for q in sqls.split(';'):
            c.execute(q)
    c.pragma("foreign_keys", True)


def load_db(sqlfile, dbfilename, recreate=False):
    c = build_db(dbfilename, recreate=recreate)
    c.row_trace = apsw.ext.DataClassRowFactory()
    import_sql(sqlfile, c=c)
    return c


def set_conn(c):
    global _conn
    _conn.close()
    _conn = c


def conn():
    global _conn
    return _conn


def set_max_attempts(n):
    global _max_q_attempts
    _max_q_attempts = n


def query(*args):
    global _max_q_attempts
    n_attempts = 0
    while n_attempts < _max_q_attempts:
        try:
            rv = conn().execute(*args)
            return rv
        except apsw.BusyError:
            n_attempts += 1
            sleeptime = n_attempts**2 * 0.1
            if sleeptime > 5:
                simplog(f"DB busy after {n_attempts} tries, sleeping {sleeptime} seconds")  # noqa: E501
            time.sleep(sleeptime)
        except apsw.ReadOnlyError:
            n_attempts += 1
            time.sleep(n_attempts**2 * 0.1)
            re_open(dbfname)
    raise Exception(f"DB Busy after {n_attempts} tries at running: {args[0]}")


def qexec(*args):
    global _max_q_attempts, dbfname
    n_attempts = 0
    while n_attempts < _max_q_attempts:
        try:
            conn().execute("BEGIN IMMEDIATE;")
            conn().execute(*args)
            conn().execute("COMMIT;")
            return
        except apsw.BusyError:
            n_attempts += 1
            time.sleep(n_attempts**2 * 0.1)
        except apsw.ReadOnlyError:
            n_attempts += 1
            time.sleep(n_attempts**2 * 0.1)
            re_open(dbfname)
    raise Exception(f"DB Busy after {n_attempts} tries at running: {args[0]}")


def create_backup(destfname):
    destination = apsw.Connection(destfname)

    # Copy into destination
    with destination.backup("main", _conn, "main") as backup:
        while not backup.done:
            backup.step(7)  # copy up to 7 pages each time


def create_export(destfname):
    import model
    with open(destfname, 'w') as f:
        f.write("BEGIN;")
        for tname in model.__all__:
            mod = importlib.import_module(f"model.{tname.lower()}")
            cls = getattr(mod, tname.capitalize())
            cls.export_to_sql(f)
        f.write("COMMIT;")



