import os

import pytest

from cytomat import Cytomat

SERIAL_PORT_ENV = "CYTOMAT_SERIAL_PORT"


@pytest.mark.integration
def test_can_connect_to_cytomat() -> None:
    serial_port = os.getenv(SERIAL_PORT_ENV)
    if not serial_port:
        pytest.skip(f"Set {SERIAL_PORT_ENV} to run hardware integration tests")

    cytomat = Cytomat(serial_port)
    assert cytomat is not None
