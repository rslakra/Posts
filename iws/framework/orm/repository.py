#
# Author: Rohtash Lakra
#
import logging
from abc import ABC, abstractmethod
from enum import auto
from typing import Iterable, Any, Dict, List, Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from framework.enums import AutoUpperCase

logger = logging.getLogger(__name__)




class EngineType(AutoUpperCase):
    """EngineType class contains various engine types"""

    CLASSICAL = auto()
    SQL_ALCHEMY = auto()


class RepositoryManager(object):
    """RepositoryManager class handles engines based on engine-types"""

    def __init__(self):
        self.engines: dict[EngineType, Engine] = None

    def register_engine(self, engineType: EngineType, engine: Any):
        """Registers the repository for the engine-type"""

        if self.engines is None:
            self.engines = {}

        self.engines[engineType] = engine

    def get_engine(self, engineType: EngineType):
        """Returns the repository's engine for the given type"""
        return self.engines[engineType] if engineType else None

    def remove_engine(self, engineType: EngineType) -> bool:
        """Removes the repository for the given type"""
        if engineType:
            self.engines.pop(engineType)
            return True

        return False

    def execute(self):
        """Executes the repository"""
        pass


class AbstractRepository(ABC):
    """RepositoryManager class handles engines based on engine-types"""

    def __init__(self, engine: Engine):
        super().__init__()
        self.__engine = engine

    @abstractmethod
    def filter(self, filters: Dict[str, Any]) -> List[Optional[Any]]:
        pass

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.__class__.__name__} <engine={self.get_engine()}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)

    def get_engine(self) -> Engine:
        return self.__engine

    @abstractmethod
    def save(self, instance):
        """Saves the instance using context manager"""
        logger.debug(f"+save(), instance={instance}")
        if instance:
            with Session(self.get_engine()) as session:
                try:
                    session.begin()
                    session.add(instance)
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
                    raise ex
                else:
                    session.commit()
                    logger.debug("Persisted a instance successfully!")

        logger.debug(f"-save()")

    @abstractmethod
    def save_all(self, instances: Iterable[object]):
        """Saves the instances using context manager"""
        logger.debug(f"+save_all(), instances={instances}")
        if instances:
            with Session(self.get_engine()) as session:
                try:
                    session.begin()
                    session.add_all(instances)
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
                    raise ex
                else:
                    session.commit()
                    logger.debug(f"Persisted [{len(instances)}] instances successfully!")
        logger.debug(f"-save_all()")
