from dataclasses import dataclass


@dataclass
class Blob:
    bucket: str
    path: str
