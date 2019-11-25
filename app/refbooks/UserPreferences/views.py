from flask import request
from flask.json import jsonify

from app import refbooks, app
from app.Utils import crud, crud_catalog, login_required


@app.route('/api/user_preferences', methods=('GET', 'POST'))
@login_required
def user_preferences(current_user):
    if request.method == 'GET':
        model = refbooks.UserPreferencesModel
        query = model.query

        if request.values.get('certificateType', None) is not None:
            query = query.filter(model.certificateType == request.values['certificateType'])
        query = query.filter(model.user_id == current_user.id)

        return jsonify({'rows': [instance.to_json() for instance in query.all()]})
    return crud(request.method,
                None if request.method == 'GET' else request.json,
                refbooks.UserPreferencesModel,
                current_user)


@app.route('/api/catalog/user_preferences', methods=('GET', 'POST'))
@login_required
def catalog_user_preferences(current_user):
    return crud_catalog(request.method, refbooks.UserPreferencesModel, current_user)
