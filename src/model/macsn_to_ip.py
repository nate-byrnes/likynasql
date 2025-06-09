from model._base import _Base
from SQL import query


class Macsn_to_ip(_Base):
    @classmethod
    def getByMAC(cls, mac):
        qry = """
            SELECT id
            FROM macsn_to_ip
            WHERE mac_addr = ?;
        """
        res = query(qry, (mac,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return []
