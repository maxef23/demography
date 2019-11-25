import datetime

from app.other.Base import *


class ClientValidationModel(db.Model, ModelMixIn):
    __tablename__ = 'rbClientValidation'
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'comment': 'Справочник валидации данных пациента (в справочнике находятся запреты)'}

    id = Column(Integer, primary_key=True)
    ageFrom = Column(Integer, nullable=True, comment='Возраст "с"')
    ageTo = Column(Integer, nullable=True, comment='Возраст "по"')
    sex = Column(Integer, comment='Пол (1 — М, 2 — Ж)')
    mkb = Column(String(45), comment='Код МКБ-10')

    @staticmethod
    def get_age(birth_date, today=None):
        if today is None:
            today = datetime.datetime.now()

        t_year = today.year
        t_month = today.month
        t_day = today.day

        b_year = birth_date.year
        b_month = birth_date.month
        b_day = birth_date.day

        result = t_year - b_year
        if b_month > t_month or (b_month == t_month and b_day > t_day):
            result -= 1
        return result

    @staticmethod
    def force_date(date_str):
        if isinstance(date_str, (datetime.date, datetime.datetime)):
            return date_str
        else:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def force_datetime(date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def is_valid_client_data(birth_date, sex, mkb):
    """ Валидация данных
        если какое-то поле пустое - валидация не проводится """
    if all(map(lambda x: bool(x), (birth_date, sex, mkb))):
        age = ClientValidationModel.get_age(ClientValidationModel.force_date(birth_date))
        return not bool(ClientValidationModel
                        .query \
                        .filter(ClientValidationModel.ageFrom <= age,
                                ClientValidationModel.ageTo >= age,
                                ClientValidationModel.sex == sex,
                                ClientValidationModel.mkb == mkb) \
                        .first())
    return True
