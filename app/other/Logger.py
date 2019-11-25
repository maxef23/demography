import datetime

from app.other.Base import *
from app.other.User import UserModel
from app.refbooks import OrganisationModel


class LoggerModel(db.Model, ModelMixIn):
    __tablename__ = 'Logger'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Логи всех действий'}

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('User.id'), primary_key=False, comment='Пользователь произведший действие')
    method = Column(String16, comment='Метод (Get, Post, Options...')
    method_action = Column(db.String(24), comment='Действие метода. (Insert, Update, Delete)', index=True)
    url = Column(String512, comment='Url с которого было произведено действие')
    data = Column(Text(5000), comment='Данные из запроса')
    description = Column(Text(256), comment='Описание действия')
    datetime = Column(DateTime, default=datetime.datetime.now, comment='Дата и время лога', index=True)
    organisation_id = Column(Integer, ForeignKey('Organisation.id'), comment='Организация пользователя')

    user = db.relationship('UserModel', foreign_keys=[userid])
    organisation = db.relationship('OrganisationModel', foreign_keys=[organisation_id])

    related_columns = [
        ('userLogin', str(UserModel.login.type)),
        ('organisationName', str(OrganisationModel.name.type)),
    ]

    @property
    def description_text(self):
        return ''

    def to_json(self):
        res = super().to_json()
        res['data'].extend([
            self.user.login if self.user else '',
            self.organisation.name if self.organisation else ''
        ])
        return res
