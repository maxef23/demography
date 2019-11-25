from flask import request

from app import refbooks, app
from app.API import login_required
from app.Utils import crud, crud_catalog, force_pagination


@app.route('/api/document_type', methods=('GET',))
@login_required
def document_type(current_user):
    if request.method == 'GET':
        query = refbooks.DocumentTypeModel.query

        code = request.args.get('code', '')
        if code:
            query = query.filter_by(code=code)

        return force_pagination(query)

    return crud(request.method, None, refbooks.DocumentTypeModel, current_user)


@app.route('/api/catalog/document_type', methods=('GET', 'POST'))
@login_required
def catalog_document_type(current_user):
    return crud_catalog(request.method, refbooks.DocumentTypeModel, current_user)
