from app.other.Base import *


class PostModel(db.Model, ModelMixIn):
    __tablename__ = 'rbPost'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник должностей'}

    id = Column(Integer, primary_key=True)
    code = Column(String(8), comment='Код')
    name = Column(String(256), comment='Наименование')
