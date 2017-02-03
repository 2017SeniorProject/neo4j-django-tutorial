# -*- coding: utf-8 -*-

from contextlib import contextmanager
from neo4j.v1 import GraphDatabase, basic_auth

__author__ = 'lundberg'


class Neo4jDBSessionManager:
    def __init__(self, uri, username=None, password=None, encrypted=True):
        self.uri = uri
        self.driver = self._get_db_driver(uri, username, password, encrypted)

    def _get_db_driver(self, uri, username=None, password=None, encrypted=True, max_pool_size=50, trust=0):
        """
        :param uri: Bolt uri
        :type uri: str
        :param username: Neo4j username
        :type username: str
        :param password: Neo4j password
        :type password: str
        :param encrypted: Use TLS
        :type encrypted: Boolean
        :param max_pool_size: Maximum number of idle sessions
        :type max_pool_size: Integer
        :param trust: Trust cert on first use (0) or do not accept unknown cert (1)
        :type trust: Integer
        :return: Neo4j driver
        :rtype: neo4j.v1.session.Driver
        """
        return GraphDatabase.driver(uri, auth=basic_auth(username, password), encrypted=encrypted,
                                    max_pool_size=max_pool_size, trust=trust)

    @contextmanager
    def _session(self):
        session = self.driver.session()
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            session.close()
    session = property(_session)

    @contextmanager
    def _transaction(self):
        session = self.driver.session()
        transaction = session.begin_transaction()
        try:
            yield transaction
        except Exception as e:
            transaction.success = False
            raise e
        else:
            transaction.success = True
        finally:
            session.close()
    transaction = property(_transaction)
