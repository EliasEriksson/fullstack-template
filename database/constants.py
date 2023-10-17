from __future__ import annotations
from sqlalchemy import text

CASCADE = "CASCADE"

gen_random_uuid = text("gen_random_uuid()")


class Lazy:
    select = "select"
    select_in = "selectin"
    joined = "joined"
    raised = "raise"
    raised_on_sql = "raise_on_sql"
    subquery = "subquery"
    dynamic = "dynamic"

    @classmethod
    def default(cls) -> str:
        return cls.select_in


class Cascades:
    save_update = "save-update"
    refresh_expire = "refresh-expire"
    delete = "delete"
    delete_orphan = "delete-orphan"
    merge = "merge"
    expunge = "expunge"

    @staticmethod
    def join(*cascades: str) -> str:
        return ", ".join({*cascades})

    @classmethod
    def default(cls, *cascades: str) -> str:
        return cls.join(
            cls.save_update,
            cls.delete,
            cls.merge,
            cls.expunge,
            *cascades,
        )
