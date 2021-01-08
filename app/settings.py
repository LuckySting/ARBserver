import abc
from typing import Dict, Union

TORTOISE_ORM_CONFIG = {
    "connections": {"default": "postgres://arb_server:1111@postgres:5432/arb_server_db"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class ISettings(abc.ABC):

    def __init__(self):
        self._init_logger()

    @abc.abstractmethod
    def get_tortoise_orm_config(self) -> Dict[str, Dict[str, Union[str, dict]]]:
        """
        Should return config dict for Tortoise orm
        :return: config dict for Tortoise orm
        """
        pass

    @abc.abstractmethod
    def _init_logger(self) -> None:
        """
        Should init logger
        :return: None
        """
        pass


class Settings(ISettings):
    def __init__(self):
        super().__init__()

    def _init_logger(self) -> None:
        logging.getLogger().handlers.clear()
        logging.basicConfig(
            format='[%(name)s] [%(process)d] [%(levelname)s] %(message)s',
            level=logging.INFO
        )

    def get_tortoise_orm_config(self) -> Dict[str, Dict[str, Union[str, dict]]]:
        return TORTOISE_ORM_CONFIG


current_settings = Settings()
try:
    from .local_settings import *
except ImportError:
    pass
