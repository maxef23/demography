from app.other.Base import *


class UserPreferencesModel(db.Model, ModelMixIn):
    __tablename__ = 'rbUserPreferences'
    __table_args__ = {'mysql_engine': 'MyISAM', 'comment': 'Справочник настроек пользователя'}

    id = Column(Integer, primary_key=True)
    certificateType = Column(String(45), comment='Тип сертификата (birth_certificate, death_certificate, etc.)')
    width = Column(Float(10, 2), comment='Ширина поля')
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=False, comment='Ссылка на пользователя')
    columns = Column(String(45), comment='Перечень колонок отделенных запятой')
