from SQL import query
from model._base import _Base


class Job(_Base):
    @classmethod
    def getNotCompleted(cls):
        qry = """
            SELECT id
            FROM job
            WHERE completed_ts IS NULL
            OR exit_status IS NULL;
        """
        rv = []
        res = query(qry)
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv

    @classmethod
    def getRunningByPID(cls, pid):
        qry = """
            SELECT id
            FROM job
            WHERE (completed_ts IS NULL
            OR exit_status IS NULL)
            AND pid = ?;
        """
        rv = []
        res = query(qry, (pid,))
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv
