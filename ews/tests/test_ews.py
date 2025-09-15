#
# Author: Rohtash Lakra
#
from tests.base import AbstractTestCase


class EWSTest(AbstractTestCase):

    def test_ews(self):
        """Tests the Models object"""
        print("+test_ews()")
        # valid object and expected results
        test = EWSTest()
        self.assertTrue(isinstance(test, AbstractTestCase))
        self.assertTrue(issubclass(EWSTest, object))
        self.assertFalse(issubclass(object, EWSTest))
        print("-test_ews()")
        print()
