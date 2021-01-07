from starlette.applications import Starlette
from app.lib.server import HelloServer
from app.lib.db import Database


def create_app() -> Starlette:
    app = HelloServer.create_server([Database.init_db], [Database.shutdown_db])
    return app
