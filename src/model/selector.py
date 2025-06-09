from model._base import _Base


class Selector(_Base):

    @classmethod
    def get(cls, id=None):
        """
        Overridden to fetch the arguments for each Command
        """
        from model.setting import Setting
        instances = super(Selector, cls).get(id=id)
        if id is not None and type(instances) is not list:
            instances = [instances]
        for inst in instances:
            inst.settings = Setting.getForParent(fkcol='selector_id',
                                                 fkid=inst.id)
        return instances

    def resolve(self, attrn, attrv):
        """
        work from highest to lowest priority
        in the list of settings. return the first
        match. (Default is considered a match)
        """
        if type(self.settings) is list:
            for st in self.settings:
                if st.match(attrn, attrv):
                    return st.resolve(attrn, attrv)
        else:
            return self.settings.resolve(attrn, attrv)
