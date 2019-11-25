from typing import Dict, List, Optional

from functools import lru_cache

from flask import request
from flask.json import jsonify
from sqlalchemy.orm import aliased

from app import app
from app.refbooks.Address.models import ADDROBJ, ActStatus


class AOLEVELS:
    subject = ['1', '2']
    district = ['3']
    city = ['35', '4', '6']
    street = ['6', '7', '75']

def get_address_object_list(aolevels: List[str],
                            parentguid: str = None,
                            formalname: str = None,
                            limit: int = None,
                            with_loc_type: bool = False,
                            only_actual: bool = True) -> Dict:
    """ Список адресных объектов по условию
    :param aolevels: Уровни адресных объектов
    :param parentguid: Идентификатор родительского объекта
    :param formalname: Наименование
    :param limit: Максимальное количество записей
    :param with_loc_type: Добавить тип местности (город/сельская местность)
    :param only_actual: Только актуальные адреса
    :return: список адресных объектов
    """
    return {'rows': []}
    cols = [ADDROBJ.AOID.label('id'),
            ADDROBJ.obj_name.label('obj')]
    if with_loc_type:
        cols.append(ADDROBJ.loc_type.label('type'))

    query = (ADDROBJ.query.with_entities(*cols)
             .filter(ADDROBJ.AOLEVEL.in_(aolevels)))
    if only_actual:
        query = query.filter(ADDROBJ.ACTSTATUS == ActStatus.Active)
    if parentguid:
        ParentADDROBJ = aliased(ADDROBJ)  # type: ADDROBJ
        query = (query.join(ParentADDROBJ, ADDROBJ.parent)
                 .filter(ParentADDROBJ.AOID == parentguid))
    if formalname:
        query = query.filter(ADDROBJ.FORMALNAME.like('%' + formalname + '%'))

    query = query.order_by('obj')
    if limit:
        query = query.limit(limit)

    return {'rows': [res._asdict() for res in query]}


def get_address_object_by_guid(guid: str) -> Optional[Dict]:
    u""" Адресный объект по ключу (AOID) """
    return None

    query = (ADDROBJ.query.with_entities(ADDROBJ.AOID.label('id'),
                                         ADDROBJ.obj_name.label('obj'),
                                         ADDROBJ.loc_type.label('type'))
             .filter(ADDROBJ.AOID == guid)
             .order_by('obj'))
    obj = query.first()
    return obj._asdict() if obj else None


@app.route('/api/get_address_object', methods=('GET',))
def address_object():
    guid = request.values.get('guid', None)
    result = get_address_object_by_guid(guid)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({})


@app.route('/api/address_object/subject', methods=('GET',))
def address_subject():
    return jsonify(get_address_object_list(aolevels=AOLEVELS.subject,
                                           formalname=request.values.get('name')))


@app.route('/api/address_object/district/<guid>', methods=('GET',))
def address_district(guid):
    name = request.values.get('name')
    result = get_address_object_list(aolevels=AOLEVELS.district,
                                           parentguid=guid,
                                           formalname=name)
    return jsonify(result)


@app.route('/api/address_object/city/<guid>', methods=('GET',))
def address_city(guid):
    return jsonify(get_address_object_list(aolevels=AOLEVELS.city,
                                           parentguid=guid,
                                           formalname=request.values.get('name'),
                                           with_loc_type=True))


@app.route('/api/address_object/street/<guid>', methods=('GET',))
def address_street(guid):
    return jsonify(get_address_object_list(aolevels=AOLEVELS.street,
                                           parentguid=guid,
                                           formalname=request.values.get('name')))
