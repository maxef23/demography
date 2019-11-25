# %%
from typing import Optional

import numpy as np
import pandas as pd

from app import db
from app.refbooks.MKB import MKBClassModel, MKBCodeModel, MKBGroupModel

ClassCodes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
              'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']


def parse_name(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.concat([
        df.drop(['code', 'name'], axis=1),
        df['name'].str.extract(r'(?P<name>.*)\((?P<code>.*)\)'),
    ], axis=1)
    df.loc[:, 'code'] = df['code'].str.strip()
    df.loc[:, 'name'] = df['name'].str.strip()
    return df


def load_mkb_csv(filename: str):
    """
    Импорт МКБ-10 из csv
    Файл взят из https://github.com/ak04nv/mkb10/blob/master/mkb10.csv
    """
    mkb = pd.read_csv(filename,
                      sep=',',
                      names=['id', 'rec_code', 'code', 'name', 'parent_id', 'addl_code', 'actual', 'date'],
                      usecols=['id', 'parent_id', 'code', 'name'])
    mkb['parent_id'] = mkb['parent_id'].fillna(0).astype(np.int)

    classes = mkb[mkb.parent_id == 0]
    classes = parse_name(classes)
    classes.drop('code', axis=1)
    classes.loc[:, 'code'] = ClassCodes

    mkb = mkb[~mkb.id.isin(classes.id)]

    groups = mkb[mkb.parent_id.isin(classes.id)]
    groups = parse_name(groups)

    mkb = mkb[~mkb.id.isin(groups.id)]

    codes0 = mkb[mkb.parent_id.isin(groups.id)]
    mkb = mkb[~mkb.id.isin(codes0.id)]

    codes1 = mkb[mkb.parent_id.isin(codes0.id)]
    codes2 = mkb[~mkb.id.isin(codes1.id)]

    class_id_map = {}
    group_id_map = {}

    for c in classes.itertuples():
        class_ = MKBClassModel.query.filter(
            (MKBClassModel.code == c.code) &
            (MKBClassModel.name == c.name)).first()  # type: Optional[MKBClassModel]
        if class_ is None:
            class_ = MKBClassModel.query.filter((MKBClassModel.code == c.code)).first()  # type: Optional[MKBClassModel]
            if class_ is None:
                class_ = MKBClassModel()
                class_.code = c.code
                db.session.add(class_)
            class_.name = c.name
            db.session.commit()
        class_id_map[c.id] = class_.id

    for g in groups.itertuples():
        class_id = class_id_map[g.parent_id]
        group_ = MKBGroupModel.query.filter(
            (MKBGroupModel.parent_id == class_id) &
            (MKBGroupModel.code.like(f'%{g.code}%'))).first()  # type: Optional[MKBGroupModel]
        if group_ is None:
            group_ = MKBGroupModel()
            group_.parent_id = class_id
            group_.code = f'({g.code})'
            group_.name = g.name
            db.session.add(group_)
            db.session.commit()
        group_id_map[g.id] = group_.id

    for codes in (codes0, codes1, codes2):
        for c in codes.itertuples():
            group_id = group_id_map[c.parent_id]
            code_ = MKBCodeModel.query.filter(
                (MKBCodeModel.parent_id == group_id) &
                (MKBCodeModel.code == c.code)).first()  # type: Optional[MKBCodeModel]
            if code_ is None:
                code_ = MKBCodeModel()
                code_.parent_id = group_id
                code_.code = c.code
                code_.name = c.name
                db.session.add(code_)
                db.session.commit()
            group_id_map[c.id] = group_id
