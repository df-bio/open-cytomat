class ConvertSteps:
    STEPS_PER_MM_H = 170
    STEPS_PER_MM_X = 2432
    STEPS_PER_MM_SHOVEL = 173
    STEPS_PER_DEG_TURN = 173
    STEPS_PER_MM_TURNTABLE = 1
    STEPS_PER_MM_TS = 1

    @classmethod
    def mm_to_steps_x(cls, mm: float) -> int:
        return round(cls.STEPS_PER_MM_X * mm)

    @classmethod
    def steps_to_mm_x(cls, steps: int) -> float:
        return round(1 / (cls.STEPS_PER_MM_X / steps), 4)

    @classmethod
    def mm_to_steps_h(cls, mm: float) -> int:
        return round(cls.STEPS_PER_MM_H * mm)

    @classmethod
    def steps_to_mm_h(cls, steps: int) -> float:
        return round(1 / (cls.STEPS_PER_MM_H / steps), 4)

    @classmethod
    def mm_to_steps_shovel(cls, mm: float) -> int:
        return round(cls.STEPS_PER_MM_SHOVEL * mm)

    @classmethod
    def steps_to_mm_shovel(cls, steps: int) -> float:
        return round(1 / (cls.STEPS_PER_MM_SHOVEL / steps), 4)

    @classmethod
    def deg_to_steps_turn(cls, deg: float) -> int:
        return round(cls.STEPS_PER_DEG_TURN * deg)

    @classmethod
    def steps_to_deg_turn(cls, steps: int) -> float:
        return round(1 / (cls.STEPS_PER_DEG_TURN / steps), 4)

    @classmethod
    def mm_to_steps_turntable(cls, mm: int) -> int:
        return round(cls.STEPS_PER_MM_TURNTABLE * mm)

    @classmethod
    def mm_to_steps_ts(cls, mm: int) -> int:
        return round(cls.STEPS_PER_MM_TS * mm)
