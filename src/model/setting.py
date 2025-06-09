from model._base import _Base


class Setting(_Base):
    """
    Order by descending such that the higher
    priority settings are first, that way if they
    match, they will be selected. If the priority is negative
    they will be ignored for the default should be higher priority
    """
    _orderBy = "ORDER BY priority DESC"

    def match(self, attrn, attrv):
        if not hasattr(self, 'forattrn') or\
                not hasattr(self, 'forattrv') or\
                self.forattrn is None or\
                self.forattrv is None:
            return True
        else:
            return attrn == self.forattrn and\
                attrv == self.forattrv

    def resolve(self, attrn, attrv):
        if self.name in ('IPADDR', 'IPLIST'):
            return attrv
        return self.value
