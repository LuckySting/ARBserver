import uvloop
import abc
from typing import List, Callable
from starlette.applications import Starlette
from starlette.routing import Route


class IServer(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def create_server(cls, routes: List[Route], on_startup: List[Callable], on_shutdown: List[Callable]) -> Starlette:
        """
        Server fabric method
        :param routes: routes list for starlette app
        :param on_startup: startup events for starlette app
        :param on_shutdown: shutdown events for starlette app
        :return: Starlette app
        """
        pass


class UVLoopServer(IServer):

    @classmethod
    def create_server(cls, routes: List[Route], on_startup: List[Callable], on_shutdown: List[Callable]) -> Starlette:
        uvloop.install()
        return Starlette(routes=routes, on_startup=on_startup, on_shutdown=on_shutdown)
