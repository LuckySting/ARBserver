import abc
from typing import Dict, Union


class ISettings(abc.ABC):

    @abc.abstractmethod
    def get_tortoise_orm_config(self) -> Dict[str, Dict[str, Union[str, dict]]]:
        pass


class Settings(ISettings):
    def get_tortoise_orm_config(self) -> Dict[str, Dict[str, Union[str, dict]]]:
        return {
            "connections": {"default": "postgres://arb_server:1111@localhost:5432/arb_server_db"},
            "apps": {
                "models": {
                    "models": ["app.models", "aerich.models"],
                    "default_connection": "default",
                },
            },
        }


current_settings = Settings()
try:
    from .local_settings import *
except ImportError:
    pass
