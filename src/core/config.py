# dataclasses
from dataclasses import dataclass


@dataclass
class Config:
    prefix: str = "$"
    env: str = "dev"
