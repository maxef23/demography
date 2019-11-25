import itertools as it
import logging
import os

import dbfread

from app import app, db
from app.refbooks.Client.models import ClientModel

logger = logging.getLogger('demography_import')
logger.setLevel(logging.INFO)


def split_every(n, iterable):
    i = iter(iterable)
    piece = list(it.islice(i, n))
    while piece:
        yield piece
        piece = list(it.islice(i, n))


def import_dbf(filename, limit=0):
    logger.info(f'Import {filename} (limit={limit}):')

    field_map = {
        'DT_VRSV': 'TEMP_POLICY_DATE',
        'NO_VRSV': 'TEMP_POLICY_NUMBER',
        'EDINNP': 'ENP',
        'SER_POL': 'POLICY_SERIAL',
        'NOM_POL': 'POLICY_NUMBER',
        'FAM': 'SURNAME',
        'IM': 'NAME1',
        'OT': 'NAME2',
        'D_R': 'BIRTHDAY',
        'POL': 'SEX',
        'RAION': 'REGION',
        'KOD_NP': 'LOCALITY_CODE',
        'NAS_P': 'LOCALITY',
        'KOD_UL': 'STREET_CODE',
        'DOM': 'HOUSE',
        'KV': 'FLAT',
        'KDLPU': 'MO_CODE',
        'KOD_SMO': 'SMO_CODE',
        'SS': 'CLIENT_SNILS',
        'SS_UCHVR': 'MEDIC_SNILS',
    }
    search_field_map = {
        'FAM': 'SURNAME',
        'IM': 'NAME1',
        'OT': 'NAME2',
        'D_R': 'BIRTHDAY',
    }

    count = 0
    countAdded = 0

    dbf = dbfread.DBF(filename, encoding='cp866')

    for recs in split_every(500, dbf):
        for rec in recs:
            count += 1
            exists = db.session.query(ClientModel.id).filter_by(
                **{
                    db_field: rec[dbf_field]
                    for dbf_field, db_field in search_field_map.items()
                    if rec[dbf_field] is not None
                }
            ).scalar() is not None

            if not exists:
                fields = {db_field: (rec[dbf_field] or None)
                          for dbf_field, db_field in field_map.items()}

                client = ClientModel(**fields)
                db.session.add(client)
                countAdded += 1

            if count >= limit: break

        logger.debug(f'processed: {count}, added: {countAdded}')
        db.session.commit()

        if count >= limit: break

    logger.info(f'Total records: {count}, added: {countAdded}')


def import_from_dir(dirname, limit=0):
    fh = logging.FileHandler(app.config.get('IMPORT_LOG_FILE', 'import.log'))
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

    logger.info(f'Import from directory: {dirname}')
    for filename in os.listdir(dirname):
        filepath = os.path.join(dirname, filename)
        if not os.path.isfile(filepath):
            continue
        if filename.lower().endswith('.dbf'):
            import_dbf(filepath, limit)
