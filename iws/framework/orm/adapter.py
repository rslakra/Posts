#
# Author: Rohtash Lakra
#

class DBAdapter:
    pass


class ObjectClass:
    pass


class AbstractAdapter(DBAdapter):

    def find_by_id(self, ObjectClass, id):
        """ Retrieve one object specified by the primary key 'pk' """
        pass

    def find_all(self, ObjectClass, **kwargs):
        """ Retrieve all objects matching the case-sensitive filters in 'kwargs'. """

    pass

    def find_first(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case-sensitive filters in 'kwargs'. """
        pass

    def contains(self, ObjectClass, **kwargs):
        """ Retrieve the object matching the case-sensitive filters in 'kwargs'. """
        pass

    def filter(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case-insensitive filters in 'kwargs'. """
        pass

    def create(self, ObjectClass, **kwargs):
        """ Add an object of class 'ObjectClass' with fields and values specified in '**kwargs'. """
        pass

    def update(self, object, **kwargs):
        """ Update object 'object' with the fields and values specified in '**kwargs'. """
        pass

    def delete(self, object):
        """ Delete object 'object'. """
        pass

    def commit(self):
        """ Commits the 'self' object. """
        pass
