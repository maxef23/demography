from typing import List, Tuple

from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.collections import InstrumentedList

from app import db
from app.Utils import xstr

Column = db.Column
String = db.String
DateTime = db.DateTime(timezone=True)
Date = db.Date
Time = db.Time
Text = db.Text
Integer = db.Integer
Float = db.Float
String16 = String(16)
String64 = String(64)
String128 = String(128)
String512 = String(512)
ForeignKey = db.ForeignKey
DayInt = TINYINT(unsigned=True)
MonthInt = TINYINT(unsigned=True)
YearInt = SMALLINT(unsigned=True)


class ModelMixIn:
    ignored_crud_keys_ins = 'row_id', 'data', 'createDatetime', 'updateDatetime', \
                            'max_page', 'curr_page', 'next_page', 'prev_page', 'createdUser_id', 'createdUser'
    ignored_crud_keys_upd = 'row_id', 'data', 'createDatetime', 'updateDatetime', 'status', \
                            'max_page', 'curr_page', 'next_page', 'prev_page', 'createdUser_id', 'createdUser', 'createUserId'

    related_columns = []  # type: List[Tuple[str,str]]

    @classmethod
    def get_ignored_crud_keys_ins(cls):
        return cls.ignored_crud_keys_ins + tuple(c_name for c_name, c_type in cls.related_columns)

    @classmethod
    def get_ignored_crud_keys_upd(cls):
        return cls.ignored_crud_keys_upd + tuple(c_name for c_name, c_type in cls.related_columns)

    def as_dict(self):
        return {column: xstr(getattr(self, column)) for column in inspect(self).attrs._data}

    def as_dict_with_row_id(self):
        return {column if column != 'id' else 'row_id': xstr(getattr(self, column))
                for column in inspect(self).attrs._data}

    def to_json(self):
        relations = getattr(inspect(self.__class__), 'relationships', [])
        return {
            'id': self.id,
            'data': [
                xstr(getattr(self, column))
                for column in inspect(self).attrs._data
                if column not in relations
            ]
        }

    def __repr__(self):
        return str(self.as_dict())

    @classmethod
    def save_lists(cls, json_data):
        pass

    @classmethod
    def get_columns_name_type(cls):
        type_list = [str(column.type) for column in cls.__table__.c]
        name_type_list = [(column_name, column_type)
                          for column_type, column_name in zip(type_list, cls.__table__.c.keys())]
        name_type_list.extend(cls.related_columns)
        return name_type_list


class RBModelMixIn(ModelMixIn):
    @staticmethod
    def xstr(s):
        if type(s) == InstrumentedList:
            return [i.id for i in s]
        if 'to_json' in dir(s):
            return s.to_json()
        return '' if s is None else str(s)

    def as_dict(self):
        relations = getattr(inspect(self.__class__), 'relationships', [])
        return {column: self.xstr(getattr(self, column))
                for column in inspect(self).attrs._data
                if column not in relations}

    def to_json(self):
        return self.as_dict()
