from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from app.lib.server import UVLoopServer
from app.lib.db import Database


async def homepage(request):
    return JSONResponse({'hello': 'world'})


def create_app() -> Starlette:
    app = UVLoopServer.create_server([Route('/', homepage)], [Database.init_db], [Database.shutdown_db])
    return app
