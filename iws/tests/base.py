#
# Author: Rohtash Lakra
#
import json
import unittest

from framework.time import timeMillis
from tests import app


class AbstractTestCase(unittest.TestCase):
    """An AbstractTestCase class, whose instances are single test cases.

    By default, the test code itself should be placed in a method named
    'runTest'.

    If the fixture may be used for many test cases, create as
    many test methods as are needed. When instantiating such a TestCase
    subclass, specify in the constructor arguments the name of the test method
    that the instance is to execute.

    Test authors should subclass TestCase for their own tests. Construction
    and deconstruction of the test's environment ('fixture') can be
    implemented by overriding the 'setUp' and 'tearDown' methods respectively.

    If it is necessary to override the __init__ method, the base class
    __init__ method must always be called. It is important that subclasses
    should not change the signature of their __init__ method, since instances
    of the classes are instantiated automatically by parts of the framework
    in order to be run.
    """

    logFileContents = False
    logKeys = False

    @classmethod
    def setUpClass(cls):
        # set app at class level
        cls.app = app
        # update app's config enableTesting=True
        cls.app.config.update({
            "enableTesting": True
        })

        # init client from app's client
        cls.client = app.test_client()

        # load json files
        with open('tests/data/app-configs.json', 'r') as app_config_file:
            # load key/values as options
            options = json.load(app_config_file)
            if cls.logFileContents:
                print(json.dumps(options))

            # store key/values to easy access
            for key, value in options.items():
                exec(f"cls.{key} = value")
                # print(f"{key} = {value}")
                if cls.logKeys:
                    print(key)

    # def setUp(self):
    #     """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
    #     to insert common logic that applies to all the tests in the class"""
    #     print("+setUp()")
    #     self.webApp = WebApp()
    #     self.app = self.webApp.create_app(test_mode=True)
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     print("-setUp()")
    #
    # def tearDown(self):
    #     """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
    #     to insert common logic that applies to all the tests in the class"""
    #     print("+tearDown()")
    #     self.app_context.pop()
    #     self.webApp = None
    #     self.app = None
    #     self.app_context = None
    #     print("-tearDown()")
    #
    # def test_webapp(self):
    #     """Tests the WebApp object"""
    #     print("+test_webapp()")
    #     assert self.app is not None
    #     assert current_app == self.app
    #     # valid object and expected results
    #     print("-test_webapp()")

    def getTestEmail(self, isAdmin: bool = False):
        return f"{'admin' if isAdmin else 'user'}{timeMillis()}@lakra.com"
