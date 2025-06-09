from model._base import _Base


class Cmdseq(_Base):
    _orderBy = 'ORDER BY name'

    @classmethod
    def get(cls, id=None, getCmds=True):
        """
        Overridden to fetch the commands for each Cmdseq
        """
        from model.command import Command
        from model.batch import Batch
        instances = super(Cmdseq, cls).get(id=id)
        if type(instances) is not list:
            instances = [instances]

        """
        **CODE SMELL** geCmds=False prevents cmdseq from pulling in its related commands
        thus introducing possible inconsistent Cmdseq instances
        """
        if not getCmds:
            return instances

        for inst in instances:
            cmds = Command.getForParent(fkcol='cmdseq_id',
                                        fkid=inst.id)
            batches = Batch.getForParent(fkcol='cmdseq_id',
                                         fkid=inst.id,
                                         skipCmdSeq=True)
            if type(cmds) is not list:
                inst.commands = [cmds]
            elif cmds:
                inst.commands = cmds
            if type(batches) is not list:
                inst.batches = batches
            else:
                inst.batches = batches
        return instances
