from model._base import _Base
from SQL import query
from support.ping import pings
from support.log import simplog
import time


class Batch(_Base):
    _validate_ips = True

    @classmethod
    def disable_ip_validation(cls):
        cls._validate_ips = False

    @classmethod
    def enable_ip_validation(cls):
        cls._validate_ips = True

    @classmethod
    def get(cls, id=None):
        """
        Overridden to fetch the arguments for each Command
        """
        from model.carrier import Carrier
        from model.cmdseq import Cmdseq
        if id:
            instances = super(Batch, cls).get(id=id)
        else:
            instances = super(Batch, cls).get()
        if id is not None and type(instances) is not list:
            instances = [instances]
        for inst in instances:
            inst._carriers = Carrier.getForParent(fkcol='batch_id',
                                                  fkid=inst.id)
            if type(inst._carriers) is not list:
                inst._carriers = [inst._carriers]
        for inst in instances:
            if hasattr(inst, 'cmdseq_id'):
                inst._cmdseq = Cmdseq.get(id=(inst.cmdseq_id,))[0]
        if len(instances) == 1:
            return instances[0]
        return instances

    @classmethod
    def getForParent(cls, fkcol, fkid, skipCmdSeq=False):
        from model.carrier import Carrier
        from model.cmdseq import Cmdseq
        instances = super(Batch, cls).getForParent(fkcol=fkcol,
                                                   fkid=fkid)
        for inst in instances:
            inst._carriers = Carrier.getForParent(fkcol='batch_id',
                                                  fkid=inst.id)
            if type(inst._carriers) is not list:
                inst._carriers = [inst._carriers]
        if not skipCmdSeq:
            for inst in instances:
                inst._cmdseq = Cmdseq.get(id=(inst.cmdseq_id,))[0]
        return instances

    @classmethod
    def getByName(cls, name):
        qry = """
            SELECT id
            FROM batch
            WHERE name like ?1;
        """
        res = query(qry, ('%' + name + '%',))
        rv = []
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate_ips = Batch._validate_ips

    def do_change_status(self, new_status):
        self.status = f'want {new_status}'
        self.put()

    def change_status(self, new_status, timeout):
        tstart = time.time()
        tdelt = None
        while tdelt is None or tdelt < timeout:
            self.refresh()
            if self.status == new_status:
                break
            elif self.status != f'want {new_status}':
                self.do_change_status(new_status)
            time.sleep(0.05)
            tdelt = time.time() - tstart
            if timeout < 0:
                tdelt = None
        return tdelt

    def does_ping(self, ipaddr):
        try:
            if self._validate_ips:
                return pings(ipaddr)
            else:
                return True
        except PermissionError:
            Batch.disable_ip_validation()
            simplog("Ping checking disabled due to insufficent privileges")
            return True

    def get_offline_ips(self):
        if not hasattr(self, '_offline_ips'):
            return []
        else:
            return self._offline_ips

    def get_online_ips(self):
        if not hasattr(self, '_offline_ips'):
            return list([x.ip_addr for x in self._carriers])
        else:
            return list(
                set([x.ip_addr for x in self._carriers]) -
                set(self._offline_ips))

    def get_stat_name(self):
        rv = self.name
        if hasattr(self, '_offline_ips'):
            offs = self.get_offline_ips()
            ons = self.get_online_ips()
            rv += f"[{len(ons)}↑, {len(offs)}↓]"
        return rv

    def get_ips(self, do_ping=True):
        store_offs = False
        if not hasattr(self, '_offline_ips'):
            self._offline_ips = []
            store_offs = True
        rv = []
        for x in self._carriers:
            if self.does_ping(x.ip_addr) or not do_ping:
                rv.append(x.ip_addr)
                if x.ip_addr in self._offline_ips and do_ping:
                    self._offline_ips.remove(x.ip_addr)
            elif store_offs:
                self._offline_ips.append(x.ip_addr)
        return rv

    @classmethod
    def getWanters(cls):
        qry = """
            SELECT id
            FROM batch
            WHERE status like 'want %';
        """
        res = query(qry)
        rv = []
        for r in res:
            rv.append(cls.get((r.id,)))
        return rv
