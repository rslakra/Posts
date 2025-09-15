import logging
import unittest

from framework.db.connector import createEngine, createDatabase
from framework.orm.sqlalchemy.repository import AbstractRepository, SqlAlchemyRepository

logger = logging.getLogger(__name__)


class RepositoryTest(unittest.TestCase):
    """Unit-tests for Repository classes"""

    def test_abstract_repository(self):
        logger.debug("+test_abstract_repository()")
        expected = "<class 'framework.orm.repository.AbstractRepository'>"
        self.assertEqual(expected, str(AbstractRepository))

        # TypeError: Can't instantiate abstract class AbstractRepository with abstract methods save, save_all

        # repository object
        # engine = createEngine("sqlite:///testPosts.db", True)
        # repository = AbstractRepository(engine)
        # self.assertIsNotNone(repository)
        # logger.debug(repository)
        # expected = 'AbstractRepository <engine=Engine(sqlite:///testPosts.db)>'
        # self.assertEqual(expected, str(repository))
        # self.assertIsNotNone(repository.get_engine())
        # result = repository.save_all(None)
        # self.assertIsNone(result)
        logger.debug("-test_abstract_repository()")

    def test_sql_alchemy_repository(self):
        logger.debug("+test_sql_alchemy_repository()")
        expected = "<class 'framework.orm.sqlalchemy.repository.SqlAlchemyRepository'>"
        self.assertEqual(expected, str(SqlAlchemyRepository))

        # repository object
        engine = createEngine("sqlite:///testPosts.db", True)
        createDatabase(engine)
        repository = SqlAlchemyRepository(engine=engine)
        self.assertIsNotNone(repository)
        logger.debug(repository)
        expected = 'SqlAlchemyRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())
        result = repository.save_all(None)
        self.assertIsNone(result)
        logger.debug("-test_sql_alchemy_repository()")


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
