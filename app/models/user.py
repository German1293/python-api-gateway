from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    hashed_password: str
    is_active: bool = True
    full_name: Optional[str] = None

