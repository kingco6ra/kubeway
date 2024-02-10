from enum import StrEnum, auto


class ProtocolType(StrEnum):
    http = auto()
    grpc = auto()


class ProxyServer(StrEnum):
    haproxy = auto()
