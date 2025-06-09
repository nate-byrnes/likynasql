from model._base import _Base
from SQL import query, qexec


class Alert(_Base):
    def put(self):
        """
        store this instance in the database.

        override default behavior of updating if ID is set.

        put will always insert.
        """
        qry = """SELECT 1 FROM "alert" WHERE id = ?;"""
        vals = (self.id,)
        res = query(qry, vals)
        if res.fetchall():
            qry = """UPDATE "alert" SET "sent" = ? WHERE "id" = ?;"""
            vals = (self.sent, self.id)
            qexec(qry, vals)
        else:
            qry = """INSERT INTO "alert" ("id", "sent")
            VALUES (?, ?);
            """
            vals = (self.id, self.sent)
            qexec(qry, vals)
