import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.dialects.postgresql.base import PGInspector
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class SQL:

    def __init__(self, sqluri: str, pool_size=20):
        """
        :param sqluri: 'postgresql://postgres:secret@localhost:5432/twitter'
        """
        self._uri = sqluri
        self.engine = create_engine(
            sqluri,  pool_size=pool_size, max_overflow=0)

        self.inspector: PGInspector = inspect(self.engine)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def list_tables(self):
        return self.inspector.get_tables_names()

    def sessionmaker(self, autocommit=False, autoflush=False):
        """ Session could be used as context manager
        Autocommit will be deprecated in SQLAlchemy 2.0
        Session.begin() method may be used to explicitly start transactions

        :param autoflush: When True, all query operations will issue a Session.
        flush() call to this Session before proceeding. Flush 
        """

        return sessionmaker(bind=self.engine,
                            autocommit=autocommit,
                            autoflush=autoflush
                            )

    def scoped_session(self, autoflush=True) -> Session:
        """ Scoped session return a Session object that could be used 
        with a context manager

        https://docs.sqlalchemy.org/en/14/orm/session_basics.html#opening-and-closing-a-session

        """
        SSession = scoped_session(
            sessionmaker(autoflush=autoflush,
                         bind=self.engine))

        return SSession
