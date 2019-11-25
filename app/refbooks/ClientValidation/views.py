from flask import request
from flask.json import jsonify

from app import app, refbooks
from app.API import login_required, user_rights
from app.Utils import crud, crud_catalog, get_columns_name_type, paginated_search_query


@app.route('/api/client_validation', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['client_validation'], 'POST': ['client_validation'], 'ANY': ['admin']})
def client_validation(current_user):
    return crud(request.method,
                None if request.method == 'GET' else request.json,
                refbooks.ClientValidationModel,
                current_user)


@app.route('/api/client_validation/q', methods=('GET',))
@login_required
@user_rights({'GET': ['client_validation', 'admin']})
def client_validation_search(current_user):
    return paginated_search_query(refbooks.ClientValidationModel)


@app.route('/api/catalog/client_validation', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['client_validation'], 'POST': ['client_validation'], 'ANY': ['admin']})
def catalog_client_validation(current_user):
    return crud_catalog(request.method, refbooks.ClientValidationModel, current_user)


@app.route('/api/is_valid_client_data', methods=('GET',))
def is_valid_client_data():
    return jsonify({'is_valid': refbooks.ClientValidation.is_valid_client_data(request.values['birth_date'],
                                                                               request.values['sex'],
                                                                               request.values['mkb'])})


@app.route('/api/client_validation_get_columns_atrs', methods=('GET',))
@login_required
def client_validation_get_columns_name_type(current_user):
    model = refbooks.ClientValidationModel
    return get_columns_name_type(model)
