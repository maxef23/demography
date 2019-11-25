from flask import request

from app import refbooks, app
from app.Utils import crud, crud_catalog, force_pagination, login_required, paginated_search_query

@app.route('/api/post', methods=('GET', 'POST'))
@login_required
def post(current_user):
    if request.method == 'GET':
        model = refbooks.PostModel
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
                refbooks.PostModel,
                current_user)


@app.route('/api/catalog/post', methods=('GET', 'POST'))
@login_required
def catalog_post(current_user):
    return crud_catalog(request.method, refbooks.PostModel, current_user)

