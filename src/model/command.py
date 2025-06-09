from model._base import _Base
from pathlib import Path


class Command(_Base):
    _extraWhere = 'AND enabled'
    _orderBy = 'ORDER BY priority ASC'

    @classmethod
    def get(cls, id=None):
        """
        Overridden to fetch the arguments for each Command
        """
        from model.argument import Argument
        from model.cmdseq import Cmdseq
        instances = super(Command, cls).get(id=id)
        if type(instances) is not list:
            instances = [instances]
        for inst in instances:
            inst.arguments = Argument.getForParent(fkcol='command_id',
                                                   fkid=inst.id)
            """
            **CODE SMELL** geCmds=False prevents cmdseq from pulling in its
            related commands thus introducing possible inconsistent Cmdseq
            instances
            """
            inst.cmdseq = Cmdseq.get(id=(inst.cmdseq_id,), getCmds=False)[0]
        return instances

    @classmethod
    def getForParent(cls, fkcol, fkid):
        from model.argument import Argument
        from model.cmdseq import Cmdseq
        instances = super(Command, cls).getForParent(fkcol=fkcol,
                                                     fkid=fkid)
        for inst in instances:
            inst.arguments = Argument.getForParent(fkcol='command_id',
                                                   fkid=inst.id)
            """
            **CODE SMELL** geCmds=False prevents cmdseq from pulling in its
            related commands thus introducing possible inconsistent Cmdseq
            instances
            """
            inst.cmdseq = Cmdseq.get(id=(inst.cmdseq_id,), getCmds=False)[0]
        return instances

    def use_ssh(self):
        if self.ssh == 1 or (self.cmdseq.overssh and self.ssh != 0):
            return True
        return False

    def ssh_user(self):
        if self.ssh_as is None:
            return self.cmdseq.ssh_as
        return self.ssh_as

    def is_singleton(self):
        singletonmode = False

        if hasattr(self, 'arguments'):
            # look to see if any arguments use singleton IP's ... ?
            for arg in self.arguments:
                if arg.is_singleton():
                    singletonmode = True
                    break
        return singletonmode

    def resolve(self, ips, batch):
        rv = []
        self._ips = ips
        singletonmode = False
        p = Path(self.path).joinpath(Path(self.executable))
        rv.append(str(p.resolve()))

        if hasattr(self, 'arguments'):
            # look to see if any arguments use singleton IP's ... ?
            for arg in self.arguments:
                if arg.is_singleton():
                    # if so, create a command array row for each
                    # IP
                    rv = [[str(p.resolve())] for i in range(len(ips))]
                    singletonmode = True
                    break

            if self.use_ssh():
                singletonmode = True
                rv = list([rv.copy() for x in ips])

            if not singletonmode:
                ips = [",".join(ips)]
                rv = list([rv.copy() for x in ips])

            for r, ip in zip(rv, ips):
                for arg in self.arguments:
                    r.extend(arg.resolve(ip, batch, self))
                if self.use_ssh():
                    r.insert(0, ip)
                if self.static_args:
                    r.append(self.static_args)

        if len(rv) == 1:
            # if there is only one command line to return
            # return it, instead of an array with it as the only
            # element
            rv = rv[0]

        return rv
