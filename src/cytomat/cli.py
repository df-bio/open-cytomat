import inspect
import logging
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from cytomat.climate_controller import ClimateController
from cytomat.config import default_config_file, load_config, save_config
from cytomat.cytomat import Cytomat
from cytomat.maintenance_controller import MaintenanceController
from cytomat.plate_handler import PlateHandler
from cytomat.serial_port import usable_serial_ports
from cytomat.shaker_controller import ShakerController

ControllerSpec = tuple[str, str, str, type[Any]]
CONTROLLERS: tuple[ControllerSpec, ...] = (
    ("plate-handler", "plate_handler", "ph", PlateHandler),
    ("maintenance-controller", "maintenance_controller", "mc", MaintenanceController),
    ("climate-controller", "climate_controller", "cc", ClimateController),
    ("shaker-controller", "shaker_controller", "sc", ShakerController),
)

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

COMMAND_ALIASES: dict[str, dict[str, str]] = {
    "plate-handler": {
        "open-transfer-door": "door-open",
        "close-transfer-door": "door-close",
        "initialize": "init",
    }
}


class AliasedGroup(click.Group):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._alias_to_primary: dict[str, str] = {}

    def add_alias(self, primary: str, alias: str) -> None:
        self._alias_to_primary[alias] = primary

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        resolved = self._alias_to_primary.get(cmd_name, cmd_name)
        return super().get_command(ctx, resolved)

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        rows: list[tuple[str, str]] = []
        aliases_by_primary: dict[str, list[str]] = defaultdict(list)
        for alias, primary in self._alias_to_primary.items():
            aliases_by_primary[primary].append(alias)

        for subcommand in self.list_commands(ctx):
            command = self.get_command(ctx, subcommand)
            if command is None or command.hidden:
                continue
            aliases = sorted(aliases_by_primary.get(subcommand, []))
            label = subcommand if not aliases else f"{subcommand} [{', '.join(aliases)}]"
            rows.append((label, command.get_short_help_str()))

        if rows:
            with formatter.section("Commands"):
                formatter.write_dl(rows)


@click.group(cls=AliasedGroup)
@click.option(
    "--serial-port",
    type=str,
    default=None,
    help="Serial port. If omitted, COM_port is read from --config-file/--config, then auto-detected when exactly one usable port is available.",
)
@click.option(
    "--config-file",
    "--config",
    "config_file",
    type=click.Path(path_type=Path, dir_okay=False),
    default=default_config_file,
    show_default=True,
    help="Path to JSON config file.",
)
@click.option(
    "--log-level",
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default="INFO",
    show_default=True,
    help="Root logger level.",
)
@click.pass_context
def main(ctx: click.Context, serial_port: str | None, config_file: Path, log_level: str) -> None:
    """Command line interface for open-cytomat."""
    state = ctx.ensure_object(dict)
    state["config_file"] = config_file
    state["log_level"] = log_level.upper()
    if ctx.resilient_parsing:
        return
    logging.basicConfig(
        level=getattr(logging, state["log_level"]),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    state["serial_port_option"] = serial_port


@main.group("action", cls=AliasedGroup)
def action() -> None:
    """Run controller actions or initialize CLI config."""


main.add_alias("action", "a")


@main.group("sila", cls=AliasedGroup)
def sila() -> None:
    """SiLA server commands."""


main.add_alias("sila", "s")


@sila.command("serve")
@click.option("--host", type=str, default="0.0.0.0")
@click.option("--port", type=int, default=50052)
@click.option("--insecure", is_flag=True, default=False, help="Use insecure transport.")
def sila_serve(host: str, port: int, insecure: bool) -> None:
    """Serve the Cytomat SiLA2 server."""
    from cytomat.sila2_adapter import server as sila_server

    state = click.get_current_context().find_root().obj
    serial_port = _get_serial_port(state)
    cytomat = Cytomat(serial_port)
    sila_server.serve(
        cytomat=cytomat,
        host=host,
        port=port,
        insecure=insecure,
        serial_port=serial_port,
    )


@action.command("initialize")
def initialize_config() -> None:
    """Initialize/update config JSON with COM_port."""
    state = click.get_current_context().find_root().obj
    config_file = state["config_file"]
    config = load_config(config_file)
    config.com_port = _get_serial_port(state)
    target = save_config(config, config_file)
    click.echo(f"Saved config: {target}")
    click.echo(f"COM_port={config.com_port}")


action.add_alias("initialize", "init")


def _get_serial_port(state: dict[str, Any]) -> str:
    if "serial_port" not in state:
        state["serial_port"] = _resolve_serial_port(
            serial_port=state.get("serial_port_option"),
            config_file=state["config_file"],
        )
    return state["serial_port"]


def _resolve_serial_port(*, serial_port: str | None, config_file: Path) -> str:
    if serial_port:
        return serial_port

    configured_port = load_config(config_file).com_port
    if configured_port:
        return configured_port

    discovered_ports = usable_serial_ports()
    if len(discovered_ports) == 1:
        detected_port = discovered_ports[0]
        click.echo(f"Auto-detected serial port: {detected_port}", err=True)
        return detected_port

    if not discovered_ports:
        raise click.UsageError(
            "No serial port configured and no usable serial ports were auto-detected. "
            "Pass --serial-port at the root command, or set COM_port in config first."
        )

    raise click.UsageError(
        "Multiple usable serial ports found: "
        f"{', '.join(discovered_ports)}. "
        "Pass --serial-port at the root command, or set COM_port in config first."
    )


def _kebab(name: str) -> str:
    return name.replace("_", "-")


def _option_type(parameter: inspect.Parameter) -> click.ParamType | type[Any]:
    annotation = parameter.annotation
    if annotation is inspect._empty:
        return str
    if annotation in (int, float, str):
        return annotation
    if annotation is bool:
        return bool
    return str


def _invoke_factory(controller_attr: str, method_name: str) -> Callable[..., None]:
    def _invoke(**kwargs: Any) -> None:
        ctx = click.get_current_context()
        root = ctx.find_root()
        root.ensure_object(dict)
        state = root.obj
        serial_port = _get_serial_port(state)
        if "cytomat" not in state:
            state["cytomat"] = Cytomat(serial_port)
        cytomat = state["cytomat"]
        controller = getattr(cytomat, controller_attr)
        method = getattr(controller, method_name)
        result = method(**kwargs)
        if result is not None:
            click.echo(result)

    return _invoke


def _register_controller_commands() -> None:
    for group_name, controller_attr, group_alias, controller_cls in CONTROLLERS:
        group = AliasedGroup(group_name)

        for method_name, method in inspect.getmembers(controller_cls, predicate=inspect.isfunction):
            if method_name.startswith("_"):
                continue

            signature = inspect.signature(method)
            params = [
                parameter
                for parameter in signature.parameters.values()
                if parameter.name != "self"
                and parameter.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
            ]

            callback = _invoke_factory(controller_attr, method_name)
            for parameter in reversed(params):
                callback = click.option(
                    f"--{_kebab(parameter.name)}",
                    required=parameter.default is inspect._empty,
                    default=None if parameter.default is inspect._empty else parameter.default,
                    type=_option_type(parameter),
                )(callback)

            command_name = _kebab(method_name)
            command_help = (method.__doc__ or "").strip().splitlines()[0] if method.__doc__ else None
            command = click.command(name=command_name, help=command_help)(callback)
            group.add_command(command)

            alias = COMMAND_ALIASES.get(group_name, {}).get(command_name)
            if alias:
                group.add_alias(command_name, alias)

        action.add_command(group)
        action.add_alias(group_name, group_alias)


_register_controller_commands()


if __name__ == "__main__":
    main()
