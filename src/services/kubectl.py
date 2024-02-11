import asyncio
import logging
from typing import Callable

from models.services import Service


class Kubectl:
    @staticmethod
    async def __output_callback(line: str, output: list):
        logging.info(line)
        if not line.startswith("Warning:"):  # FIXME.
            output.append(line)

    @staticmethod
    async def __read_stream(stream, callback, output):
        while True:
            line = await stream.readline()
            if not line:
                break
            await callback(line.decode().strip(), output)

    async def __execute_command(
        self, command: list[str], output_callback: Callable = __output_callback
    ):
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        output = []  # type: ignore[var-annotated]
        await asyncio.gather(
            self.__read_stream(process.stdout, output_callback, output),
            self.__read_stream(process.stderr, output_callback, output),
        )

        await process.wait()
        return output

    async def __get_pod_name(self, namespace: str, service: str) -> str:
        command = [
            "kubectl",
            "get",
            "pods",
            "-l",
            f"app={service}",
            "-o",
            "name",
            "-n",
            namespace,
        ]
        output = await self.__execute_command(command)
        return output[0]

    async def __forward_port(
        self, namespace: str, pod: str, local_port: int, remote_port: int,
    ) -> None:
        command = [
            "kubectl",
            "port-forward",
            "--address",
            "0.0.0.0",
            "-n",
            namespace,
            pod,
            f"{local_port}:{remote_port}",
        ]
        logging.info(f"Forward {pod} to {local_port}:{remote_port}")
        _ = await self.__execute_command(command)

    async def forward_ports(self, services: list[Service]) -> None:
        tasks = []
        for service in services:
            for namespace in service.namespaces:
                pod_name = await self.__get_pod_name(namespace, service.name)
                tasks.extend(
                    [
                        self.__forward_port(
                            namespace=namespace,
                            pod=pod_name,
                            local_port=forwarding.local_port,
                            remote_port=forwarding.remote_port,
                        )
                        for forwarding in service.forwardings
                    ]
                )
        await asyncio.gather(*tasks)
