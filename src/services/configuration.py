from jinja2 import Environment, FileSystemLoader

from appconfig import config
from enums import ProtocolType, ProxyServer


class ConfigurationService:
    def __init__(
        self, proxy_server: ProxyServer, templates_path: str = config.TEMPLATES_PATH
    ):
        self.__proxy_server = proxy_server
        self.__templates_path = templates_path

    def __get_template(self):
        env = Environment(loader=FileSystemLoader(self.__templates_path))
        match self.__proxy_server:
            case ProxyServer.haproxy:
                return env.get_template(config.HAPROXY_TEMPLATE_NAME)
            case _:
                raise ValueError(f"Unknown proxy server: {self.__proxy_server}")

    def __get_haproxy_config(self) -> str:
        paths = []
        backends = []
        for service in config.SERVICES:
            for forwarder in service.forwardings:
                paths.append({"backend": service.name, "protocol": forwarder.protocol})
                backends.append(
                    {
                        "name": service.name,
                        "protocol": forwarder.protocol,
                        "port": forwarder.generated_port,
                        "proto_h2": (
                            "proto h2"
                            if forwarder.protocol == ProtocolType.grpc
                            else ""
                        ),
                    }
                )

        return self.__get_template().render(
            timeout_connect=config.HAPROXY_TIMEOUT_CONNECT,
            timeout_client=config.HAPROXY_TIMEOUT_CLIENT,
            timeout_server=config.HAPROXY_TIMEOUT_SERVER,
            paths=paths,
            backends=backends,
        )

    def get_configuration(self) -> str:
        match self.__proxy_server:
            case ProxyServer.haproxy:
                return self.__get_haproxy_config()
            case _:
                raise ValueError(f"Unknown proxy server: {self.__proxy_server}")
