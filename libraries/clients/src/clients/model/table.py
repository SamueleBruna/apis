from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Table:

     project: str
     dataset: str
     table_name: str
     # full_name: str
     # fields: List[dict]
     # partition_field: Optional[str] = None
     # num_rows: Optional[int] = None
     # num_bytes: Optional[int] = None
     # self_link : Optional[str] =None