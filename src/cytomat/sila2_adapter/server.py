from __future__ import annotations

import argparse
import logging
import signal
import subprocess
import threading
import uuid
from pathlib import Path

from cytomat import Cytomat

HOST = "0.0.0.0"
DEFAULT_PORT = 50052

logger = logging.getLogger(__name__)


def _server_uuid(*, host: str, port: int, serial_port: str) -> uuid.UUID:
    seed = f"differential.bio/open-cytomat/{host}:{port}/{serial_port}"
    return uuid.uuid5(uuid.NAMESPACE_URL, seed)


def _ensure_certs(cert_dir: Path, host: str) -> tuple[bytes, bytes]:
    cert_dir.mkdir(parents=True, exist_ok=True)
    cert_path = cert_dir / "server.crt"
    key_path = cert_dir / "server.key"

    if not cert_path.exists() or not key_path.exists():
        cmd = [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            str(key_path),
            "-out",
            str(cert_path),
            "-days",
            "3650",
            "-subj",
            f"/CN={host}",
        ]
        subprocess.run(cmd, check=True)

    return key_path.read_bytes(), cert_path.read_bytes()


def serve(
    *,
    cytomat: Cytomat,
    host: str,
    port: int,
    insecure: bool,
    cert_dir: Path,
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
            private_key, cert_chain = _ensure_certs(cert_dir, host)
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Cytomat SiLA2 server.")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--insecure", action="store_true", help="Use insecure transport.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument("--serial-port", required=True, help="Serial port (e.g. /dev/ttyUSB0, COM10).")
    parser.add_argument(
        "--cert-dir",
        default="/tmp/open-cytomat/certs",
        help="Directory for generated/loaded TLS certificates when not using --insecure.",
    )
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    cytomat = Cytomat(args.serial_port)
    serve(
        cytomat=cytomat,
        host=args.host,
        port=args.port,
        insecure=args.insecure,
        cert_dir=Path(args.cert_dir),
        serial_port=args.serial_port,
    )
