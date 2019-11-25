from flask import request
from flask.json import jsonify
from sqlalchemy import or_

from app import app, refbooks
from app.API import login_required
from app.Utils import FETCH_LIMIT, paginated_search_query


@app.route('/api/client', methods=('GET',))
@login_required
def client(current_user):
    query = refbooks.ClientModel.query

    # Фильтр по Имени (Client.name1)
    if request.values.get('client_name1', None) is not None:
        query = query.filter(refbooks.ClientModel.NAME1.like('{}%'.format(request.values['client_name1'])))

    # Фильтр по Отчеству (Client.name2)
    if request.values.get('client_name2', None) is not None:
        query = query.filter(refbooks.ClientModel.NAME2.like('{}%'.format(request.values['client_name2'])))

    # Фильтр по Фамилии (Client.surname)
    if request.values.get('client_surname', None) is not None:
        query = query.filter(refbooks.ClientModel.SURNAME.like('{}%'.format(request.values['client_surname'])))

    # Фильтр по Полису (Client.temp_policy_number | Client.policy_number)
    # Точное соответствие во временном или постоянном полисе.
    if request.values.get('policy_number', None) is not None:
        query = query.filter(or_(
            refbooks.ClientModel.TEMP_POLICY_NUMBER == request.values['policy_number'],
            refbooks.ClientModel.POLICY_NUMBER == request.values['policy_number']))

    if request.values.get('no_man') == '1':
        query = query.filter(refbooks.ClientModel.SEX != 1)

    return jsonify({'rows': [instance.to_json() for instance in query.limit(FETCH_LIMIT).all()]})


@app.route('/api/client/q', methods=('GET',))
@login_required
def client_search(current_user):
    return paginated_search_query(refbooks.ClientModel)
