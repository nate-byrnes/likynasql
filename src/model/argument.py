from model._base import _Base
from support.template import process


class Argument(_Base):

    _orderBy = "ORDER BY priority ASC"

    @classmethod
    def getForParent(cls, fkcol=None, fkid=None):
        """
        Overridden to fetch the arguments for each Command
        and to ensure all arguments selectors are populated
        """
        from model.selector import Selector
        instances = super(Argument, cls).getForParent(fkcol, fkid)
        if id is not None and type(instances) is not list:
            instances = [instances]
        for inst in instances:
            inst.selector = Selector.get(id=(inst.selector_id,))
        return instances

    def is_singleton(self):
        """
        Checks to see if this argument's name is IPADDR
        and value is SINGLE. If so, it is a singleton
        argument.
        """
        if self.selector == []:
            return False
        if type(self.selector[0].settings) is not list:
            stg = self.selector[0].settings
            return stg.name == 'IPADDR' and stg.value == 'SINGLE'
        for stg in self.selector[0].settings:
            if stg.name == 'IPADDR' and stg.value == 'SINGLE':
                return True
        return False

    def resolve(self, ip, batch, command):
        """
        given the input IP address, resolve
        to the correct setting in the list of settings
        in the selector.
        """
        rv = [self.argstr]
        if hasattr(self, 'selector'):
            for sel in self.selector:
                rv.append(sel.resolve('IPADDR', ip))
        if self.separator != ' ':
            rv = [self.separator.join(rv)]

        rv = [process(r, ip, batch, command) for r in rv]
        return rv
