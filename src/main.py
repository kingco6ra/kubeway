import asyncio
import logging

from appconfig import config
from enums import ProxyServer
from services.configuration import ConfigurationService
from services.kubectl import Kubectl
from utils.file_io import get_services_from_file, write_configuration_file

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    logging.info("Starting kubectl-forwarder...")
    proxy_server = ProxyServer(config.PROXY_SERVER)
    configuration_service = ConfigurationService(proxy_server)
    kubectl = Kubectl(namespace=config.KUBERNETES_NAMESPACE)

    write_configuration_file(
        config.HAPROXY_CONFIG_PATH, configuration_service.get_configuration()
    )

    while True:
        logging.info("Reforward ports.")
        await kubectl.forward_ports()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
