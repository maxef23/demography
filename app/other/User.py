from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import func, join, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from app import app
from app.other.Base import *
from app.other.Group import GroupModel, GroupRightModel, RightModel


class UserModel(db.Model, ModelMixIn):
    __tablename__ = 'User'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Пользователь'}

    id = Column(Integer, primary_key=True)
    login = Column(String64, nullable=False, comment='Логин', unique=True)
    password = Column(String128, nullable=False, comment='Пароль')
    firstName = Column(String64)
    familyName = Column(String64)
    middleName = Column(String64)
    groupList = db.relationship('GroupModel', secondary='User_Group')
    organisationId = Column(Integer, ForeignKey('Organisation.id', ondelete='SET NULL'),
                            comment='Организация, в которой работает пользователь')

    post_id = Column(Integer, ForeignKey('rbPost.id'), primary_key=False, comment='Должность')
    post = db.relationship('PostModel', foreign_keys=[post_id])

    speciality_id = Column(Integer, ForeignKey('rbSpeciality.id'), primary_key=False, comment='Специальность')
    speciality = db.relationship('SpecialityModel', foreign_keys=[speciality_id])

    SNILS = Column(String16, comment='СНИЛС')

    organisationAdminList = db.relationship('OrganisationAdminModel')

    @property
    def full_name(self):
        return '%s %s %s' % (self.familyName, self.firstName, self.middleName,)

    def generate_auth_token(self, expiration=10000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'row_id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)
        return UserModel.query.get(data['row_id'])

    @classmethod
    def save_lists(cls, json_data):
        current = cls.query.filter_by(id=json_data['data']['row_id']).first()  # type: UserModel
        groupList = json_data['data'].get('groupList', '')
        if groupList:
            group_id_list = list(map(int, groupList.split(',')))
            current.groupList = GroupModel.query.filter(GroupModel.id.in_(group_id_list)).all()
        else:
            current.groupList = []
        db.session.commit()

    @validates('login')
    def validate_login(self, key, login):
        if not login: return ''
        exists = UserModel.query.filter_by(login=login).first()
        if exists:
            raise AssertionError(u'Пользователь с таким логином уже существует')
        return login

    @hybrid_property
    def level(self):
        """ Уровень доступа пользователя """
        return max((group.level for group in self.groupList), default=0)

    @level.expression
    def level(cls):
        return (select([func.ifnull(func.max(RightModel.level), 0)])
                .join(GroupModel)
                .join(UserGroupModel)
                .where(UserGroupModel.userId == cls.id)
                .label('user_level'))

    def right_codes(self):
        t = join(UserGroupModel, GroupModel, UserGroupModel.groupId == GroupModel.id)
        t = join(t, GroupRightModel, GroupRightModel.groupId == GroupModel.id)
        t = join(t, RightModel, RightModel.id == GroupRightModel.rightId)
        q = select([RightModel.code]).select_from(t).where(UserGroupModel.userId == self.id)
        return set(row.code for row in db.session.execute(q))

    def __str__(self):
        return f'<User(id={self.id}, login={self.login})>'

class UserGroupModel(db.Model, ModelMixIn):
    __tablename__ = 'User_Group'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    userId = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    groupId = Column(Integer, ForeignKey('Group.id', ondelete='CASCADE'), primary_key=True)
