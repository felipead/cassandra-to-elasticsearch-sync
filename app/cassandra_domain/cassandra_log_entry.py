from time_uuid import TimeUUID

from app.core.model.abstract_data_object import AbstractDataObject
from app.core.model.identifier import Identifier


class CassandraLogEntry(AbstractDataObject):

    def __init__(self, logged_keyspace=None, logged_table=None, logged_key=None,
                 time_uuid=None, operation=None, updated_columns=None):

        self._logged_keyspace = logged_keyspace
        self._logged_table = logged_table
        self._logged_key = logged_key
        self._time_uuid = time_uuid
        self._operation = operation
        self._updated_columns = updated_columns

    @property
    def time_uuid(self):
        return self._time_uuid

    @time_uuid.setter
    def time_uuid(self, value):
        if value is not None:
            self._time_uuid = TimeUUID.convert(value)
        else:
            self._time_uuid = None

    @property
    def time(self):
        if self.time_uuid is not None:
            return self.time_uuid.get_datetime()
        else:
            return None

    @property
    def timestamp(self):
        if self.time_uuid is not None:
            return self.time_uuid.get_timestamp()
        else:
            return None

    @property
    def logged_keyspace(self):
        return self._logged_keyspace

    @logged_keyspace.setter
    def logged_keyspace(self, value):
        self._logged_keyspace = value
        
    @property
    def logged_table(self):
        return self._logged_table

    @logged_table.setter
    def logged_table(self, value):
        self._logged_table = value

    @property
    def logged_key(self):
        return self._logged_key

    @logged_key.setter
    def logged_key(self, value):
        self._logged_key = value

    @property
    def logged_identifier(self):
        return Identifier(self.logged_keyspace, self.logged_table, self.logged_key)

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value

    @property
    def is_delete(self):
        if self._operation:
            return self._operation.lower() == "delete"
        return False

    @property
    def is_save(self):
        if self._operation:
            return self._operation.lower() == "save"
        return False

    @property
    def updated_columns(self):
        return self._updated_columns

    @updated_columns.setter
    def updated_columns(self, value):
        if value is not None:
            self._updated_columns = set(value)
        else:
            self._updated_columns = None

    def _deep_equals(self, other):
        return self.time_uuid == other.time_uuid and \
            self.logged_keyspace == other.logged_keyspace and \
            self.logged_table == other.logged_table and \
            self.logged_key == other.logged_key and \
            self.operation == other.operation and \
            self.updated_columns == other.updated_columns

    def __hash__(self):
        current_hash = hash((self.time_uuid, self.logged_keyspace, self.logged_table, self.logged_key, self.operation))
        if self.updated_columns is None:
            return current_hash
        else:
            return hash((current_hash, frozenset(self.updated_columns)))

    def __repr__(self):
        return repr({
            "time_uuid": self.time_uuid,
            "logged_keyspace": self.logged_keyspace,
            "logged_table": self.logged_table,
            "logged_key": self.logged_key,
            "operation": self.operation,
            "updated_columns": self.updated_columns
        })
