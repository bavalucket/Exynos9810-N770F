from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class Image:
    name: str
    stage: str | None = "st2"
    update_header: bool = False
    no_crc: bool = False
    ree: bool = False
    split: tuple["Image", ...] = ()
    crypt: Callable[[str, bool], None] | None = None

@dataclass(frozen=True)
class SoC:
    signing_type: int
    odin: tuple[Image, ...]
