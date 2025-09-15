import logging
import unittest

from framework.datetime import nowMillis
from rest.company.repository import CompanyRepository
from rest.company.schema import CompanySchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class CompanyRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.company.repository.CompanyRepository'>"
        self.assertEqual(expected, str(CompanyRepository))

        # init object
        self.companyRepository = CompanyRepository()
        logger.debug(f"companyRepository={self.companyRepository}")
        self.assertIsNotNone(self.companyRepository)
        expected = 'CompanyRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.companyRepository))
        self.assertIsNotNone(self.companyRepository.get_engine())

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.companyRepository = None
        self.assertIsNone(self.companyRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_company(self):
        logger.debug("+test_create_company()")

        companyName = f"Lakra Inc-{nowMillis()}"
        # company's json
        company_json = {
            "name": companyName
        }

        companySchema = CompanySchema(**company_json)
        logger.debug(f"companySchema={companySchema}")
        self.assertIsNotNone(companySchema)
        # self.assertIsNone(companySchema.branches)

        companySchema = self.companyRepository.save(companySchema)
        logger.debug(f"companySchema={companySchema}")
        self.assertIsNotNone(companySchema)
        # self.assertIsNone(companySchema.branches)
        self.assertIsNotNone(companySchema.id)
        self.assertEqual(companyName, companySchema.name)

        logger.debug("-test_create_company()")
        print()

    def test_create_company_with_branches(self):
        logger.debug("+test_create_company_with_branches()")

        companyName = f"Parent Inc-{nowMillis()}"
        # company's json
        company_json = {
            "name": companyName,
            "branches": [
                {
                    "name": f"Child Inc-{nowMillis()}"
                }
            ]
        }
        companySchema = CompanySchema(**company_json)
        logger.debug(f"companySchema={companySchema}")
        self.assertIsNotNone(companySchema)
        self.assertIsNotNone(companySchema.branches)

        companySchema = self.companyRepository.save(companySchema)
        logger.debug(f"companySchema={companySchema}")
        self.assertIsNotNone(companySchema)
        self.assertIsNotNone(companySchema.branches)
        self.assertIsNotNone(companySchema.id)
        self.assertEqual(companyName, companySchema.name)
        logger.debug("-test_create_company_with_branches()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
