from enum import IntEnum, unique


@unique
class Flags(IntEnum):
    READ = 1 << 0  # bit 0
    WRITE = 1 << 1  # bit 1
    EXECUTE = 1 << 2  # bit 2
    DELETE = 1 << 3  # bit 3
    # Use int64 size for DB compatibility


class BitMask:
    def __init__(self, value=0):
        self.value = value

    def set_flag(self, flag: Flags):
        self.value |= flag

    def clear_flag(self, flag: Flags):
        self.value &= ~flag

    def has_flag(self, flag: Flags) -> bool:
        return (self.value & flag) == flag

    def __int__(self):
        return self.value

    def __repr__(self):
        active_flags = [flag.name for flag in Flags if self.has_flag(flag)]
        return f"<BitMask {self.value} Flags: {active_flags}>"


# Uso
mask = BitMask()
mask.set_flag(Flags.READ)
mask.set_flag(Flags.EXECUTE)
print(mask)  # <BitMask 3 Flags: ['READ', 'WRITE']>

print(mask.has_flag(Flags.EXECUTE))  # False

mask.clear_flag(Flags.READ)
print(mask)  # <BitMask 2 Flags: ['WRITE']>
