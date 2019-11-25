from flask import request
from sqlalchemy.orm import joinedload

from app import app, refbooks
from app.API import login_required, user_rights
from app.Utils import crud, crud_catalog, force_pagination, get_columns_name_type, paginated_search_query


@app.route('/api/organisation', methods=('GET',))
@login_required
def organisation_get(current_user):
    query = refbooks.OrganisationModel.query
    if request.values.get('org_name', None) is not None:
        query = query.filter(refbooks.OrganisationModel.name.like('%{}%'.format(request.values['org_name'])))
    if request.values.get('org_id', None) is not None:
        query = query.filter(refbooks.OrganisationModel.id == request.values['org_id'])

    return force_pagination(query)


@app.route('/api/organisation', methods=('POST',))
@login_required
@user_rights({'ANY': ['organisation', 'admin']})
def organisation_post(current_user):
    return crud(request.method, request.json, refbooks.OrganisationModel, current_user)


@app.route('/api/organisation/q', methods=('GET',))
@login_required
def organisation_search(current_user):
    return paginated_search_query(refbooks.OrganisationModel)


@app.route('/api/catalog/organisation', methods=('GET', 'POST'))
@login_required
def catalog_organisation(current_user):
    query = refbooks.OrganisationModel.query.options(joinedload(refbooks.OrganisationModel.userList))
    return crud_catalog(request.method, refbooks.OrganisationModel, current_user, query=query)


@app.route('/api/organisation_get_columns_atrs', methods=('GET',))
@login_required
def organisation_get_columns_name_type(current_user):
    model = refbooks.OrganisationModel
    return get_columns_name_type(model)
