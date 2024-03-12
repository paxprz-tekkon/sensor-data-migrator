from __future__ import annotations
import typing


class DbConnection(typing.Protocol):
    def execute(self, query, values=None) -> DbConnection:
        ...

    def fetchall(self, query, values=None) -> typing.List[typing.Any]:
        ...

    def fetchone(self, query, values=None) -> typing.Any:
        ...

    def fetchval(self, query, values=None) -> typing.Any:
        ...
