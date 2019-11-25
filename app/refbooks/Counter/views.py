from flask import request

from app import app, refbooks
from app.API import login_required, user_rights
from app.Utils import Action, BadRequest, crud, force_pagination, get_columns_name_type


@app.route('/api/certificate_series', methods=('GET', 'POST'))
@login_required
@user_rights({'ANY': ["certificate_series"]})
def certificates_series(current_user):
    if request.method == 'GET':
        return force_pagination(refbooks.CounterModel.query)

    if request.json['action'] == Action.updated:
        return crud(request.method, request.json, refbooks.CounterModel, current_user)


@app.route('/api/certificate_series_get_columns_atrs', methods=('GET',))
# @login_required
def certificates_series_get_columns_atrs(current_user):
    return get_columns_name_type(refbooks.CounterModel)
