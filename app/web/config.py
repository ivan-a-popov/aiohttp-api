import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class Config:
    username: str
    password: str
    db_name: str
    db_host: str


def setup_config(app: "Application"):
    with open("config/config.yaml", "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        username=raw_config["credentials"]["username"],
        password=raw_config["credentials"]["password"],
        db_name=raw_config["credentials"]["db_name"],
        db_host=raw_config["credentials"]["db_host"],
    )
