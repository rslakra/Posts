#
# Author: Rohtash Lakra
#

import logging
from typing import Mapping, Iterable, Dict, Any, List, Optional

from werkzeug.datastructures import MultiDict

from framework.orm.repository import AbstractRepository
from globals import connector

logger = logging.getLogger(__name__)


class ClassicalRepository(AbstractRepository):
    """The base repository of all non-ORM repositories."""

    def filter(self, filters: Dict[str, Any]) -> List[Optional[Any]]:
        pass

    def __init__(self):
        super().__init__(engine=connector.engine)

    def execute(self, statement, params={}, many: bool = False):
        """Executes the query"""
        logger.info(f"execute({statement}, {params}, {many}), connector => {connector}")
        # print(f"execute({params}, {many}), connector => {connector}")
        connection = connector.get_connection()
        if many:
            return connection.executemany(statement, params)
        else:
            return connection.execute(statement, params)

    def build_filters(self, filters, connector='AND', operators={}, return_tuple=False):
        logger.debug(f"+build_filters({filters}, {connector}, {operators}, {return_tuple})")
        filter_clause = ""
        query_params = {}
        if filters:
            query_fragments = []
            # check filter is type of multi-dictionary
            if isinstance(filters, MultiDict):
                # iterate each key
                for key in filters.keys():
                    values = filters.getlist(key)
                    # check values count
                    if len(values) > 1:
                        in_params = []
                        # iterate values
                        for index, value in enumerate(values):
                            unique_key = f'{key}_{index}'
                            in_params.append(f'%({unique_key})s')
                            query_params[unique_key] = value

                        query_fragments.append(f'{key} IN ({", ".join(in_params)})')
                    else:
                        unique_key = f'{key}_0'
                        operator = operators.get(key) if operators.get(key, None) else '='
                        query_fragments.append(f'{key}{operator}%({unique_key})s')
                        query_params[unique_key] = values[0]

            # check filters is type of mapping
            elif isinstance(filters, Mapping):
                # iterate each item of filters
                for index, (key, value) in enumerate(filters.items()):
                    # check value is type of list
                    if isinstance(value, list):
                        if not value:
                            query_fragments.append('FALSE')
                            continue

                        in_params = []
                        for index, list_value in enumerate(value):
                            unique_key = f'{key}_{index}'
                            in_params.append(f'%({unique_key})s')
                            query_params[unique_key] = list_value

                        query_fragments.append(f'{key} IN ({", ".join(in_params)})')
                    else:
                        operator = operators.get(key) if operators.get(key, None) else '='
                        query_fragments.append(f'{key}{operator}%({key})s')
                        query_params[key] = value
            else:
                raise ValueError('The "query_params" must be either dictionary or MultiDict!')
            filter_clause = f' {connector} '.join(query_fragments)

        # return response
        if return_tuple:
            logger.debug(f"-build_filters(), filter_clause={filter_clause}, query_params={query_params}")
            return filter_clause, query_params
        else:
            logger.debug(f"-build_filters(), filter_clause={filter_clause}")
            filter_clause

    def where_clause(self, filters, connector='AND', operators={}):
        logger.debug(f"where_clause({filters}, {connector}, {operators})")
        filter_clause, query_params = self.build_filters(filters, connector, operators, return_tuple=True)
        return 'WHERE ' + filter_clause, query_params if filters else filter_clause

    def __format_field(self, field):
        return "{}=%({})s".format(field, field)

    def build_update_set_fields(self, update_json):
        logger.debug(f"+build_update_set_fields({update_json})")
        update_keys = list(update_json.keys())
        update_fields = "{} {}".format(
            ", ".join([self.__format_field(update_key) for update_key in update_keys[0:-1]]),
            self.__format_field(update_keys[-1])
        )
        # update_fields = ''.join([update_key + '=%(' + update_key + ')s, ' for update_key in update_keys[0:-1]]) + update_keys[-1] + '=%(' + update_keys[-1] + ')s'

        update_set_fields = "SET {}".format(update_fields)
        logger.debug(f"-build_update_set_fields(), update_set_fields={update_set_fields}")
        return update_set_fields

    def save(self, instance):
        pass

    def save_all(self, instances: Iterable[object]):
        pass
