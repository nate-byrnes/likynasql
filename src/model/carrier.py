from model._base import _Base
from SQL import query


class Carrier(_Base):
    @classmethod
    def get(cls, id=None):
        """
        Overridden to fetch the arguments for each Command
        """
        from model.chip import Chip
        instances = super(Carrier, cls).get(id=id)
        if id is not None and type(instances) is not list:
            instances = [instances]
        for inst in instances:
            inst.chips = Chip.getForParent(fkcol='carrier_id',
                                           fkid=inst.id)
        return instances

    @classmethod
    def getByIP(cls, ip):
        qry = """
            SELECT id
            FROM carrier
            WHERE ip_addr = ?;
        """
        res = query(qry, (ip,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return []

    @classmethod
    def getBySN(cls, sn):
        qry = """
            SELECT id
            FROM carrier
            WHERE serno = ?;
        """
        res = query(qry, (sn,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return []
