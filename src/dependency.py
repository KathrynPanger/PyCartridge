from typing import NamedTuple


class Dependency(NamedTuple):
    version: str
    constraints: str