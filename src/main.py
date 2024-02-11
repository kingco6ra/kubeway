import asyncio
import logging

from appconfig import config
from enums import ProxyServer
from services.configuration import ConfigurationService
from services.kubectl import Kubectl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    logging.info("Starting kubeway...")
    proxy_server = ProxyServer(config.PROXY_SERVER)
    configuration_service = ConfigurationService(proxy_server)
    configuration_service.write_configuration_file(config.SERVICES)
    kubectl = Kubectl()
    await kubectl.forward_ports(config.SERVICES)


if __name__ == "__main__":
    asyncio.run(main())
