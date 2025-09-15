#
# Author: Rohtash Lakra
#
from tests.base import AbstractTestCase
from framework.orm.pydantic.entity import AbstractEntity, BaseEntity, NamedEntity, ErrorEntity, ErrorResponse


class TestAbstract(AbstractTestCase):

    def test_abstract_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_entity()")
        abstractEntity = AbstractEntity()
        print(f"abstractEntity: {abstractEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(abstractEntity, AbstractEntity))
        self.assertFalse(isinstance(abstractEntity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_abstract_entity()")

    def test_base_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_base_entity()")
        baseEntity = BaseEntity(1)
        print(f"baseEntity: {baseEntity}")

        # valid object and expected results
        self.assertEqual(1, baseEntity.get_id())
        self.assertNotEqual(2, baseEntity.get_id())

        self.assertTrue(isinstance(baseEntity, AbstractEntity))
        self.assertFalse(isinstance(baseEntity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_base_entity()")

    def test_named_entity(self):
        """Tests an NamedEntity object"""
        print("+test_named_entity()")
        namedEntity = NamedEntity(1, "Roh")
        print(f"namedEntity: {namedEntity}")

        # valid object and expected results
        self.assertEqual(1, namedEntity.get_id())
        self.assertNotEqual(2, namedEntity.get_id())

        self.assertTrue(isinstance(namedEntity, AbstractEntity))
        self.assertTrue(isinstance(namedEntity, NamedEntity))
        self.assertFalse(isinstance(namedEntity, TestAbstract))
        self.assertTrue(issubclass(NamedEntity, AbstractEntity))
        self.assertFalse(issubclass(AbstractEntity, NamedEntity))
        print("-test_named_entity()")

    def test_error_entity(self):
        """Tests an ErrorEntity object"""
        print("+test_error_entity()")
        errorEntity = ErrorEntity(200, "Success")
        print(f"errorEntity: {errorEntity}")

        # valid object and expected results
        self.assertEqual(200, errorEntity.status)
        self.assertNotEqual(400, errorEntity.status)
        self.assertEqual("Success", errorEntity.message)
        self.assertIsNone(errorEntity.exception)

        self.assertTrue(isinstance(errorEntity, AbstractEntity))
        self.assertTrue(isinstance(errorEntity, ErrorEntity))
        self.assertFalse(isinstance(errorEntity, BaseEntity))
        self.assertTrue(issubclass(ErrorEntity, object))
        self.assertTrue(issubclass(ErrorEntity, AbstractEntity))
        self.assertFalse(issubclass(ErrorEntity, BaseEntity))
        print("-test_error_entity()")

    def test_entity(self):
        """Tests all entities object"""
        print("+test_entity()")
        entityObject = BaseEntity(100)
        print(f"entityObject: {entityObject}")
        self.assertEqual(100, entityObject.get_id())
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.json()
        print(f"entityObjectJson: \n{entityObjectJson}")
        self.assertEqual(entityObjectJson, entityObject.json())

        entityObject = NamedEntity(1600, "R. Lakra")
        print(f"entityObject: {entityObject}")
        self.assertEqual(1600, entityObject.get_id())
        self.assertEqual("R. Lakra", entityObject.name)
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.json()
        print(f"entityObjectJson: \n{entityObjectJson}")

        # valid object and expected results
        self.assertTrue(isinstance(entityObject, NamedEntity))
        self.assertTrue(isinstance(entityObject, AbstractEntity))
        self.assertFalse(isinstance(entityObject, ErrorEntity))
        self.assertFalse(issubclass(object, AbstractEntity))

        errorEntity = ErrorEntity(400, "Error")
        print(f"errorEntity: {errorEntity}")
        errorEntityJson = errorEntity.json()
        print(f"errorEntityJson: \n{errorEntityJson}")
        print("-test_entity()")

    def test_error_response(self):
        """Tests an ErrorResponse object"""
        print("+test_error_response()")
        errorResponse = ErrorResponse(400, "Invalid Input!")
        print(f"errorResponse: {errorResponse}")
        self.assertIsNotNone(errorResponse)
        self.assertIsNotNone(errorResponse.error)
        self.assertEqual(400, errorResponse.error.status)
        self.assertEqual("Invalid Input!", errorResponse.error.message)
        self.assertIsNone(errorResponse.error.exception)

        errorResponseJson = errorResponse.json()
        print(f"errorResponseJson: \n{errorResponseJson}")
        print("-test_error_response()")
