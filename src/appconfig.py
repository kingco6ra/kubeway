from dataclasses import dataclass

from models.services import Service
from utils.file_io import read_yaml_file


@dataclass
class AppConfig:
    SERVICES: list[Service]
    CONFIG_PATH: str = "config.yaml"

    PROXY_SERVER: str = "haproxy"
    TEMPLATES_PATH: str = "templates/"

    HAPROXY_CONFIG_PATH: str = "haproxy/haproxy.conf"
    HAPROXY_TEMPLATE_NAME: str = "haproxy.conf.j2"
    HAPROXY_TIMEOUT_CONNECT: int = 1000  # in ms
    HAPROXY_TIMEOUT_CLIENT: int = 1000  # in ms
    HAPROXY_TIMEOUT_SERVER: int = 1000  # in ms

    @classmethod
    def load_from_yaml(cls, file_path: str) -> "AppConfig":
        data = read_yaml_file(file_path)
        print(data)
        if "SERVICES" in data:
            data["SERVICES"] = [
                Service.from_dict(service) for service in data["SERVICES"]
            ]
        return cls(**data)


config = AppConfig.load_from_yaml("config.yaml")
