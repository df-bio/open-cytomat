from cytomat.sila2_adapter import server as server_module


class TestServerModule:
    def test_server_uuid_is_stable_for_same_inputs(self) -> None:
        first = server_module._server_uuid(host="127.0.0.1", port=50052, serial_port="COM1")
        second = server_module._server_uuid(host="127.0.0.1", port=50052, serial_port="COM1")

        assert first == second

    def test_server_uuid_changes_when_inputs_change(self) -> None:
        baseline = server_module._server_uuid(host="127.0.0.1", port=50052, serial_port="COM1")
        different_port = server_module._server_uuid(host="127.0.0.1", port=50053, serial_port="COM1")
        different_serial = server_module._server_uuid(host="127.0.0.1", port=50052, serial_port="COM2")

        assert baseline != different_port
        assert baseline != different_serial
