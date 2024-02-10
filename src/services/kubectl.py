import asyncio
import logging
from typing import Callable

from appconfig import config


class Kubectl:
    def __init__(self, namespace: str):
        self.__namespace = namespace

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

    async def __get_pod_name(self, service: str) -> str:
        command = [
            "kubectl",
            "get",
            "pods",
            "-l",
            f"app={service}",
            "-o",
            "name",
            "-n",
            self.__namespace,
        ]
        output = await self.__execute_command(command)
        return output[0]

    async def __forward_port(
        self,
        pod: str,
        local_port: int,
        remote_port: int,
    ) -> None:
        command = [
            "kubectl",
            "port-forward",
            "--address",
            "0.0.0.0",
            "-n",
            self.__namespace,
            pod,
            f"{local_port}:{remote_port}",
        ]
        logging.info(f"Forward {pod} to {local_port}:{remote_port}")
        _ = await self.__execute_command(command)

    async def forward_ports(self) -> None:
        tasks = []
        for service in config.SERVICES:
            pod_name = await self.__get_pod_name(service.name)

            for location in service.forwardings:
                tasks.append(
                    self.__forward_port(
                        pod=pod_name,
                        local_port=location.generated_port,
                        remote_port=location.port,
                    )
                )
        await asyncio.gather(*tasks)
