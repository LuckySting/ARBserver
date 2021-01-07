import abc
import logging
from tortoise import Tortoise
from app.settings import current_settings

logger = logging.getLogger(__name__)


class IDatabase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def init_db(cls) -> None:
        """
        Database initialization coroutine, must be called before any db action
        """

    @classmethod
    @abc.abstractmethod
    async def shutdown_db(cls) -> None:
        """
        Database shutdown coroutine, must be called before server shutting down
        :return: None
        """


class Database(IDatabase):

    @classmethod
    async def init_db(cls) -> None:
        logger.info('Start database initialization')
        logger.debug('Database configuration: \n' + str(current_settings.get_tortoise_orm_config()))
        await Tortoise.init(config=current_settings.get_tortoise_orm_config())

    @classmethod
    async def shutdown_db(cls) -> None:
        logger.info('Shutting down database')
        await Tortoise.close_connections()
