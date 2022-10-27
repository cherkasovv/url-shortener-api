from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class Response:
    status: int
    content: Optional[Union[str, dict]] = None