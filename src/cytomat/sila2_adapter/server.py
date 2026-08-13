import logging
import signal
import threading
import uuid
from importlib import resources

from cytomat import Cytomat

logger = logging.getLogger(__name__)


def _server_uuid(*, host: str, port: int, serial_port: str) -> uuid.UUID:
    seed = f"differential.bio/open-cytomat/{host}:{port}/{serial_port}"
    return uuid.uuid5(uuid.NAMESPACE_URL, seed)


def _read_packaged_tls_asset(filename: str) -> bytes:
    asset = resources.files("cytomat.sila2_adapter") / "certs" / filename
    with asset.open("rb") as handle:
        return handle.read()


def serve(
    *,
    cytomat: Cytomat,
    host: str,
    port: int,
    insecure: bool,
    serial_port: str,
) -> None:
    from sila2.server import SilaServer

    from cytomat.sila2_adapter.features import FEATURE_BINDINGS

    server = SilaServer(
        server_name="Cytomat Server",
        server_type="CytomatServer",
        server_description="SiLA2 server for open-cytomat plate movement commands.",
        server_version="0.1.0",
        server_vendor_url="https://differential.bio",
        server_uuid=_server_uuid(host=host, port=port, serial_port=serial_port),
    )

    for feature, impl in FEATURE_BINDINGS:
        server.set_feature_implementation(feature, impl(server, cytomat))

    stop_requested = threading.Event()

    def _handle_signal(signum: int, _frame: object) -> None:
        logger.info(f"Shutdown signal received: {signum}")
        stop_requested.set()

    previous_sigint = signal.getsignal(signal.SIGINT)
    previous_sigterm = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    logger.info(f"Starting Cytomat SiLA server on {host}:{port}")
    try:
        if insecure:
            server.start_insecure(host, port, enable_discovery=True)
        else:
            private_key = _read_packaged_tls_asset("server.key")
            cert_chain = _read_packaged_tls_asset("server.crt")
            server.start(
                host,
                port,
                private_key=private_key,
                cert_chain=cert_chain,
                enable_discovery=True,
            )

        while not stop_requested.wait(0.5):
            pass
    except KeyboardInterrupt:
        stop_requested.set()
    finally:
        signal.signal(signal.SIGINT, previous_sigint)
        signal.signal(signal.SIGTERM, previous_sigterm)
        if server.running:
            logger.info("Stopping Cytomat SiLA server...")
            server.stop(grace_period=2)
        cytomat.serial_port.close()
