from app import refbooks, app
from app.Utils import FETCH_LIMIT


@app.route('/api/mkb/classes', methods=('GET',))
def mkb_classes():
    return refbooks.get_mkb_data(refbooks.MKBClassModel, 'class')


@app.route('/api/mkb/groups', methods=('GET',))
def mkb_groups():
    return refbooks.get_mkb_data(refbooks.MKBGroupModel, 'group')


@app.route('/api/mkb/codes', methods=('GET',))
def mkb_codes():
    return refbooks.get_mkb_data(refbooks.MKBCodeModel, 'code', limit=FETCH_LIMIT)
