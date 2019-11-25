from app.other.Base import *


class SpecialityModel(db.Model, ModelMixIn):
    __tablename__ = 'rbSpeciality'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник специальностей'}

    id = Column(Integer, primary_key=True)
    code = Column(String(8), comment='Код')
    name = Column(String64, comment='Наименование')
