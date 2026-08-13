from __future__ import annotations

from pathlib import Path

from cytomat.config import CytomatConfig, load_config


class Parameters:
    COM_port: str = CytomatConfig().com_port
    steps_per_mm_h: int = 170
    max_steps_h: int = 0
    steps_per_mm_x: int = 2432
    max_steps_x: int = 0
    steps_per_mm_shovel: int = 173
    max_steps_shovel: int = 24000
    steps_per_deg_turn: int = 173
    max_deg_turn: int = 180
    lid_holder_slot: int | None = None
    pipet_station_slot: int = 27
    measurement_slot: int = 6

    @classmethod
    def load(cls, config_file: Path | None = None) -> None:
        config = load_config(config_file)
        cls.COM_port = config.com_port
