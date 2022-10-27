from dataclasses import dataclass
from typing import Union

@dataclass
class Request:
    path: str
    method: str
    body: Union[dict, str]