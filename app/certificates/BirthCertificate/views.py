import datetime

from flask import request

from app import app, certificates
from app.API import login_required, user_rights
from app.Utils import crud, force_query_by_request_values, get_columns_name_type, paginated_search_query, set_certificate_completed, set_certificate_deleted, \
    set_certificate_signed, set_certificate_instead_final, set_certificate_instead_prelim, set_certificate_lost, set_certificate_spoiled
from app.certificates.BirthCertificate.prints import print_certificate, print_empty_certificate, print_duplicate
from app.other import UserModel


@app.route('/api/birth_certificate', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['birth_certificate_GET'], 'POST': ['birth_certificate_UPDATE'], 'ANY': ['admin']})
def birth_certificate(current_user: UserModel):
    if request.method == 'GET':
        query = certificates.BirthCertificateModel.query.filter_by(organisation_id=current_user.organisationId)
        query = query.outerjoin(certificates.BirthCertificateModel.updateUser)
        return force_query_by_request_values(certificates.BirthCertificateModel, query,
                                             order=certificates.BirthCertificateModel.id.desc())
    else:
        json_data = request.json if request.method != 'GET' else None
        if request.method == 'POST' and json_data['action'] == 'updated':
            json_data['data']['updateDatetime'] = datetime.datetime.now()
        return crud(request.method, request.json, certificates.BirthCertificateModel, current_user)


@app.route('/api/birth_certificate/q', methods=('GET',))
@login_required
@user_rights({'GET': ['birth_certificate_GET', 'admin']})
def birth_certificate_search(current_user):
    query = certificates.BirthCertificateModel.query.filter_by(organisation_id=current_user.organisationId)
    return paginated_search_query(certificates.BirthCertificateModel, query)


@app.route('/api/birth_certificate/print', methods=('GET',))
@login_required
@user_rights({'GET': ['birth_certificate_GET'], 'ANY': ['admin']})
def birth_certificate_print(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.BirthCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_certificate(cert)


@app.route('/api/birth_certificate/print_empty', methods=('GET',))
@login_required
@user_rights({'GET': ['birth_certificate_GET'], 'ANY': ['admin']})
def birth_certificate_print_empty(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.BirthCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_empty_certificate(cert)


@app.route('/api/birth_certificate/print_duplicate', methods=('GET',))
@login_required
@user_rights({'GET': ['birth_certificate_GET'], 'ANY': ['admin']})
def birth_certificate_print_duplicate(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.BirthCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_duplicate(cert)


@app.route('/api/birth_certificate_completed', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_completed(current_user):
    return set_certificate_completed(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_accept', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_done(current_user):
    return set_certificate_signed(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_spoiled', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_spoiled(current_user):
    return set_certificate_spoiled(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_lost', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_lost(current_user):
    return set_certificate_lost(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_instead_prelim', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_instead_prelim(current_user):
    return set_certificate_instead_prelim(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_instead_final', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_instead_final(current_user):
    return set_certificate_instead_final(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_deleted', methods=('POST',))
@login_required
@user_rights({'POST': ['birth_certificate_ACCEPT'], 'ANY': ['admin']})
def birth_certificate_deleted(current_user):
    return set_certificate_deleted(certificates.BirthCertificateModel, request.json['row_id'], current_user)


@app.route('/api/birth_certificate_get_columns_atrs', methods=('GET',))
@login_required
def birth_certificate_get_columns_name_type(current_user):
    model = certificates.BirthCertificateModel
    return get_columns_name_type(model)
