from typing import Iterator, Any
from enum import Enum


def get_enum_members_values(cls: type[Enum] | Enum) -> Iterator[Any]:
    return list(map(lambda member: member.value, cls.__members__.values()))
