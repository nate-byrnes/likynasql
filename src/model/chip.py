from model._base import _Base
from SQL import query


class Chip(_Base):
    _orderBy = 'ORDER BY slot'

    @classmethod
    def get(cls, id=None):
        """
        Overridden to fetch the Carrier for each Chip
        """
        from model.carrier import Carrier
        instances = super(Chip, cls).get(id=id)
        if id is not None and type(instances) is not list:
            instances = [instances]
        for inst in instances:
            c = Carrier.get(id=(inst.carrier_id,))
            if type(c) is list and c:
                c = c[0]
            if c:
                inst._carrier = c
        return instances

    @classmethod
    def getByDNA(cls, dna):
        qry = """
            SELECT id
            FROM chip
            WHERE dna = ?;
        """
        res = query(qry, (dna,))
        for r in res:
            rv = cls.get((r.id,))
            return rv
        return []
