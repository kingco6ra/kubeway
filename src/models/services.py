from dataclasses import dataclass, field

from mashumaro.mixins.dict import DataClassDictMixin

from enums import ProtocolType
from utils.ports import get_free_port


@dataclass
class Forwarding:
    protocol: ProtocolType
    port: int
    generated_port: int = field(default_factory=get_free_port)


@dataclass
class Service(DataClassDictMixin):
    name: str
    forwardings: list[Forwarding]
