from pathlib import Path

import pytest

from cytomat.sila2_adapter import server as server_module


class _FakeSerialPort:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class _FakeCytomat:
    def __init__(self, serial_port: str) -> None:
        self.serial_port_name = serial_port
        self.serial_port = _FakeSerialPort()


class TestServerCli:
    def test_parser_has_server_options_group(self) -> None:
        parser = server_module._build_parser()
        group_titles = {group.title for group in parser._action_groups}
        assert "serve/s options" in group_titles

    def test_main_requires_serial_port(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("sys.argv", ["cytomat-sila-server"])
        with pytest.raises(SystemExit) as exc:
            server_module.main()
        assert exc.value.code == 2

    def test_main_builds_server_from_args(self, monkeypatch: pytest.MonkeyPatch) -> None:
        calls: dict[str, object] = {}

        def fake_serve(**kwargs) -> None:
            calls.update(kwargs)

        monkeypatch.setattr(server_module, "Cytomat", _FakeCytomat)
        monkeypatch.setattr(server_module, "serve", fake_serve)
        monkeypatch.setattr(
            "sys.argv",
            [
                "cytomat-sila-server",
                "--serial-port",
                "COM1",
                "--insecure",
                "--host",
                "127.0.0.1",
                "--port",
                "50052",
                "--cert-dir",
                "/tmp/cytomat-certs",
            ],
        )

        server_module.main()

        assert calls["host"] == "127.0.0.1"
        assert calls["port"] == 50052
        assert calls["insecure"] is True
        assert calls["serial_port"] == "COM1"
        assert calls["cert_dir"] == Path("/tmp/cytomat-certs")
        assert calls["cytomat"].serial_port_name == "COM1"
