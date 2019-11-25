from app import db
from app.other.Base import *


class DocumentTypeModel(db.Model, ModelMixIn):
    __tablename__ = 'rbDocumentType'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник типов документов'}

    id = Column(Integer, primary_key=True)
    name = Column(String128, nullable=False, comment='Название')
    code = Column(String64, comment='Код')
