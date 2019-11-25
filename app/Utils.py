import datetime
from enum import Enum
from functools import wraps

from flask import Response, request
from flask.json import jsonify
from flask_sqlalchemy import BaseQuery, Pagination
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql import desc

from app import app, db, other

FETCH_LIMIT = 350


class BadRequest(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        result = dict(self.payload or ())
        result['message'] = self.message
        return result


class Action:
    completed = 'completed'
    deleted = 'deleted'
    done = 'done'
    inserted = 'inserted'
    inserted_to_print = 'inserted_to_print'
    instead_final = 'instead_final'
    instead_preliminary = 'instead_preliminary'
    lost = 'lost'
    spoiled = 'spoiled'
    updated = 'updated'


class CertStatus(Enum):
    DELETED = 0  # Удалено
    PROJECT = 1  # Проект
    COMPLETED = 2  # Заполнено
    SIGNED = 3  # Подписано
    FINAL = 4  # Окончательное
    PRELIM = 5  # Предварительное
    SPOILED = 6  # Испорченное
    LOST = 7  # Утерянное
    EMPTY = 8  # Выдано пустое


def xstr(s):
    if type(s) == InstrumentedList:
        return [i.id for i in s]
    return None if s is None else str(s)


def get_user_id_by_token(token):
    if not token:
        return None
    try:
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)
        return data['row_id']
    except:
        return None


def get_user_by_token(token):
    s = Serializer(app.config['SECRET_KEY'], expires_in=1200)
    if token is None:
        raise BadRequest(message='Вы не зашли в систему', status_code=401)
    try:
        data = s.loads(token)
        user_id = data['row_id']
        user = other.UserModel.query.get(user_id)
        if user is None:
            raise BadRequest(message='Не найден пользователь [id={}]'.format(user_id), status_code=401)
        return user
    except SignatureExpired:
        raise BadRequest(message='Сессия закончена. Перезайдите', status_code=401)
    except BadSignature:
        raise BadRequest(message='Неверный ключ сессии. Перезайдите', status_code=401)
    except InvalidRequestError:
        return get_user_by_token(token)


def login_required(func):
    @wraps(func)
    def wrapper():
        try:
            token = request.args.get('token', None)
            user = get_user_by_token(token)
            return func(user)
        except BadRequest as e:
            return Response(e.message, status=e.status_code)

    return wrapper


def get_user_rights(user):
    u"""
    Возвращает список кодов прав пользователя системы

    :param user: экземпляр модели пользователя
    :type user: app.models.User.UserModel
    :return: список прав
    :rtype: set[str]
    """
    return user.right_codes()


def has_any_right(user, rights):
    return bool(get_user_rights(user).intersection(rights))


def user_rights(right_dict=None, is_any=True):
    def user_rights_decorator(func):
        @wraps(func)
        def user_rights_wrapper(current_user):
            try:
                assert right_dict is not None and len(right_dict.items()) > 0, \
                    'the `right_dict` dict should not be None and items count must be greater then 0'

                method = request.method
                right_list = right_dict.get(method, []) + right_dict.get('ANY', [])
                right_intersect = set(right_list) & get_user_rights(current_user)
                if (is_any and len(right_intersect) > 0) or (not is_any and len(right_intersect) == len(right_dict)):
                    return func(current_user)
                else:
                    return Response('Недостаточно прав', status=403)
            except BadRequest as e:
                return Response(e.message, status=e.status_code)

        return user_rights_wrapper

    return user_rights_decorator


def force_pagination(query: BaseQuery, order=None):
    query = query.order_by(order if order is not None else desc('id'))
    page = int(request.values.get('page', 1))
    per_page = int(request.values.get('per_page', FETCH_LIMIT))
    pagination = query.paginate(page, per_page, error_out=False)  # type: Pagination
    return jsonify({
        'rows': [instance.to_json() for instance in pagination.items],
        'max_page': pagination.pages,
        'curr_page': pagination.page,
        'next_page': pagination.next_num,
        'prev_page': pagination.prev_num,
    })


def force_query_by_request_values(model, query: BaseQuery = None, order=None):
    if query is None:
        query = model.query
    for param, value in filter(lambda x: hasattr(model, x), request.values.keys()):
        query = query.filter(getattr(model, param).like('{}%'.format(value)))
    return force_pagination(query, order)


def crud(method, json_data, model, current_user):
    """
    crud логика для всех моделей, к которым предполагается доступ по стандартному crud
    Заточена под протокол общения с dhtmlx
    Обратите внимание, что метод GET отвратительно зависит от порядка полей. Так работает протокол dhtmlx
    Всем новым сертификатам проставляется статус 0
    :param method:
    :param json_data
    :param model:
    :param current_user
    """
    if method == 'GET':
        return force_pagination(model.query)

    elif method == 'POST':
        if json_data['action'] in (Action.inserted, Action.inserted_to_print):
            new_instance_data = {k: v if v != '' else None if 'List' not in k else []
                                 for k, v in json_data['data'].items() if k not in model.get_ignored_crud_keys_ins()}
            if not (model.__name__ in ('BirthCertificateModel', 'DeathCertificateModel',
                                       'PerinatalDeathCertificateModel')
                    and new_instance_data['serial'] and new_instance_data['number']):
                if hasattr(model, 'createDatetime'):
                    new_instance_data['createDatetime'] = datetime.datetime.now()
                if hasattr(model, 'status'):
                    new_instance_data['status'] = CertStatus.PROJECT.value
                if hasattr(model, 'createUserId'):
                    new_instance_data['createUserId'] = current_user.id
                if hasattr(model, 'user_id'):
                    new_instance_data['user_id'] = current_user.id
            if hasattr(model, 'updateDatetime'):
                new_instance_data['updateDatetime'] = datetime.datetime.now()
            if hasattr(model, 'updateUserId'):
                new_instance_data['updateUserId'] = current_user.id

            if model.__name__ == 'GroupModel':
                new_instance_data['createdUser_id'] = int(current_user.id)

            try:
                serial_year = new_instance_data.pop('serial_year', None)
                new_instance = model(**new_instance_data)
                if model.__name__ in ('BirthCertificateModel', 'DeathCertificateModel',
                                      'PerinatalDeathCertificateModel'):
                    new_instance.init_from_user(
                        user=current_user,
                        onlyOrganisation=json_data['action'] == Action.inserted_to_print
                    )
                    if json_data['action'] == Action.inserted_to_print:
                        new_instance.status = CertStatus.EMPTY.value
                elif isinstance(new_instance, other.UserModel):
                    new_instance.organisationId = current_user.organisationId

                db.session.add(new_instance)
                db.session.commit()

                if model.__name__ in ('BirthCertificateModel', 'DeathCertificateModel',
                                      'PerinatalDeathCertificateModel'):
                    new_instance.__class__.update_serial_number(
                        cert_id=new_instance.id,
                        year=serial_year  # json_data['action'] == Action.inserted_to_print
                    )

            except Exception as e:
                raise BadRequest(message=str(e))

            # Проставление настроек по умолчанию при создании нового юзера
            if model.__name__ == 'UserModel':
                from app.refbooks.UserPreferences import UserPreferencesModel
                for certificate_type in ['birth_certificate', 'death_certificate', 'perinatal_death_certificate']:
                    pref_instance_data = {'certificateType': certificate_type, 'user_id': new_instance.id,
                                          'columns': '0,4,5'}
                    pref_instance = UserPreferencesModel(**pref_instance_data)
                    db.session.add(pref_instance)
                    db.session.commit()

            response_data = {'action': json_data['action'],
                             'data': new_instance.as_dict_with_row_id()}
            if json_data['action'] == Action.inserted_to_print:
                response_data['gr_id'] = json_data.get('id', '')
            return jsonify(response_data)

        elif json_data['action'] == Action.updated:
            # Сохранить все не списки
            new_instance_data = {k: v if v != '' else None for k, v in json_data['data'].items()
                                 if k not in model.get_ignored_crud_keys_upd() and 'List' not in k}
            if hasattr(model, 'updateUserId'):
                new_instance_data['updateUserId'] = current_user.id

            current_instance = model.query.filter_by(id=json_data['data']['row_id']).first()
            if current_instance is not None and hasattr(current_instance,
                                                        'status') and current_instance.status == CertStatus.SIGNED.value:
                raise BadRequest(message='Нельзя обновлять подписанный документ')

            try:
                model.query.filter_by(id=json_data['data']['row_id']).update(new_instance_data)
            except IntegrityError as e:
                raise BadRequest(message=str(e))
            db.session.commit()

            # Сохранить списки
            model.save_lists(json_data)

            return jsonify({'action': Action.updated})
        elif json_data['action'] == Action.deleted:
            cert = model.query.filter_by(id=json_data['data']['row_id']).first()

            if hasattr(model, 'status'):
                current_status = cert.status
                if current_status != CertStatus.PROJECT.value:
                    raise BadRequest(message='Нельзя удалять подписанный документ')
            if model.__name__ in ('BirthCertificateModel', 'DeathCertificateModel', 'PerinatalDeathCertificateModel'):
                model.query.filter_by(id=json_data['data']['row_id']).update({'status': CertStatus.DELETED.value})
            else:
                model.query.filter_by(id=json_data['data']['row_id']).delete()
            db.session.commit()
            return jsonify({'action': Action.deleted})


def crud_catalog(method, model, current_user, query=None):
    if method == 'GET':
        # if model.__name__ == 'RightModel' and current_user.userRight != 3:
        #     query = model.query.filter(~model.name.contains('Админ')).limit(FETCH_LIMIT).all()
        #     return jsonify([instance.as_dict_with_row_id() for instance in query])
        if query is None:
            query = model.query
        return jsonify([instance.as_dict_with_row_id() for instance in query.limit(FETCH_LIMIT).all()])


def set_certificate_signed(model, cert_id, current_user):
    """
    Перевод сертификата в статус подписанного/напечатанного. Больше этот сертификат изменять нельзя.
    :param model:
    :param cert_id:
    :param current_user:
    :return:
    """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status == CertStatus.SIGNED.value:
        raise BadRequest(message='Сертификат уже подписан')
    elif current_status == CertStatus.SPOILED.value:
        raise BadRequest(message='Нельзя подписать сертификат: Сертификат является испорченым')
    elif current_status == CertStatus.LOST.value:
        raise BadRequest(message='Нельзя подписать сертификат: Сертификат является утеряным')
    elif current_status in (CertStatus.PROJECT.value, CertStatus.COMPLETED.value, CertStatus.EMPTY.value):
        cert.status = CertStatus.SIGNED.value
        if hasattr(cert, 'closedUserId'):
            cert.closedUserId = current_user.id
        if hasattr(cert, 'closedDatetime'):
            cert.closedDatetime = datetime.datetime.now()
        db.session.commit()
    else:
        raise BadRequest(message='Сертификат не должен иметь статуса')
    return jsonify({'action': Action.done})


def set_certificate_completed(model, cert_id, current_user):
    """ Сертификат заполнен """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status in (CertStatus.PROJECT.value, CertStatus.EMPTY.value):
        cert.status = CertStatus.COMPLETED.value
        db.session.commit()
        return jsonify({'action': Action.completed, 'data': cert.as_dict_with_row_id()})
    else:
        raise BadRequest(message='Сертификат не должен иметь статуса')


def set_certificate_spoiled(model, cert_id, current_user):
    """
    Перевод сертификата в статус испорченного. Больше этот сертификат изменять нельзя.
    :param model:
    :param cert_id:
    :param current_user:
    :return:
    """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status == CertStatus.SPOILED.value:
        raise BadRequest(message='Сертификат уже является испорченым')
    elif current_status == CertStatus.LOST.value:
        raise BadRequest(message='Нельзя пометить сертификат как испорченый: Сертификат является утеряным')
    elif current_status == CertStatus.SIGNED.value or current_status == CertStatus.COMPLETED.value:
        cert.status = CertStatus.SPOILED.value  # Испорчено
        db.session.commit()

        new_cert = cert
        new_cert.status = CertStatus.PROJECT.value
        new_cert.createDatetime = datetime.datetime.now()
        new_cert.createUser = current_user
        new_cert_data = new_cert.as_dict_with_row_id()
        new_cert_data['prevCertId'] = cert.id
        new_cert_data['prevCert'] = [cert.id]
        new_cert_data['row_id'] = None

        return jsonify({'action': Action.spoiled, 'data': new_cert_data})
    else:
        raise BadRequest(message='Сертификат должен быть подписан')


def set_certificate_lost(model, cert_id, current_user):
    """
    Перевод сертификата в статус потерянного. Больше этот сертификат изменять нельзя.
    :param model:
    :param cert_id:
    :param current_user:
    :return:
    """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status == CertStatus.SPOILED.value:
        raise BadRequest(message='Нельзя пометить сертификат как утерянный: Сертификат является испорченным')
    elif current_status == CertStatus.LOST.value:
        raise BadRequest(message='Сертификат уже является утерянным')
    elif current_status == CertStatus.SIGNED.value or current_status == CertStatus.COMPLETED.value:
        cert.status = CertStatus.LOST.value  # Потерян
        db.session.commit()

        new_cert = cert
        new_cert.status = CertStatus.COMPLETED.value
        new_cert.createDatetime = datetime.datetime.now()
        new_cert.createUser = current_user
        new_cert_data = new_cert.as_dict_with_row_id()
        new_cert_data['prevCertId'] = cert.id
        new_cert_data['prevCert'] = [cert.id]
        new_cert_data['row_id'] = None

        return jsonify({'action': Action.lost, 'data': new_cert_data})
    else:
        raise BadRequest(message='Сертификат должен быть подписан')


def set_certificate_instead_prelim(model, cert_id, current_user):
    """ Новый сертификат вместо предварительного """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status == CertStatus.SIGNED.value or current_status == CertStatus.COMPLETED.value:
        cert.status = CertStatus.PRELIM.value
        db.session.commit()

        new_cert = cert
        new_cert.status = CertStatus.PROJECT.value
        new_cert.createDatetime = datetime.datetime.now()
        new_cert.createUser = current_user
        new_cert_data = new_cert.as_dict_with_row_id()
        new_cert_data['prevCertId'] = cert.id
        new_cert_data['prevCert'] = [cert.id]
        new_cert_data['row_id'] = None

        return jsonify({'action': Action.instead_preliminary, 'data': new_cert_data})
    else:
        raise BadRequest(message='Сертификат должен быть подписан')


def set_certificate_deleted(model, cert_id, current_user):
    """ Отметить сертификат удаленным """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    if cert.status == CertStatus.PROJECT.value:
        cert.status = CertStatus.DELETED.value
        db.session.commit()
        return jsonify({'action': Action.deleted})
    else:
        raise BadRequest(message='Сертификат должен иметь статус "Проект"')


def set_certificate_instead_final(model, cert_id, current_user):
    """ Новый сертификат вместо окончательного """
    cert = model.query.filter_by(id=cert_id).first()
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    current_status = cert.status
    if current_status == CertStatus.SIGNED.value or current_status == CertStatus.COMPLETED.value:
        cert.status = CertStatus.FINAL.value
        db.session.commit()

        new_cert = cert
        new_cert.status = CertStatus.PROJECT.value
        new_cert.createDatetime = datetime.datetime.now()
        new_cert.createUser = current_user
        new_cert_data = new_cert.as_dict_with_row_id()
        new_cert_data['prevCertId'] = cert.id
        new_cert_data['prevCert'] = [cert.id]
        new_cert_data['row_id'] = None

        return jsonify({'action': Action.instead_final, 'data': new_cert_data})
    else:
        raise BadRequest(message='Сертификат должен быть подписан')


def get_columns_name_type(model):
    """
    По запросу выдает список полей модели и их типы.
    :param model:
    :return:
    """
    return jsonify([
        {
            'column_name': column_name,
            'column_type': column_type
        }
        for column_name, column_type in model.get_columns_name_type()
    ])


def paginated_search_query(model, query: BaseQuery = None):
    if query is None:
        query = model.query
    for arg_name, value in request.args.items():
        if arg_name == 'row_id': arg_name = 'id'
        field = getattr(model, arg_name, None)
        if field is not None and value:
            from sqlalchemy import DateTime, Date
            is_date_field = isinstance(field.property.columns[0].type, (Date, DateTime))
            if is_date_field and '_' in value:
                value_from, value_to = value.split('_', 1)
                query = query.filter(field.between(value_from, value_to))
            else:
                query = query.filter(field.like('%{}%'.format(value)))
    return force_pagination(query)
