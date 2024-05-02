from dataclasses import dataclass


@dataclass
class Blob:
    project: str
    bucket: str
    path: str
