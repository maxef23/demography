from app.other.Base import *


class MKBClassModel(RBModelMixIn, db.Model):
    __tablename__ = 'rbMKBClass'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник классов МКБ-10'}

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, comment='Наименование класса МКБ-10')
    code = Column(String16, comment='Код класса МКБ-10')


class MKBGroupModel(RBModelMixIn, db.Model):
    __tablename__ = 'rbMKBGroup'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник групп МКБ-10'}

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, comment='Наименование группы МКБ-10')
    code = Column(String16, comment='Код группы МКБ-10')
    parent_id = Column(Integer, ForeignKey('rbMKBClass.id'), primary_key=False, comment='Ссылка на класс МКБ-10')
    parent = db.relationship("MKBClassModel")


class MKBCodeModel(RBModelMixIn, db.Model):
    __tablename__ = 'rbMKBCode'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник диагнозов МКБ-10'}

    id = Column(Integer, primary_key=True)
    name = Column(String(320), nullable=False, comment='Наименование диагноза МКБ-10')
    code = Column(String16, comment='Код диагноза МКБ-10')
    parent_id = Column(Integer, ForeignKey('rbMKBGroup.id'), primary_key=False, comment='Ссылка на группу МКБ-10')
    parent = db.relationship("MKBGroupModel")


# def get_mkb_data(model, field, limit=None):
#     from flask import request
#     from flask.json import jsonify
#
#     if request.values.get(field, None) is None:
#         query = model.query
#     else:
#         query = model.query.filter(model.code.like('%s%%' % request.values[field]))
#     if limit is not None:
#         query = query.limit(limit)
#     return jsonify({'rows': [instance.to_json() for instance in query.all()]})


def get_mkb_data(model, field, limit=None):
    from flask import request
    from flask.json import jsonify

    query = model.query
    if request.values.get(field, None) is not None:
        query = query.filter(model.code.like('%{}%'.format(request.values[field])))
    if request.values.get('name', None) is not None:
        query = query.filter(model.name.like('%{}%'.format(request.values['name'])))
    if limit is not None:
        query = query.limit(limit)
    return jsonify({'rows': [instance.to_json() for instance in query.all()]})
