#
# Author: Rohtash Lakra
#
import json
import logging

from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel, BaseModel, NamedModel, ErrorModel, ResponseModel
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class TestPydanticModel(AbstractTestCase):

    def test_abstract_pydantic_model(self):
        """Tests an AbstractEntity object"""
        logger.debug("+test_abstract_pydantic_model()")
        abstract_model = AbstractModel(id=1)
        logger.debug(f"abstract_model={abstract_model}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_model, AbstractModel))
        self.assertFalse(isinstance(abstract_model, TestPydanticModel))
        self.assertTrue(issubclass(AbstractModel, object))
        self.assertFalse(issubclass(object, AbstractModel))

        logger.debug("-test_abstract_pydantic_model()")
        print()

    def test_getAllFields(self):
        """Tests an getAllFields() method"""
        logger.debug("+test_getAllFields()")
        named_model = NamedModel(id=16, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = ['created_at', 'updated_at', 'id', 'name']
        allFields = named_model.getAllFields()
        logger.debug(f"allFields={allFields}")
        self.assertIsNotNone(allFields)
        self.assertEqual(expected, allFields)

        logger.debug("-test_getAllFields()")
        print()

    def test_getClassFields(self):
        """Tests an getClassFields() method"""
        logger.debug("+test_getClassFields()")
        named_model = NamedModel(id=16, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = ['created_at', 'updated_at', 'id', 'name']
        classFields = NamedModel.getClassFields()
        logger.debug(f"classFields={classFields}")
        self.assertIsNotNone(classFields)
        self.assertEqual(expected, classFields)

        logger.debug("-test_getClassFields()")
        print()

    def test_model_json_schema(self):
        """Tests the model_json_schema() method"""
        logger.debug("+test_model_json_schema()")
        namedModel = NamedModel(id=16, name="Roh")
        logger.debug(f"namedModel={namedModel}")

        # valid object and expected results
        self.assertTrue(isinstance(namedModel, NamedModel))
        self.assertFalse(isinstance(namedModel, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = {"description": "NamedModel used an entity with a property called 'name' in it", "properties": {
            "id": {"anyOf": [{"type": "integer"}, {"type": "null"}], "default": None, "title": "Id"},
            "created_at": {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "default": None,
                           "title": "Created At"},
            "updated_at": {"anyOf": [{"format": "date-time", "type": "string"}, {"type": "null"}], "default": None,
                           "title": "Updated At"}, "name": {"title": "Name", "type": "string"}}, "required": ["name"],
                    "title": "NamedModel", "type": "object"}
        modelJsonSchema = NamedModel.model_json_schema()
        logger.debug(f"modelJsonSchema={modelJsonSchema}")
        logger.debug(f"json -> modelJsonSchema={json.dumps(modelJsonSchema)}")
        self.assertIsNotNone(modelJsonSchema)
        self.assertEqual(expected, modelJsonSchema)

        expected = {'id': 16, 'created_at': None, 'updated_at': None, 'name': 'Roh'}
        modelDump = namedModel.model_dump(mode="json")
        logger.debug(f"modelDump={modelDump}")
        logger.debug(f"json -> modelDump={json.dumps(modelDump)}")
        self.assertIsNotNone(modelDump)
        self.assertEqual(expected, modelDump)

        logger.debug("-test_model_json_schema()")
        print()

    def test_abstract_model(self):
        """Tests an AbstractModel object"""
        logger.debug("+test_abstract_model()")
        abstract_model = BaseModel(id=1)
        logger.debug(f"abstract_model={abstract_model}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_model, BaseModel))
        self.assertFalse(isinstance(abstract_model, TestPydanticModel))
        self.assertTrue(issubclass(BaseModel, object))
        self.assertFalse(issubclass(object, BaseModel))

        logger.debug("-test_abstract_model()")
        print()

    def test_named_model(self):
        """Tests an NamedEntity object"""
        logger.debug("+test_named_model()")
        named_model = NamedModel(id=10, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertEqual(10, named_model.get_id())
        self.assertNotEqual(2, named_model.get_id())

        self.assertTrue(isinstance(named_model, BaseModel))
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, BaseModel))
        self.assertFalse(issubclass(BaseModel, NamedModel))

        logger.debug("-test_named_model()")
        print()

    def test_error_model(self):
        """Tests an ErrorEntity object"""
        logger.debug("+test_error_model()")
        errorModel = ErrorModel.buildError(httpStatus=HTTPStatus.INTERNAL_SERVER_ERROR,
                                           message="Internal Server Error!")
        logger.debug(f"errorModel={errorModel}")

        # valid object and expected results
        self.assertIsNotNone(errorModel)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.statusCode, errorModel.status)
        self.assertEqual("Internal Server Error!", errorModel.message)
        self.assertNotEqual(HTTPStatus.INTERNAL_SERVER_ERROR.message, errorModel.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST, errorModel.status)

        self.assertTrue(isinstance(errorModel, AbstractModel))
        self.assertTrue(isinstance(errorModel, ErrorModel))
        self.assertFalse(isinstance(errorModel, BaseModel))
        self.assertTrue(issubclass(ErrorModel, object))
        self.assertTrue(issubclass(ErrorModel, AbstractModel))
        self.assertFalse(issubclass(AbstractModel, ErrorModel))

        logger.debug("-test_error_model()")
        print()

    def test_models(self):
        """Tests all entities object"""
        logger.debug("+test_models()")
        baseModel = BaseModel(id=100)
        logger.debug(f"baseModel: {baseModel}")
        self.assertEqual(100, baseModel.get_id())
        self.assertNotEqual("Lakra", baseModel.get_id())
        jsonBaseModel = baseModel.to_json()
        logger.debug(f"jsonBaseModel={jsonBaseModel}")
        self.assertEqual(jsonBaseModel, baseModel.to_json())

        namedModel = NamedModel(id=1600, name="R. Lakra")
        logger.debug(f"namedModel: {namedModel}")
        self.assertEqual(1600, namedModel.get_id())
        self.assertEqual("R. Lakra", namedModel.name)
        self.assertNotEqual("Lakra", namedModel.get_id())
        jsonNamedModel = namedModel.to_json()
        logger.debug(f"jsonNamedModel={jsonNamedModel}")
        self.assertEqual(jsonNamedModel, namedModel.to_json())

        # valid object and expected results
        self.assertTrue(isinstance(namedModel, NamedModel))
        self.assertTrue(isinstance(namedModel, BaseModel))
        self.assertFalse(isinstance(namedModel, ErrorModel))
        self.assertFalse(issubclass(object, BaseModel))

        errorModel = ErrorModel.buildError(httpStatus=HTTPStatus.BAD_REQUEST, message="Error")
        logger.debug(f"errorModel={errorModel}")

        # valid object and expected results
        self.assertIsNotNone(errorModel)
        self.assertEqual(HTTPStatus.BAD_REQUEST.statusCode, errorModel.status)
        self.assertEqual("Error", errorModel.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST.message, errorModel.message)
        self.assertNotEqual(HTTPStatus.OK, errorModel.status)

        jsonErrorModel = errorModel.to_json()
        logger.debug(f"jsonErrorModel={jsonErrorModel}")
        logger.debug("-test_models()")
        print()

    def test_response_model_success(self):
        """Tests an ResponseModel object"""
        logger.debug("+test_response_model_success()")
        named_entity = NamedModel(id=1600, name="R. Lakra")
        responseModel = ResponseModel.buildResponse(HTTPStatus.CREATED, named_entity)
        logger.debug(f"responseModel={responseModel}")
        self.assertIsNotNone(responseModel)
        self.assertEqual(HTTPStatus.CREATED.statusCode, responseModel.status)
        self.assertIsNotNone(responseModel.data)
        self.assertIsNone(responseModel.errors)
        self.assertFalse(responseModel.hasError())
        jsonResponseModel = responseModel.to_json()
        self.assertIsNotNone(jsonResponseModel)
        logger.debug(f"jsonResponseModel={jsonResponseModel}")

        # build json response
        response_entity_json = ResponseModel.jsonResponse(HTTPStatus.CREATED, named_entity)
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json={response_entity_json}")
        logger.debug("-test_response_model_success()")
        print()

    def test_response_model_error(self):
        """Tests an ResponseModel object"""
        logger.debug("+test_response_model_error()")
        error_entity = ErrorModel.buildError(httpStatus=HTTPStatus.BAD_REQUEST, message="Error")
        response = ResponseModel.buildResponse(HTTPStatus.BAD_REQUEST, error_entity)
        logger.debug(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.statusCode, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)
        jsonResponse = response.to_json()
        self.assertIsNotNone(jsonResponse)
        logger.debug(f"jsonResponse={jsonResponse}")

        # build json response
        response_entity_json = ResponseModel.jsonResponse(HTTPStatus.BAD_REQUEST, error_entity)
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json={response_entity_json}")
        logger.debug("-test_response_model_error()")
        print()

    def test_build_response_with_critical(self):
        """Tests an ResponseEntity.build_response() object"""
        logger.debug("+test_build_response_with_critical()")

        try:
            named_entity = NamedModel(id=1600, name="R. Lakra")
            raise ValueError("The name should be unique!")
        except ValueError as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, named_entity, exception=ex,
                                                   is_critical=True)

        logger.debug(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.statusCode, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)
        self.assertTrue(len(response.errors) > 0)
        logger.debug(f"response.errors => {response.errors}")
        self.assertEqual("The name should be unique!", response.errors[0].message)

        # build json response
        response_entity_json = response.to_json()
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json: {response_entity_json}")
        logger.debug("-test_build_response_with_critical()")
        print()
