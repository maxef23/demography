import datetime
from typing import Optional

from sqlalchemy import func

from app.other.Base import *

CounterNameMap = {
    'bc_counter': 'Рождаемость',
    'dc_counter': 'Смертность',
    'pdc_counter': 'Перинатальная смертность',
}


class CounterModel(db.Model, ModelMixIn):
    __tablename__ = 'Counter'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Счетчик для подстановки серии/номера сертификата'}

    id = Column(Integer, primary_key=True)

    updateDatetime = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления')
    updateUserId = Column(Integer, ForeignKey('User.id'), primary_key=False,
                          comment='Пользователь, внесший последние изменения')

    code = Column(String16, nullable=False, comment='Код')
    name = Column(String64, nullable=False, comment='Наименование')
    year = Column(Integer, default=2018, nullable=False, comment='Год для подстановки в серию')
    number = Column(Integer, default=0, nullable=False, comment='Текущее значение счетчика')

    @classmethod
    def get_ignored_crud_keys_upd(cls):
        res = super().get_ignored_crud_keys_upd()
        return res + ('code',)

    @classmethod
    def get_counter(cls, code: str, year: int = None):
        """ Поиск/создание счетчика """
        if year is None:
            year = datetime.date.today().year
        counter = db.session.query(cls).filter_by(code=code, year=year).first()  # type: Optional[CounterModel]
        if counter is None:
            counter = cls(code=code,
                          name='{}_{}'.format(CounterNameMap.get(code, ''), year),
                          year=year)
            db.session.add(counter)
            db.session.commit()
        return counter


db.Index('ix_code_year', CounterModel.code, CounterModel.year, unique=True)
