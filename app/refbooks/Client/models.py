from app.other.Base import *


class ClientModel(db.Model, ModelMixIn):
    __tablename__ = 'Client'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Клиент'}


    id = Column(Integer, primary_key=True)
    TEMP_POLICY_DATE = Column(Date, comment='Дата временного полиса')
    TEMP_POLICY_NUMBER = Column(Integer, comment='Номер временного полиса')
    ENP = Column(String64, comment='Единый номер полиса')
    POLICY_NUMBER = Column(String64, comment='Номер постоянного полиса')
    POLICY_SERIAL = Column(String16, comment='Серия постоянного полиса')
    POLICY_DATE = Column(Date, comment='Дата постоянного полиса')
    SURNAME = Column(String64, comment='Фамилия')
    NAME1 = Column(String64, comment='Имя')
    NAME2 = Column(String64, comment='Отчество')
    BIRTHDAY = Column(Date, comment='Дата рождения')
    SEX = Column(Integer, comment='Пол. 1 - мужской, 2 - женский')
    AREA = Column(String16, comment='')
    REGION = Column(String16, comment='Регион???')
    LOCALITY_CODE = Column(String16, comment='Код местности???')
    LOCALITY = Column(String16, comment='Местность')
    STREET_CODE = Column(String16, comment='Код улицы')
    HOUSE = Column(String16, comment='Номер дома')
    FLAT = Column(String16, comment='Квартира')
    MO_CODE = Column(String16, comment='')
    SMO_CODE = Column(String16, comment='')
    CLIENT_SNILS = Column(String64, comment='Снилс')
    MEDIC_SNILS = Column(String64, comment='')

    name_brith_idx = db.Index('NAME_BIRTH_IDX', SURNAME, NAME1, NAME2, BIRTHDAY)
    policy_idx = db.Index('POLICY_IDX', POLICY_NUMBER, POLICY_SERIAL)
    temp_policy_idx = db.Index('TEMPPOLICY_IDX', TEMP_POLICY_NUMBER)
    enp_idx = db.Index('ENP_IDX', ENP)
    snils_idx = db.Index('CLIENT_SNILS', CLIENT_SNILS)
