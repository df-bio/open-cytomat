import pytest
from serial.serialutil import SerialException
from serial.tools import list_ports

from cytomat import Cytomat


def _first_usable_serial_port() -> str | None:
    for port in list_ports.comports():
        try:
            cytomat = Cytomat(port.device)
        except (SerialException, PermissionError):
            continue

        cytomat.serial_port.close()
        return port.device

    return None


@pytest.mark.integration
def test_can_connect_to_cytomat() -> None:
    serial_port = _first_usable_serial_port()
    if serial_port is None:
        pytest.skip("No usable serial port found; skipping hardware integration test")

    cytomat = Cytomat(serial_port)
    assert cytomat is not None
    cytomat.serial_port.close()
