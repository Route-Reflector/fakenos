"""
Module tests for compatibility with Docker containers.
"""

# pylint: disable=unused-argument
import os
import subprocess
import time

from netmiko import ConnectHandler
import pytest

IN_GITHUB_ACTIONS: bool = os.getenv("GITHUB_ACTIONS") is not None

fakerouter1 = {
    "device_type": "cisco_ios",
    "host": "localhost",
    "username": "user",
    "password": "user",
    "port": 12723,
}

fakerouter2 = {
    "device_type": "cisco_ios",
    "host": "localhost",
    "username": "user",
    "password": "user",
    "port": 12724,
}


def _skip_docker_tests() -> bool:
    """Return True if Docker tests should be skipped."""
    if IN_GITHUB_ACTIONS:
        return True
    try:
        subprocess.run(
            ["docker", "info"],
            check=True,
            capture_output=True,
        )
        return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        return True


@pytest.fixture
def setup():
    """Starts the docker containers."""
    try:
        subprocess.run(
            ["docker", "compose", "-f", "docker/docker-compose.yaml", "up", "-d"],
            check=True,
        )
        time.sleep(5)
        yield
    finally:
        subprocess.run(
            ["docker", "compose", "-f", "docker/docker-compose.yaml", "down"],
            check=True,
        )


@pytest.mark.skipif(_skip_docker_tests(), reason="Docker is not available or in CI.")
def test_container(setup):
    """
    Test that we can connect to the device and run a command
    in the case that the device is a container.

    Specifically, in this test will connect to a Cisco IOS
    device running in a container and run the command "show clock".
    """
    times_to_collect: int = 100

    device = ConnectHandler(**fakerouter1)

    outputs = [device.send_command("show clock") for _ in range(times_to_collect)]

    assert len(outputs) == times_to_collect
    assert all(isinstance(i, str) for i in outputs)
    assert all("Traceback" not in i for i in outputs)


@pytest.mark.skipif(_skip_docker_tests(), reason="Docker is not available or in CI.")
def test_container_multiple_connections(setup):
    """
    Similar to test_container, but it runs multiple
    connections to the device.
    """
    connections_count = 10
    times_to_collect = 5

    outputs = {"device1": [], "device2": []}

    for _ in range(connections_count):
        device1 = ConnectHandler(**fakerouter1)
        device2 = ConnectHandler(**fakerouter2)

        for _ in range(times_to_collect):
            outputs["device1"].append(device1.send_command("show clock"))
            outputs["device2"].append(device2.send_command("show clock"))

        device1.disconnect()
        device2.disconnect()

    assert len(outputs["device1"]) == connections_count * times_to_collect
    assert all("Traceback" not in i for i in outputs["device1"])
    assert all(isinstance(i, str) for i in outputs["device1"])

    assert len(outputs["device2"]) == connections_count * times_to_collect
    assert all("Traceback" not in i for i in outputs["device2"])
    assert all(isinstance(i, str) for i in outputs["device2"])
