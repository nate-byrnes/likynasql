import pytest
import os


@pytest.fixture
def fx_load_db(request):
    from SQL import load_db, set_conn, conn
    old_conn = conn()
    from uuid import uuid4
    fname = uuid4().hex
    try:
        c = load_db(request.param, f'/tmp/{fname}.db')
        os.environ['TMMDBFILE'] = f'/tmp/{fname}.db'
        set_conn(c)

        yield f'/tmp/{fname}.db'
    except:  # noqa: E722
        pass
    finally:
        set_conn(old_conn)
        os.unlink(f'/tmp/{fname}.db')
        os.unlink(f'/tmp/{fname}.db-shm')
        os.unlink(f'/tmp/{fname}.db-wal')


@pytest.fixture(scope='function')
def use_test_db():
    os.environ["TMMDBFILE"] = "test/test.db"
    yield
    from model.threshold import Threshold
    Threshold.delete()
    from model.metric import Metric
    Metric.delete()
