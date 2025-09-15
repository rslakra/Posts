#
# Author: Rohtash Lakra
#
from tests.base import AbstractTestCase


class IWSTest(AbstractTestCase):

    def test_iws(self):
        """Tests the IWS service"""
        print("+test_iws()")
        # valid object and expected results
        test = IWSTest()
        self.assertTrue(isinstance(test, AbstractTestCase))
        self.assertTrue(issubclass(IWSTest, object))
        self.assertFalse(issubclass(object, IWSTest))
        print("-test_iws()")
        print()

