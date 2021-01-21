import uvloop
import abc
import logging
from typing import List, Callable
from os.path import dirname, join
from graphene import Schema
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route, Mount
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.staticfiles import StaticFiles

logger = logging.getLogger(__name__)


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


class IGraphQLServer(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], schema: Schema) -> Starlette:
        """
        Server fabric method
        :param schema: GraphQL schema for starlette app
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
        logger.info('uvloop install')
        return Starlette(routes=routes, on_startup=on_startup, on_shutdown=on_shutdown)


class BasicServer(IServer):

    @classmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], routes=None) -> Starlette:
        if routes is None:
            routes = []
        return Starlette(routes=routes, on_startup=on_startup, on_shutdown=on_shutdown)


class HelloServer(UVLoopServer):

    @classmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], routes=None) -> Starlette:
        async def hello(request: Request) -> Response:
            return JSONResponse({'hello': 'world'})

        logger.info('Creating HelloServer')
        return super().create_server(on_startup, on_shutdown, [Route('/', hello)])


class GraphQLServer(IGraphQLServer):
    @classmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], schema: Schema) -> Starlette:
        staticfiles_app = cls._get_static_files_app()
        graphql_route = Route('/', GraphQLApp(schema=schema, executor_class=AsyncioExecutor))
        logger.info('Creating GraphQLServer')
        return UVLoopServer.create_server(on_startup, on_shutdown, routes=[staticfiles_app, graphql_route])

    @classmethod
    def _get_static_files_app(cls) -> Mount:
        project_dir = dirname(dirname(dirname(__file__)))
        static_dir = join(project_dir, 'static')
        staticfiles_app = Mount('/static', app=StaticFiles(directory=static_dir), name="static")
        return staticfiles_app


class TestServer(IGraphQLServer):
    @classmethod
    def create_server(cls, on_startup: List[Callable], on_shutdown: List[Callable], schema: Schema) -> Starlette:
        staticfiles_app = cls._get_static_files_app()
        graphql_route = Route('/', GraphQLApp(schema=schema, executor_class=AsyncioExecutor))
        logger.info('Creating TestServer')
        return BasicServer.create_server(on_startup, on_shutdown, routes=[staticfiles_app, graphql_route])

    @classmethod
    def _get_static_files_app(cls) -> Mount:
        project_dir = dirname(dirname(dirname(__file__)))
        static_dir = join(project_dir, 'static')
        staticfiles_app = Mount('/static', app=StaticFiles(directory=static_dir), name="static")
        return staticfiles_app
