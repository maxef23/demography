from flask import request

from app import refbooks, app
from app.Utils import crud, crud_catalog, force_pagination, login_required


@app.route('/api/speciality', methods=('GET', 'POST'))
@login_required
def speciality(current_user):
    if request.method == 'GET':
        model = refbooks.SpecialityModel
        query = model.query

        if request.values.get('name', None) is not None:
            query = query.filter(model.name.like('%{}%'.format(request.values['name'])))
        if request.values.get('code', None) is not None:
            query = query.filter(model.name.like('%{}%'.format(request.values['code'])))
        if request.values.get('id', None) is not None:
            query = query.filter(model.id == request.values['id'])

        return force_pagination(query)
    return crud(request.method,
                None if request.method == 'GET' else request.json,
                refbooks.SpecialityModel,
                current_user)


@app.route('/api/catalog/speciality', methods=('GET', 'POST'))
@login_required
def catalog_speciality(current_user):
    return crud_catalog(request.method, refbooks.SpecialityModel, current_user)
