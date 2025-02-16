# dataclasses
from dataclasses import dataclass


@dataclass
class Config:
    owner_ids: list[int]
    prefix: str = "$"
    env: str = "dev"
