import datetime

from flask import request

from app import app, certificates, refbooks
from app.API import login_required, user_rights
from app.Utils import BadRequest, crud, force_query_by_request_values, get_columns_name_type, paginated_search_query, \
    set_certificate_completed, set_certificate_signed, set_certificate_instead_final, set_certificate_instead_prelim, \
    set_certificate_lost, set_certificate_spoiled, set_certificate_deleted
from app.certificates.PerinatalDeathCertificate.prints import print_certificate, print_empty_certificate, print_duplicate
from app.other import UserModel


@app.route('/api/perinatal_death_certificate', methods=('GET', 'POST'))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET'], 'POST': ['perinatal_death_certificate_UPDATE'], 'ANY': ['admin']})
def perinatal_death_certificate(current_user: UserModel):
    if request.method == 'GET':
        query = certificates.PerinatalDeathCertificateModel.query.filter_by(organisation_id=current_user.organisationId)
        query = query.outerjoin(certificates.PerinatalDeathCertificateModel.updateUser)
        return force_query_by_request_values(certificates.PerinatalDeathCertificateModel, query,
                                             order=certificates.PerinatalDeathCertificateModel.id.desc())
    else:
        json_data = request.json if request.method != 'GET' else None
        if request.method == 'POST' and json_data['action'] == 'updated':
            json_data['data']['updateDatetime'] = datetime.datetime.now()
        return crud(request.method, json_data, certificates.PerinatalDeathCertificateModel, current_user)


@app.route('/api/perinatal_death_certificate/q', methods=('GET',))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET', 'admin']})
def perinatal_death_certificate_search(current_user):
    query = certificates.PerinatalDeathCertificateModel.query.filter_by(organisation_id=current_user.organisationId)
    return paginated_search_query(certificates.PerinatalDeathCertificateModel, query)


@app.route('/api/perinatal_death_certificate/print', methods=('GET',))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET'], 'ANY': ['admin']})
def perinatal_death_certificate_print(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.PerinatalDeathCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_certificate(cert)


@app.route('/api/perinatal_death_certificate/print_empty', methods=('GET',))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET'], 'ANY': ['admin']})
def perinatal_death_certificate_print_empty(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.PerinatalDeathCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_empty_certificate(cert)


@app.route('/api/perinatal_death_certificate/print_duplicate', methods=('GET',))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET'], 'ANY': ['admin']})
def perinatal_death_certificate_print_duplicate(current_user):
    if request.values.get('id', None) is not None:
        cert = certificates.PerinatalDeathCertificateModel.query.filter_by(id=request.values['id']).first_or_404()
        return print_duplicate(cert)


@app.route('/api/perinatal_death_certificate_completed', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_completed(current_user):
    return set_certificate_completed(certificates.PerinatalDeathCertificateModel, request.json['row_id'], current_user)


@app.route('/api/perinatal_death_certificate_accept', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_done(current_user):
    model = certificates.PerinatalDeathCertificateModel
    validation_func = refbooks.ClientValidation.is_valid_client_data
    cert_id = request.json['row_id']
    cert = model.query.filter_by(id=cert_id).first()  # type: certificates.PerinatalDeathCertificateModel
    if cert is None:
        raise BadRequest(
            message=f'Не найден сертификат с id={cert_id}',
            status_code=404
        )
    elif validation_func(cert.birthDatetime, cert.sex, cert.deathReasonMainMKBId):
        return set_certificate_signed(model, request.json['row_id'], current_user)
    else:
        raise BadRequest(
            message='Валидация данных не пройдена: Дата рождения: %s; Пол: %s; Код основного диагноза: %s' % (
                cert.birthDatetime, ['-', 'M', 'Ж'][cert.sex], cert.deathReasonMainMKBId
            ),
            status_code=406
        )


@app.route('/api/perinatal_death_certificate_spoiled', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_spoiled(current_user):
    return set_certificate_spoiled(certificates.PerinatalDeathCertificateModel, request.json['row_id'], current_user)


@app.route('/api/perinatal_death_certificate_lost', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_lost(current_user):
    return set_certificate_lost(certificates.PerinatalDeathCertificateModel, request.json['row_id'], current_user)


@app.route('/api/perinatal_death_certificate_instead_prelim', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_instead_prelim(current_user):
    return set_certificate_instead_prelim(certificates.PerinatalDeathCertificateModel, request.json['row_id'],
                                          current_user)


@app.route('/api/perinatal_death_certificate_instead_final', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_instead_final(current_user):
    return set_certificate_instead_final(certificates.PerinatalDeathCertificateModel, request.json['row_id'],
                                         current_user)


@app.route('/api/perinatal_death_certificate_deleted', methods=('POST',))
@login_required
@user_rights({'POST': ['perinatal_death_certificate_ACCEPT'], 'ANY': ['admin']})
def perinatal_death_certificate_deleted(current_user):
    return set_certificate_deleted(certificates.PerinatalDeathCertificateModel, request.json['row_id'], current_user)


@app.route('/api/perinatal_death_certificate_get_columns_atrs', methods=('GET',))
@login_required
@user_rights({'GET': ['perinatal_death_certificate_GET'], 'ANY': ['admin']})
def perinatal_death_certificate_get_columns_name_type(current_user):
    model = certificates.PerinatalDeathCertificateModel
    return get_columns_name_type(model)
