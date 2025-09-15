#
# Author: Rohtash Lakra
#
import logging

from framework.orm.pydantic.entity import AbstractEntity, BaseEntity, NamedEntity
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class TestPydanticEntity(AbstractTestCase):

    def test_abstract_entity(self):
        """Tests an AbstractEntity object"""
        logger.debug("+test_abstract_entity()")
        abstractEntity = AbstractEntity()
        logger.debug(f"abstractEntity={abstractEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(abstractEntity, AbstractEntity))
        self.assertFalse(isinstance(abstractEntity, TestPydanticEntity))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))

        logger.debug("-test_abstract_entity()")
        print()

    def test_base_entity(self):
        """Tests an AbstractEntity object"""
        logger.debug("+test_base_entity()")
        baseEntity = BaseEntity(id=1)
        logger.debug(f"baseEntity={baseEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(baseEntity, BaseEntity))
        self.assertFalse(isinstance(baseEntity, TestPydanticEntity))
        self.assertTrue(issubclass(BaseEntity, object))
        self.assertFalse(issubclass(object, BaseEntity))

        logger.debug("-test_base_entity()")
        print()

    def test_named_entity(self):
        """Tests an AbstractEntity object"""
        logger.debug("+test_named_entity()")
        namedEntity = NamedEntity(id=100, name="Roh")
        logger.debug(f"namedEntity={namedEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(namedEntity, NamedEntity))
        self.assertFalse(isinstance(namedEntity, TestPydanticEntity))
        self.assertTrue(issubclass(NamedEntity, object))
        self.assertFalse(issubclass(object, NamedEntity))

        logger.debug("-test_named_entity()")
        print()
