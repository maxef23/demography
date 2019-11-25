import logging
import sys
import traceback

from flask import Response, g, request
from flask.json import jsonify

from app import app, db, other
from app.Utils import crud, crud_catalog, force_pagination, get_columns_name_type, get_user_by_token, \
    get_user_id_by_token, get_user_rights, has_any_right, login_required, paginated_search_query, user_rights
from app.certificates import BirthCertificateModel, DeathCertificateModel, PerinatalDeathCertificateModel
from app.refbooks import ClientModel, ClientValidationModel, CounterModel, MKBCodeModel, OrganisationModel, PostModel, \
    UserPreferencesModel

map_model = {
    'user': other.UserModel,
    'group': other.GroupModel,
    'log': other.LoggerModel,
    'organisation': OrganisationModel,
    'client': ClientModel,
    'counter': CounterModel,
    'mkb/codes': MKBCodeModel,
    'post': PostModel,
    'user_preferences': UserPreferencesModel,
    'client_validation': ClientValidationModel,
    'birth_certificate': BirthCertificateModel,
    'death_certificate': DeathCertificateModel,
    'perinatal_death_certificate': PerinatalDeathCertificateModel
}


@app.route('/api/get_model_structure', methods=('GET',))
@login_required
def get_model_structure(current_user):
    if request.values.get('model', None) is not None:
        model = map_model[request.values.get('model', None)]
    return get_columns_name_type(model)


@app.route('/api/current_user', methods=('GET',))
@login_required
def get_current_user(current_user: other.UserModel):
    return jsonify(current_user.to_json())


@app.route('/api/user', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['user'], 'POST': ['user'], 'ANY': ['admin']})
def user(current_user):
    if request.method == 'GET':
        if 'admin' in get_user_rights(current_user):
            query = other.UserModel.query
        else:
            query = other.UserModel.query.filter_by(organisationId=current_user.organisationId)

        if request.values.get('user_name', None) is not None:
            query = query.filter(other.UserModel.login.like('%s%%' % request.values['user_name']))
        if request.values.get('user_id', None) is not None:
            query = query.filter(other.UserModel.id == request.values['user_id'])

        return force_pagination(query)
    return crud(request.method, request.json, other.UserModel, current_user)


@app.route('/api/user/q', methods=('GET',))
@login_required
def user_search(current_user):
    query = other.UserModel.query.filter_by(organisationId=current_user.organisationId)
    return paginated_search_query(other.UserModel, query)


@app.route('/api/user_get_columns_atrs', methods=('GET',))
@login_required
def user_get_columns_name_type(current_user):
    model = other.UserModel
    return get_columns_name_type(model)


@app.route('/api/group', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['group'], 'POST': ['group'], 'ANY': ['admin']})
def group(current_user: other.UserModel):
    if request.method == 'GET':
        query = other.GroupModel.query
        if not has_any_right(current_user, ['admin']):
            query = query.filter(other.GroupModel.level <= current_user.level)
        if not has_any_right(current_user, ['admin', 'Groups']):
            query = query.filter(other.GroupModel.id.in_([g.id for g in current_user.groupList]))

        if request.values.get('group_name', None) is not None:
            query = query.filter(other.GroupModel.name.like('%s%%' % request.values['group_name']))
        if request.values.get('group_id', None) is not None:
            query = query.filter(other.GroupModel.id == request.values['group_id'])

        return force_pagination(query)
    return crud(request.method, request.json, other.GroupModel, current_user)


@app.route('/api/group/q', methods=('GET',))
@login_required
@user_rights({'GET': ['group', 'admin']})
def group_search(current_user):
    return paginated_search_query(other.GroupModel)


@app.route('/api/group_get_columns_atrs', methods=('GET',))
@login_required
def group_get_columns_name_type(current_user):
    model = other.GroupModel
    return get_columns_name_type(model)


@app.route('/api/catalog/group', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['user'], 'POST': ['user'], 'ANY': ['admin']})
def catalog_group(current_user):
    query = other.GroupModel.query
    query = query.filter(other.GroupModel.level <= current_user.level)
    return crud_catalog(request.method, other.GroupModel, current_user, query)


@app.route('/api/catalog/right', methods=('GET',))
@login_required
@user_rights({'GET': ['group'], 'POST': ['group'], 'ANY': ['admin']})
def catalog_right(current_user):
    return crud_catalog(request.method, other.RightModel, current_user)


@app.route('/api/get_current_user_rights', methods=('GET',))
@login_required
def get_current_user_rights(current_user):
    return jsonify({'user_rights': list(get_user_rights(current_user))})


@app.route('/api/test_connection', methods=('GET',))
def test_connection():
    if db.session.is_active:
        db.engine.execute("SELECT 'HELLO WORLD!'").cursor.fetchall()
        return Response('Connection succeeded', status=200)
    else:
        return Response('Lost connection to DB', status=500)


@app.route('/api/login', methods=('POST',))
def login():
    in_login = request.json['login']
    in_password = request.json['password']
    current_user: other.UserModel = other.UserModel.query.filter_by(login=in_login).first()
    if current_user is None or not current_user.password == in_password:
        return Response('Логин или пароль не верны', status=406)
    else:
        return jsonify({'token': current_user.generate_auth_token().decode('utf-8')})


@app.route('/api/log', methods=('GET',))
@login_required
def log(current_user):
    query = (other.LoggerModel.query
             .outerjoin(other.LoggerModel.user)
             .outerjoin(OrganisationModel))
    return force_pagination(query)


@app.route('/api/log/q', methods=('GET',))
@login_required
def log_search(current_user):
    query = (other.LoggerModel.query
             .outerjoin(other.LoggerModel.user)
             .outerjoin(OrganisationModel)
             .filter(other.UserModel.organisationId == current_user.organisationId))
    return paginated_search_query(other.LoggerModel, query)


@app.route('/api/log_get_columns_atrs', methods=('GET',))
@login_required
def log_get_columns_name_type(current_user):
    model = other.LoggerModel
    return get_columns_name_type(model)


@app.route('/api/catalog/log', methods=('GET',))
@login_required
def catalog_log(current_user):
    return crud_catalog(request.method, other.LoggerModel, current_user)


if app.config.get('DEBUG_LOG'):
    from logging.handlers import WatchedFileHandler
    import time
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    # handler = WatchedFileHandler(app.config.get('DEBUG_LOG_FILENAME', 'debug.log'))
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(process)d] %(message)s'))
    debug_log = logging.getLogger(__name__ + '.sql')
    debug_log.setLevel(logging.DEBUG)
    debug_log.addHandler(handler)


    @app.before_request
    def log():
        g.request_time = time.time()
        user_id = get_user_id_by_token(request.args.get('token'))
        debug_log.debug(f'request[User.id={user_id}][{request.remote_addr}] {request.method} {request.url}')
        if request.data:
            debug_log.debug(f'body: {request.data}')


    @app.after_request
    def log(response: Response):
        ms = (time.time() - g.request_time) * 1000.0
        if not response.direct_passthrough:
            if response.is_json:
                response_info = response.data
            else:
                response_info = f'{len(response.data)} bytes'
        else:
            response_info = '(direct passthrough)'
        debug_log.debug(f'[{ms:4.1f} ms] response [{response.status_code}][{response.content_type}] {response_info}')
        return response


    @event.listens_for(Engine, 'before_cursor_execute')
    def log(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())


    @event.listens_for(Engine, 'after_cursor_execute')
    def log(conn, cursor, statement, parameters, context, executemany):
        total = 1000.0 * (time.time() - conn.info['query_start_time'].pop(-1))
        try:
            sql = cursor.mogrify(statement, parameters).replace('\n', ' ')  # TODO: работает только с "pymysql" драйвером
        except (TypeError, ValueError):
            sql = 'SQL N/A'
        debug_log.debug(f'[{total:4.1f} ms] {sql}')


class SQLAlchemyHandler(logging.Handler):
    """Класс для записи лога в БД."""

    def emit(self, record):
        try:
            new_instance_data = {
                'userid': record.args[1],
                'organisation_id': record.args[2],
                'url': record.args[3],
                'method_action': record.args[4],
                'data': record.args[5],
                'method': request.method,
            }
            new_instance = other.LoggerModel(**new_instance_data)
            db.session.add(new_instance)
            db.session.commit()
        except:
            pass


db_handler = SQLAlchemyHandler()
db_handler.setLevel(logging.INFO)
db_logger = logging.getLogger(__name__)
db_logger.setLevel(logging.INFO)
db_logger.addHandler(db_handler)


@app.after_request
def after_request(response):
    """Лог всех действий в базу данных. Выполняется после каждого запроса."""
    exc_info = sys.exc_info()
    try:
        if request.method in ('POST',):
            if request.path not in ('/api/get_current_user_rights',
                                    '/api/catalog/right',
                                    '/api/user_preferences'):
                json_data = request.json  # type: dict
                try:
                    user = get_user_by_token(request.args.get('token', None))
                    user_id = user.id
                    organisation_id = user.organisationId
                except:
                    user_id = None
                    organisation_id = None

                if json_data is not None:
                    method_action = json_data.get('action', None)  # Тип метода (insert, update, delete, etc.)
                else:
                    method_action = None
                db_logger.info('log', response, user_id, organisation_id, request.path, method_action, str(request.data))
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        traceback.print_exception(*exc_info)
        del exc_info
    finally:
        return response


@app.after_request
def close_session_after_request(response):
    db.session.close()
    return response
