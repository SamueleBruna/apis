from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Table:
    project: str
    dataset: str
    table_name: str
