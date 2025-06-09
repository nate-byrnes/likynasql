from model._base import _Base
from SQL import query


class Ip_to_mac(_Base):
    @classmethod
    def getByIP(cls, ip):
        qry = """
            SELECT id
            FROM ip_to_mac
            WHERE ipaddr = ?;
        """
        res = query(qry, (ip,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return []
