from typing import Optional

from app.other.Base import *
from app.other.User import UserModel
from app.refbooks.Post import PostModel


class OrganisationModel(db.Model, ModelMixIn):
    __tablename__ = 'Organisation'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник организаций'}

    id = Column(Integer, primary_key=True)
    address = Column(String128, comment='Адрес')
    code = Column(String16, comment='Код МО')
    name = Column(String(256), comment='Название организации')
    okpo = Column(String(8), comment='Код по ОКПО')
    shortName = Column(String128, comment='Короткое наименование организации')

    userList = db.relationship('UserModel')

    @staticmethod
    def get_head_user(organisationId: int) -> Optional[UserModel]:
        """ Главный врач медицинской организации """
        query = (db.session.query(UserModel)
                 .join(PostModel)
                 .filter(UserModel.organisationId == organisationId)
                 .filter(PostModel.code == '20668'))
        return query.first()


class OrganisationAdminModel(db.Model, ModelMixIn):
    __tablename__ = 'OrganisationAdmin'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Администраторы организаций'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), comment='Пользователь')
    organisation_id = Column(Integer, ForeignKey('Organisation.id'), comment='Организация')

    user = db.relationship('UserModel', foreign_keys=[user_id])
    organisation = db.relationship('OrganisationModel', foreign_keys=[organisation_id])
