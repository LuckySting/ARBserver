import uvloop
import abc
from typing import List, Callable
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route


class IServer(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable],
                      routes: List[Route] = None) -> Starlette:
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
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], routes=None) -> Starlette:
        if routes is None:
            routes = []
        uvloop.install()
        return Starlette(routes=routes, on_startup=on_startup, on_shutdown=on_shutdown)


class HelloServer(UVLoopServer):

    @classmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], routes=None) -> Starlette:
        async def hello(request: Request) -> Response:
            return JSONResponse({'hello': 'world'})

        return super().create_server(on_startup, on_shutdown, [Route('/', hello)])
