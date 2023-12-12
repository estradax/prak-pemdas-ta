import mysql.connector
from typing import NamedTuple
from mysql.connector.pooling import PooledMySQLConnection

class User(NamedTuple):
    id: str
    name: str
    username: str
    password: str
            
class AppState:
    running = True

    user: User | None = None

    def __init__(self, db: PooledMySQLConnection | mysql.connector.MySQLConnection):
        self.db = db

class BaseHandler:
    def handle(self, _: AppState):
        pass

class Option(NamedTuple):
    name: str
    handler: BaseHandler

class Input(NamedTuple):
    name: str
    type: str

class ExitHandler(BaseHandler):
    def handle(self, app_state):
        app_state.running = False
