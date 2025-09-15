#
# Author: Rohtash Lakra
#
import logging

from framework.utils import Utils
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UtilsTest(AbstractTestCase):

    def test_randomUUID(self):
        logger.debug("+test_randomUUID()")
        uuid = Utils.randomUUID()
        logger.debug(f"uuid={uuid}")
        self.assertIsNotNone(uuid)
        logger.debug("-test_randomUUID()")
        print()

    def test_stackTrace(self):
        logger.debug("+test_stackTrace()")
        error = ValueError('validation error message!')
        stackTrace = Utils.stackTrace(error)
        print(f"stackTrace={stackTrace}")
        self.assertIsNotNone(stackTrace)
        logger.debug("-test_stackTrace()")
        print()

    def test_exception(self):
        logger.debug("+test_exception()")
        try:
            raise Utils.exception(ValueError, 'A validation error message!')
        except ValueError as ex:
            print(f"ex={ex}")
            self.assertIsNotNone(ex)
        logger.debug("-test_exception()")
        print()

    def test_camelCaseToSnakeCase(self):
        logger.debug("+test_camelCaseToSnakeCase()")

        def check(lower_cc, upper_cc, correct):
            x1 = Utils.camelCaseToSnakeCase(lower_cc)
            x2 = Utils.camelCaseToSnakeCase(upper_cc)
            assert correct == x1
            assert correct == x2

            y1 = Utils.snakeCaseToCamelCase(x1, True)
            y2 = Utils.snakeCaseToCamelCase(x2, False)
            assert upper_cc == y1
            assert lower_cc == y2

        examples = [('foo', 'Foo', 'foo'),
                    ('fooBar', 'FooBar', 'foo_bar'),
                    ('fooBarBaz', 'FooBarBaz', 'foo_bar_baz'),
                    ('fOO', 'FOO', 'f_o_o'),
                    ('rohtashLakra', 'RohtashLakra', 'rohtash_lakra')]

        for a, b, c in examples:
            check(a, b, c)
        logger.debug("-test_camelCaseToSnakeCase()")
        print()

    def test_measure_ttfb(self):
        logger.debug("+test_measure_ttfb()")
        url = "https://www.google.com/"
        ttfb = Utils.measure_ttfb(url)
        print(f"TTFB for {url}: {ttfb:.2f} ms, {ttfb / 1000:.2f} seconds")
        self.assertIsNotNone(ttfb)
        self.assertGreaterEqual(ttfb, 1)
        logger.debug("-test_measure_ttfb()")
        print()
