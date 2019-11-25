from sqlalchemy import func, join, select
from sqlalchemy.ext.hybrid import hybrid_property

from app.other.Base import *


class GroupRightModel(db.Model, ModelMixIn):
    __tablename__ = 'Group_Right'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    groupId = Column(Integer, ForeignKey('Group.id', ondelete='CASCADE'), primary_key=True)
    group = db.relationship('GroupModel', foreign_keys=[groupId])
    rightId = Column(Integer, ForeignKey('Right.id', ondelete='CASCADE'), primary_key=True)
    right = db.relationship('RightModel', foreign_keys=[rightId])


class GroupModel(db.Model, ModelMixIn):
    __tablename__ = 'Group'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Группа пользователей'}

    id = Column(Integer, primary_key=True)
    name = Column(String128, comment='Название и описание группы')
    userList = db.relationship('UserModel', secondary='User_Group')

    rightList = db.relationship('RightModel', secondary='Group_Right')
    createdUser_id = Column(Integer, ForeignKey('User.id'), primary_key=False, comment='Ссылка на создателя группы')
    createdUser = db.relationship("UserModel")

    @classmethod
    def save_lists(cls, json_data):
        current = cls.query.filter_by(id=json_data['data']['row_id']).first()  # type: GroupModel
        rightList = json_data['data'].get('rightList', '')
        if rightList:
            right_id_list = rightList.split(',')
            current.rightList = RightModel.query.filter(RightModel.id.in_(right_id_list)).all()
        else:
            current.rightList = []
        db.session.commit()

    @hybrid_property
    def level(self):
        """ Уровень доступа группы """
        return max((right.level for right in self.rightList), default=0)

    @level.expression
    def level(cls):
        table = join(RightModel, GroupRightModel, RightModel.id == GroupRightModel.rightId)
        return (select([func.ifnull(func.max(RightModel.level), 0)])
                .select_from(table)
                .where(GroupRightModel.groupId == cls.id)).label('group_level')


class RightModel(db.Model, ModelMixIn):
    __tablename__ = 'Right'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Справочник прав'}

    id = Column(Integer, primary_key=True)
    name = Column(String128, comment='Название и описание права')
    code = Column(String64, comment='Код права')
    level = Column(Integer, default=0, nullable=False, comment='Уровень доступа')

    groupList = db.relationship('GroupModel', secondary='Group_Right')
