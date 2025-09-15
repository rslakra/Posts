import unittest

from framework.enums import BaseEnum, AutoUpperCase, AutoLowerCase, EnvType


class EnumsTest(unittest.TestCase):
    """Unit-tests for Enums"""

    def test_base_enum(self):
        print("test_base_enum")
        self.assertEqual("<enum 'BaseEnum'>", str(BaseEnum))
        print()

    def test_auto_upper_case_enum(self):
        print("test_auto_upper_case_enum")
        self.assertEqual("<enum 'AutoUpperCase'>", str(AutoUpperCase))
        # self.assertEqual(('CONSUMER', 'EXPERT'), AutoUpperCase.names())
        # self.assertEqual(('consumer', 'service_provider'), AutoUpperCase.values())
        # text = 'expert'
        # expected = 'AutoUpperCase <EXPERT=service_provider>'
        # print(f"{text} of_name={AutoUpperCase.of_name(text)}")
        # self.assertEqual(expected, str(AutoUpperCase.of_name(text)))
        # self.assertTrue(AutoUpperCase.equals(AutoUpperCase.EXPERT, text))
        #
        # text = 'service_provider'
        # print(f"{text} of_value={AutoUpperCase.of_value(text)}")
        # self.assertEqual(expected, str(AutoUpperCase.of_value(text)))
        # self.assertTrue(AutoUpperCase.equals(AutoUpperCase.EXPERT, text))
        print()

    def test_auto_lower_case_enum(self):
        print("test_auto_lower_case_enum")
        self.assertEqual("<enum 'AutoLowerCase'>", str(AutoLowerCase))
        print()

    def test_env_type_enum(self):
        print("test_env_type_enum")
        self.assertEqual("<enum 'EnvType'>", str(EnvType))
        print(f"names={EnvType.names()}")
        expected = ('DEV', 'LOCAL', 'PROD', 'QA', 'STAGE', 'TEST', 'UAT')
        self.assertEqual(expected, EnvType.names())
        print(f"values={EnvType.values()}")
        expected = (('development', 'develop', 'dev'), ('local', 'localhost'), ('production', 'live', 'prod'), 'qa',
                    ('staging', 'stage'), ('testing', 'test'), 'uat')
        self.assertEqual(expected, EnvType.values())

        # test name
        text = 'prod'
        print(f"{text} of_name={EnvType.of_name(text)}")
        expected = "EnvType <PROD=('production', 'live', 'prod')>"
        self.assertEqual(expected, str(EnvType.of_name(text)))
        self.assertTrue(EnvType.equals(EnvType.PROD, text))

        # test value
        text = 'production'
        print(f"{text} of_value={EnvType.of_value(text)}")
        expected = "EnvType <PROD=('production', 'live', 'prod')>"
        self.assertEqual(expected, str(EnvType.of_value(text)))
        self.assertTrue(EnvType.equals(EnvType.PROD, text))

        # test env
        env_type = EnvType.get_env_type()
        print(f"env_type={env_type}")
        if env_type is not None:
            self.assertIsNotNone(env_type)

        # test env
        flask_env = EnvType.flask_env()
        print(f"flask_env={flask_env}")
        if flask_env is not None:
            self.assertIsNotNone(flask_env)

        text = 'live'
        print(f"{text} of_value={EnvType.of_value(text)}")
        expected = "EnvType <PROD=('production', 'live', 'prod')>"
        self.assertEqual(expected, str(EnvType.of_value(text)))

    def test_is_development(self):
        print("test_is_development")
        for env_type in EnvType.DEV.value:
            print(f"env_type={env_type}, type={type(env_type)}")
            self.assertTrue(EnvType.is_development(env_type))

    def test_is_local(self):
        print("test_is_local")
        for env_type in EnvType.LOCAL.value:
            self.assertTrue(EnvType.is_local(env_type))

    def test_is_production(self):
        print("test_is_production")
        for env_type in EnvType.PROD.value:
            self.assertTrue(EnvType.is_production(env_type))

    def test_is_qa(self):
        print("test_is_qa")
        self.assertTrue(EnvType.is_qa(EnvType.QA.value))

    def test_is_staging(self):
        print("test_is_staging")
        for env_type in EnvType.STAGE.value:
            self.assertTrue(EnvType.is_staging(env_type))

    def test_is_testing(self):
        print("test_is_testing")
        for env_type in EnvType.TEST.value:
            self.assertTrue(EnvType.is_testing(env_type))

    def test_is_uat(self):
        print("test_is_uat")
        self.assertTrue(EnvType.is_uat(EnvType.UAT.value))


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
