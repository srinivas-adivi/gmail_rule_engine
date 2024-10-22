from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database(ABC):
    def __init__(self):
        self.engine = None
        self.session = None

    def connect(self, connection_string):
        self.engine = create_engine(connection_string)
        print(f"{self.__class__.__name__}: {connection_string} connected")

    def create_session(self):
        if not self.session:
            session = sessionmaker(bind=self.engine)
            self.session = session()

        return self.session

    def close(self):
        if self.engine:
            self.engine.dispose()
            print(f"{self.__class__.__name__}: connection closed")

    @abstractmethod
    def get_connection_string(self, config):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class SQLiteDatabase(Database):

    def get_connection_string(self, config):
        # Construct the SQLite connection string using values from config
        database = config.get('database', None)
        if not database:
            ValueError(f"No `database` found in config: {config}")
        return f"sqlite:///{database}"
