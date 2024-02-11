from jinja2 import Environment, FileSystemLoader

from appconfig import config
from enums import ProtocolType, ProxyServer
from models.services import Service
from utils.file_io import write_file


class ConfigurationService:
    def __init__(
        self,
        proxy_server: ProxyServer,
        templates_path: str = config.TEMPLATES_PATH,
    ):
        self.__proxy_server = proxy_server
        self.__templates_path = templates_path
        self.__config_path: str | None = None

    def __get_template(self):
        env = Environment(loader=FileSystemLoader(self.__templates_path))
        match self.__proxy_server:
            case ProxyServer.haproxy:
                return env.get_template(config.HAPROXY_TEMPLATE_NAME)
            case _:
                raise ValueError(f"Unknown proxy server: {self.__proxy_server}")

    def __get_haproxy_config(self, services: list[Service]) -> str:
        backends = [
            {
                "name": service.name,
                "namespace": namespace,
                "protocol": forwarder.protocol,
                "port": forwarder.local_port,
                "proto_h2": (
                    "proto h2" if forwarder.protocol == ProtocolType.grpc else ""
                ),
            }
            for service in services
            for namespace in service.namespaces
            for forwarder in service.forwardings
        ]

        return self.__get_template().render(
            timeout_connect=config.HAPROXY_TIMEOUT_CONNECT,
            timeout_client=config.HAPROXY_TIMEOUT_CLIENT,
            timeout_server=config.HAPROXY_TIMEOUT_SERVER,
            backends=backends,
        )

    def __get_configuration(self, services: list[Service]) -> str:
        match self.__proxy_server:
            case ProxyServer.haproxy:
                self.__config_path = config.HAPROXY_CONFIG_PATH
                return self.__get_haproxy_config(services)
            case _:
                raise ValueError(f"Unknown proxy server: {self.__proxy_server}")

    def write_configuration_file(self, services: list[Service]):
        configuration = self.__get_configuration(services)
        if self.__config_path is None:
            raise RuntimeError("Configuration file not specified.")
        write_file(self.__config_path, configuration)
