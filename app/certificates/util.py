import datetime
from typing import Any, Optional

from markupsafe import Markup
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from app.other.Base import *
from app.other.User import UserModel
from app.refbooks import CounterModel, OrganisationModel


def combine_name(*items):
    return ' '.join(it for it in items if it)


def combine_date(year, month, day) -> Optional[datetime.date]:
    if not (year and month and day):
        return None
    try:
        return datetime.date(year, month, day)
    except (ValueError, TypeError):
        return None


# def render_pdf(template, **context):
#     data = render_template(template, **context)
#     pdf = BytesIO()
#     pisa.CreatePDF(data, pdf)
#     pdf.seek(0)
#     return send_file(pdf, as_attachment=False, mimetype='application/pdf')


class LocType:
    """ Тип местности """
    City = 1  # Городская
    Countryside = 2  # Сельская


month_names = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
               'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
month_names_gc = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

datetime_number_agreement = [
    ('год', 'года', 'лет'),
    ('месяц', 'месяца', 'месяцев'),
    ('неделя', 'недели', 'недель'),
    ('день', 'дня', 'дней'),
    ('час', 'часа', 'часов'),
    ('минута', 'минуты', 'минут'),
]


def agree_number_and_word(value, words):
    """ Согласовать число и существительное """
    if value < 0: value = -value
    if (value / 10) % 10 != 1:
        if value % 10 == 1:
            return words[0]
        elif 1 < value % 10 < 5:
            return words[1]
    return words[-1]


def format_period_entry(value: Any, words: Tuple[str, str, str]) -> str:
    try:
        return '{} {}'.format(value, agree_number_and_word(int(value), words))
    except (ValueError, TypeError):
        return '{} {}'.format(value, words[-1])


def format_period(years=None, months=None, weeks=None, days=None, hours=None, minutes=None) -> str:
    """ Текстовое представление периода """
    return ' '.join(format_period_entry(value, words)
                    for value, words in zip((years, months, weeks, days, hours, minutes),
                                            datetime_number_agreement)
                    if value)


def month_name(m, gc=False):
    if not m: return ''
    if 1 <= m <= 12:
        return month_names_gc[m] if gc else month_names[m]
    return ''


class BaseCertificate(object):
    createDatetime = Column(DateTime, default=datetime.datetime.now, comment='Дата создания документа')

    @declared_attr
    def createUserId(self):
        return Column(Integer, ForeignKey('User.id'), primary_key=False,
                      comment='Пользователь, создавший предварительную запись')

    @declared_attr
    def createUser(cls):
        return db.relationship('UserModel', foreign_keys=[cls.createUserId])

    updateDatetime = Column(DateTime, onupdate=func.now(), comment='Дата последнего обновления файла')

    @declared_attr
    def updateUserId(cls):
        return Column(Integer, ForeignKey('User.id'), primary_key=False,
                      comment='Пользователь, внесший последние изменения')

    @declared_attr
    def updateUser(cls):
        return db.relationship('UserModel', foreign_keys=[cls.updateUserId])

    @property
    def updateUserLogin(self):
        return self.updateUser.login if self.updateUser is not None else ''

    closedDatetime = Column(DateTime, nullable=True, comment='Дата и время создания предварительной записи')

    @declared_attr
    def closedUserId(cls):
        return Column(Integer, ForeignKey('User.id'), primary_key=False, comment='Пользователь, закрывший запись')

    @declared_attr
    def closedUser(cls):
        return db.relationship('UserModel', foreign_keys=[cls.closedUserId])

    status = Column(Integer, comment='Статус документа')
    serial = Column(String16, nullable=True, comment='Серия документа')
    number = Column(Integer, nullable=True, comment='Номер документа', index=True)

    deliveryDate_Y = Column(YearInt, comment='Корешок. Дата выдачи документа (год)')
    deliveryDate_M = Column(MonthInt, comment='Корешок. Дата выдачи документа (месяц)')
    deliveryDate_D = Column(DayInt, comment='Корешок. Дата выдачи документа (день)')

    @property
    def deliveryDate(self):
        return combine_date(self.deliveryDate_Y, self.deliveryDate_M, self.deliveryDate_D)

    medicalOrganisationHeadFamilyName = Column(String64, comment='Фамилия руководителя мед. учреждения')
    medicalOrganisationHeadFirstName = Column(String64, comment='Имя руководителя мед. учреждения')
    medicalOrganisationHeadMiddleName = Column(String64, comment='Отчество руководителя мед. учреждения')

    @property
    def medicalOrganisationHeadName(self):
        return combine_name(self.medicalOrganisationHeadFamilyName,
                            self.medicalOrganisationHeadFirstName,
                            self.medicalOrganisationHeadMiddleName)

    recipientFamilyName = Column(String64, comment='Корешок. Фамилия')
    recipientFirstName = Column(String64, comment='Корешок. Имя')
    recipientMiddleName = Column(String64, comment='Корешок. Отчество')

    @property
    def recipientName(self) -> str:
        return combine_name(self.recipientFamilyName, self.recipientFirstName, self.recipientMiddleName)

    @declared_attr
    def recipientDocumentType(cls):
        return Column(Integer, ForeignKey('rbDocumentType.id', ondelete='SET NULL'),
                      comment='Корешок. Документ {rbDocumentType}', nullable=True)

    @declared_attr
    def recipientDocType(cls):
        return db.relationship('DocumentTypeModel', foreign_keys=[cls.recipientDocumentType])

    recipientDocumentSerial = Column(String64, comment='Корешок. Серия документа')
    recipientDocumentNumber = Column(String64, comment='Корешок. Номер документа')
    recipientDocumentOrigin = Column(String128, comment='Кем выдан документ')

    recipientDocumentDate_Y = Column(YearInt, comment='Дата выдачи документа удостоверяющего личность (год)')
    recipientDocumentDate_M = Column(MonthInt, comment='Дата выдачи документа удостоверяющего личность (месяц)')
    recipientDocumentDate_D = Column(DayInt, comment='Дата выдачи документа удостоверяющего личность (день)')

    @property
    def recipientDocumentDate(self):
        return combine_date(self.recipientDocumentDate_Y,
                            self.recipientDocumentDate_M,
                            self.recipientDocumentDate_D)

    @property
    def recipientDocument(self) -> str:
        """ Документ устоверяющий личность """
        return ' '.join(it for it in (
            self.recipientDocType.name if self.recipientDocType else '',
            self.recipientDocumentSerial,
            self.recipientDocumentNumber,
            ' '.join(t for t in ('выдан',
                                 self.recipientDocumentOrigin or '',
                                 self.recipientDocumentDate.strftime('%d.%m.%Y')
                                 if self.recipientDocumentDate else '') if t)
            if self.recipientDocumentDate is not None or self.recipientDocumentOrigin else ''
        ) if it)

    @declared_attr
    def doctorWhoGaveCertificatePost_id(cls):
        return Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                      comment='Должность врача, выдавшего медицинское свидетельство')

    @declared_attr
    def doctorWhoGaveCertificatePost(cls):
        return db.relationship('PostModel', foreign_keys=[cls.doctorWhoGaveCertificatePost_id])

    doctorWhoGaveCertificateFamilyName = Column(String64, comment='Фамилия врача, выдавшего медицинское свидетельство')
    doctorWhoGaveCertificateFirstName = Column(String64, comment='Имя врача, выдавшего медицинское свидетельство')
    doctorWhoGaveCertificateMiddleName = Column(String64, comment='Отчество врача, выдавшего медицинское свидетельство')

    @property
    def doctorWhoGaveCertificateName(self):
        return combine_name(self.doctorWhoGaveCertificateFamilyName,
                            self.doctorWhoGaveCertificateFirstName,
                            self.doctorWhoGaveCertificateMiddleName)

    @declared_attr
    def doctorWhoCheckedCertificatePost_id(cls):
        return Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                      comment='Должность врача, проверившего медицинское свидетельство')

    @declared_attr
    def doctorWhoCheckedCertificatePost(cls):
        return db.relationship('PostModel', foreign_keys=[cls.doctorWhoCheckedCertificatePost_id])

    doctorWhoCheckedCertificateFamilyName = Column(String64,
                                                   comment='Фамилия врача, проверившего медицинское свидетельство')
    doctorWhoCheckedCertificateFirstName = Column(String64, comment='Имя врача, проверившего медицинское свидетельство')
    doctorWhoCheckedCertificateMiddleName = Column(String64,
                                                   comment='Отчество врача, проверившего медицинское свидетельство')

    @property
    def doctorWhoCheckedCertificateName(self):
        return combine_name(self.doctorWhoCheckedCertificateFamilyName,
                            self.doctorWhoCheckedCertificateFirstName,
                            self.doctorWhoCheckedCertificateMiddleName)

    @declared_attr
    def doctorWhoFillCertificatePost_id(cls):
        return Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                      comment='Должность врача, заполнившего медицинское свидетельство')

    @declared_attr
    def doctorWhoFillCertificatePost(cls):
        return db.relationship('PostModel', foreign_keys=[cls.doctorWhoFillCertificatePost_id])

    doctorWhoFillCertificateFamilyName = Column(String64,
                                                comment='Фамилия врача, заполнившего медицинское свидетельство')
    doctorWhoFillCertificateFirstName = Column(String64, comment='Имя врача, заполнившего медицинское свидетельство')
    doctorWhoFillCertificateMiddleName = Column(String64,
                                                comment='Отчество врача, заполнившего медицинское свидетельство')

    @property
    def doctorWhoFillCertificateName(self) -> str:
        return combine_name(self.doctorWhoFillCertificateFamilyName,
                            self.doctorWhoFillCertificateFirstName,
                            self.doctorWhoFillCertificateMiddleName)

    @declared_attr
    def organisation_id(cls):
        return Column(Integer, ForeignKey('Organisation.id'), primary_key=False,
                      comment='Организация, выдавшая сертификат')

    @declared_attr
    def organisation(cls):
        return db.relationship('OrganisationModel', foreign_keys=[cls.organisation_id])

    @classmethod
    def get_serial(cls, year=None):
        """ Текущая серия сертификатов """
        raise NotImplementedError

    def init_from_user(self, user: UserModel, onlyOrganisation=False):
        self.organisation_id = user.organisationId
        if not onlyOrganisation:
            self.doctorWhoFillCertificateFamilyName = user.familyName
            self.doctorWhoFillCertificateFirstName = user.firstName
            self.doctorWhoFillCertificateMiddleName = user.middleName
            self.doctorWhoFillCertificatePost_id = user.post_id

            head_user = OrganisationModel.get_head_user(user.organisationId)
            if head_user is not None:
                self.medicalOrganisationHeadFamilyName = head_user.familyName
                self.medicalOrganisationHeadFirstName = head_user.firstName
                self.medicalOrganisationHeadMiddleName = head_user.middleName

    counter_code = ''

    @classmethod
    def update_serial_number(cls, cert_id, year=None):
        """ Заполнение серии/номера в сертификате
             номер должен заполняться счетчиком (текущий + 1),
             выполняется update-запросом, чтобы при параллельных запросах на создание не было дублирования номера """
        counter = CounterModel.get_counter(code=cls.counter_code, year=year)
        table = cls.__table__
        db.session.execute(
            table.update().where(table.c.id == cert_id).values(
                serial=cls.get_serial(counter.year),
                number=func.getCounterValue(counter.id)
            )
        )
        db.session.commit()


def checkbox(cond, value='V', empty='&nbsp;'):
    return Markup('<div class="checkbox">{0}</div>'.format(value if cond else empty))


def underline_if(cond, value):
    return Markup('<span {0}>{1}</span>'.format('class="underline"' if cond else '',
                                                value))


def underlined(value, cond, style=''):
    return Markup('<div class="underline" {style}>{value}</div>'.format(
        style='style="%s"' % style if not cond else '',
        value=value if cond else ''
    ))


def underlined_style(value, style):
    return underlined(value, bool(value), style)


def underlined_width(value, width):
    return underlined_style(value, "width: {};".format(width))


def format_time(value: Optional[datetime.time],
                fmt: str = '%H:%M',
                undefined: bool = False) -> str:
    return value.strftime(fmt) if value else ('XXXX' if undefined else '')
