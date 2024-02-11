from dataclasses import dataclass, field

from mashumaro.mixins.dict import DataClassDictMixin

from enums import ProtocolType
from utils.ports import get_free_port


@dataclass
class Forwarding:
    protocol: ProtocolType
    remote_port: int
    local_port: int = field(default_factory=get_free_port)


@dataclass
class Service(DataClassDictMixin):
    name: str
    namespaces: list[str]
    forwardings: list[Forwarding]
