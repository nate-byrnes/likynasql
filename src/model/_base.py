from SQL import qexec, query


def exp_prep(val, cdict):
    """
    {
    'type': r.type,
    'required': True if r.notnull == 1 else False,
    'default': r.dflt_value,
    'primarykey': True if r.pk == 1 else False
    }

    val = exp_prep(getattr(r, col), v)
    """
    if val is None:
        return 'NULL'
    if cdict['type'].lower() in ('text', 'char', 'varchar', 'datetime', 'date', 'time'):  # noqa: E501
        return f"'{val}'"
    else:
        return f"{val}"


def resdcrf2dict(resr):
    rv = {}
    for k in dir(resr):
        if not k.startswith('_'):
            rv[k] = getattr(resr, k)
    return rv


def base2vals(inst, skip=[]):
    rv = []
    for i in dir(inst):
        if not callable(getattr(inst, i)) \
                and not i.startswith('_') \
                and i not in skip \
                and type(getattr(inst, i)) is not list:
            rv.append(getattr(inst, i))
    return tuple(rv)


def base2names(inst, skip=[]):
    rv = []
    for i in dir(inst):
        if not callable(getattr(inst, i)) \
                and not i.startswith('_') \
                and i not in skip \
                and type(getattr(inst, i)) is not list:
            rv.append(i)
    return rv


def makeUpdate(inst):
    """
    generate an update statement and argument list
    against a table with the same name as
    the class of the instance, assuming there
    is an ID column and field
    """
    qry = f"UPDATE {inst.__class__.__name__.lower()} SET "
    sets = []
    for cname in base2names(inst, skip=['id']):
        sets.append(f"{cname} = ?")
    qry += ", ".join(sets) + " WHERE id = ?;"

    vals = base2vals(inst, skip=['id'])
    vals += (getattr(inst, 'id'), )
    return qry, tuple(vals)


def makeInsert(inst):
    """
    generate an insert statement and parameter list
    against a table with the same name as the class
    of the provided instance. it is assumed there is
    an autoincrementing ID field which will
    be assigned to the instance.
    """
    qry = f"INSERT INTO {inst.__class__.__name__.lower()} ("
    qry += ", ".join(base2names(inst, skip=['id']))
    qry += ") VALUES ("
    qry += ", ".join(['?' for x in base2names(inst, skip=['id'])])
    qry += ") RETURNING id;"

    vals = base2vals(inst, skip=['id'])
    return qry, tuple(vals)


class _Base:
    _orderBy = ''
    _extraWhere = ''

    @classmethod
    def get(cls, id=None):
        """
        fetch one or all records for the
        subclassed type depending upon whether or not
        id is provided.

        id must be a tuple.
        """
        _fetchOne = f"""
                    SELECT *
                    FROM {cls.__name__.lower()}
                    WHERE id = ?
                    {cls._extraWhere}
                    {cls._orderBy};
                """
        _fetchAll = f"""
                    SELECT *
                    FROM {cls.__name__.lower()}
                    {cls._extraWhere}
                    {cls._orderBy};
                """
        if cls._extraWhere:
            _fetchAll = _fetchAll.replace('AND', 'WHERE')
        if id:
            dat = query(_fetchOne, id)
        else:
            dat = query(_fetchAll)
        rv = []
        for row in dat:
            rd = resdcrf2dict(row)
            c = cls(None, **rd)
            rv.append(c)
        if len(rv) != 1:
            return rv
        else:
            return rv[0]

    def refresh(self):
        q = f"""
            SELECT *
            FROM {self.__class__.__name__.lower()}
            WHERE id = ?
        """
        dat = query(q, (self.id,))
        for x in dat:
            rd = resdcrf2dict(x)
            for k, v in rd.items():
                setattr(self, k, v)
            return
        raise Exception(f"Entry for {self.__class__.__name__} with id: {self.id} deleted by another process")  # noqa: E501

    @classmethod
    def getForParent(cls, fkcol, fkid):
        """
        fetch one or all records for the
        subclassed type depending upon whether or not
        id is provided.

        id must be a tuple.
        """
        _fetchAll = f"""
                    SELECT *
                    FROM {cls.__name__.lower()}
                    WHERE {fkcol} = ?
                    {cls._orderBy};
                """
        dat = query(_fetchAll, (fkid,))
        rv = []
        for row in dat:
            rd = resdcrf2dict(row)
            c = cls(None, **rd)
            rv.append(c)
        return rv

    def put(self):
        """
        store this instance in the database.

        if ID is not set, or is None, insert
        else update
        """
        if hasattr(self, 'id') and self.id is not None:
            qry, vals = makeUpdate(self)
            qexec(qry, vals)
        else:
            qry, vals = makeInsert(self)
            res = query(qry, vals)
            for r in res:
                self.id = r.id

    @classmethod
    def delete(cls, id=None):
        """
        Delete one, or all records from the
        underlying table.
        """
        _deleteOne = f"""
                    DELETE
                    FROM {cls.__name__.lower()}
                    WHERE id = ?;
                """
        _deleteAll = f"""
                    DELETE
                    FROM {cls.__name__.lower()};
                """
        if id:
            qexec(_deleteOne, id)
        else:
            qexec(_deleteAll)

    @classmethod
    def get_columns(cls):
        if not hasattr(cls, '__cols'):
            cls.__cols = {}
            res = query(f"PRAGMA table_info('{cls.__name__.lower()}')")  # noqa: E501
            for r in res:
                cls.__cols[r.name] = {
                    'type': r.type,
                    'required': True if r.notnull == 1 else False,
                    'default': r.dflt_value,
                    'primarykey': True if r.pk == 1 else False
                    }
        return cls.__cols

    @classmethod
    def export_to_sql(cls, file):
        """
        write the insert statement to repopulate this
        table into the passed file handle
        """
        pks = []
        cns = []
        tabname = cls.__name__.lower()
        ins = f"INSERT INTO {tabname} ("
        sel = "SELECT "
        cols = cls.get_columns()
        for c, v in cols.items():
            if v['primarykey']:
                pks.append(c)
            cns.append(c)
        cns = ",".join(cns)
        ins += cns
        ins += ") VALUES "
        sel += cns
        sel += f" FROM {tabname}"
        if pks:
            sel += f" ORDER BY {','.join(pks)}"
        sel += ";"

        firstrow = True
        res = query(sel)
        for r in res:
            rarr = []
            for col, v in cols.items():
                val = exp_prep(getattr(r, col), v)
                rarr.append(val)
            if firstrow:
                ins += f"\n({','.join(rarr)})"
                firstrow = False
            else:
                ins += f",\n({','.join(rarr)})"
            file.write(ins)
            ins = ""
        file.write(";\n")

    @classmethod
    def add_op_arguments(cls, g, op):
        cls.get_columns()
        match op:
            case 'list':
                pass
            case 'describe':
                g.add_argument('-v')
            case 'get':
                g.add_argument('id', help=f"The unique identifier for this {cls.__name__}")  # noqa: E501
            case 'add':
                for nm, md in cls.__cols.items():
                    g.add_argument(f"-{nm}",
                                   required=md['required'],
                                   help=f"a value of type {md['type']}")
            case 'change':
                for nm, md in cls.__cols.items():
                    g.add_argument(f"-{nm}",
                                   required=md['primarykey'],
                                   help=f"a value of type {md['type']}")
            case 'remove':
                for nm, md in cls.__cols.items():
                    if not md['primarykey']:
                        continue
                    g.add_argument(f"-{nm}",
                                   required=md['required'],
                                   help=f"a value of type {md['type']}")
            case 'search':
                for nm, md in cls.__cols.items():
                    if md['primarykey']:
                        continue
                    g.add_argument(f"-{nm}",
                                   required=False,
                                   help=f"a value of type {md['type']}")

    def __init__(self, *args, **kwargs):
        """
        Given an indict of kwargs
        populate this instance with so-named
        attributes

        this allows the data model to be completely
        implied (yes ... implied ...)
        from the database structure
        """
        cols = self.__class__.get_columns()
        for k, v in kwargs.items():
            if k in cols:
                setattr(self, k, v)

    def __repr__(self):
        return ", ".join(
            [f"{k} = {repr(v)}" for k, v in zip(base2names(self), base2vals(self))])  # noqa: E501

    def __str__(self):
        return "\n".join(
            [self.__class__.__name__] +
            [f"\t{k}: {str(v)}" for k, v in zip(base2names(self), base2vals(self))]  # noqa: E501
            )

    def __len__(self):
        """
        **CODE SMELL**
        since _base.get() returns the instance when there is only one...
        """
        return 1
