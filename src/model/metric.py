from model._base import _Base
from SQL import query


class Metric(_Base):
    @classmethod
    def getByName(cls, name):
        qry = """
            SELECT id
            FROM metric
            WHERE name = ?;
        """
        res = query(qry, (name,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return None

    @classmethod
    def getSince(cls, epoch):
        qry = """
            SELECT id
            FROM metric
            WHERE last_updated_unix > ?;
        """
        rv = []
        res = query(qry, (epoch,))
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv

    @classmethod
    def getByNameWithThreshold(cls, name):
        qry = """
            SELECT id
            FROM metric AS m
            JOIN threshold AS t
            on m.id = t.id
            WHERE name = ?;
        """
        res = query(qry, (name,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return None

    @classmethod
    def getWithThreshold(cls):
        qry = """
            SELECT m.id
            FROM metric AS m
            JOIN threshold AS t
            on m.id = t.id;
        """
        res = query(qry)
        rv = []
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv
