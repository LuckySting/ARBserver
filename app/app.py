from starlette.applications import Starlette
from app.lib.server import GraphQLServer
from app.lib.db import Database
from app.schema import HelloSchema


def create_app() -> Starlette:
    app = GraphQLServer.create_server([Database.init_db], [Database.shutdown_db], HelloSchema.get_schema())
    return app
