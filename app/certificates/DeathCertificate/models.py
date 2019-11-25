import datetime

from dateutil.relativedelta import relativedelta

from app.certificates.util import BaseCertificate, combine_date, combine_name, format_period
from app.other.Base import *
from app.other.User import UserModel


class DeathCertificateModel(db.Model, ModelMixIn, BaseCertificate):
    __tablename__ = 'DeathCertificate'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Форма 106/У-08'}

    counter_code = 'dc_counter'

    id = Column(Integer, primary_key=True)

    type = Column(Integer, comment='Тип свидетельства. 0 — предварительное, 1 — окончательное, '
                                   '2 — взамен предварительного, 3 — взамен окончательного')
    isUnidentified = Column(Integer, comment='Личность не установлена. 0 — нет, 1 — да')
    SNILS = Column(String64, comment='СНИЛС')
    familyName = Column(String64, comment='1.1, 2.1. Фамилия умершего')
    firstName = Column(String64, comment='1.1, 2.1. Имя умершего')
    middleName = Column(String64, comment='1.1, 2.1. Отчество умершего')
    birthDate_Y = Column(YearInt, comment='1.3, 1.7, 2.3. Дата рождения (год)')
    birthDate_M = Column(MonthInt, comment='1.3, 1.7, 2.3. Дата рождения (месяц)')
    birthDate_D = Column(DayInt, comment='1.3, 1.7, 2.3. Дата рождения (день)')
    sex = Column(Integer, comment='1.2, 2.2. Пол (1 — М, 2 — Ж)')
    isRegistryUnidentified = Column(Integer, comment='Место постоянного жительства (регистрации) не установлено. '
                                                     '0 — нет (установлено), 1 — да')
    registryRegion = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Область')
    registryArea = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Район')
    registryCity = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Город')
    registryStreet = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Улица')
    registryHouse = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Дом')
    registryFlat = Column(String64, comment='1.5, 2.5. Место постоянного жительства. Квартира')
    registryLocality = Column(Integer, comment='Местность постоянного жительства. 0 — городская, 1 — сельская')
    isDeathPlaceUnidentified = Column(Integer, comment='Место смерти не установлено. 0 — нет, 1 — да')
    deathPlace = Column(Integer, comment='1.6, 2.9. Смерть наступила (1 — на месте происшествия, '
                                         '2 — в машине скорой помощи, 3 — встационаре, 4 — дома, 5 — в другом месте)')
    deathRegion = Column(String64, comment='1.5, 2.5. Место смерти. Область')
    deathArea = Column(String64, comment='1.5, 2.5. Место смерти. Район')
    deathCity = Column(String64, comment='1.5, 2.5. Место смерти. Город')
    deathStreet = Column(String64, comment='1.5, 2.5. Место смерти. Улица')
    deathHouse = Column(String64, comment='1.5, 2.5. Место смерти. Дом')
    deathFlat = Column(String64, comment='1.5, 2.5. Место смерти. Квартира')
    deathLocality = Column(Integer, comment='Местность смерти. 0 — городская, 1 — сельская')
    isDeathDateAndTimeUnidentified = Column(Integer, comment='Дата и время смерти не установлено. 0 — нет, 1 — да')
    isDeathTimeUnidentified = Column(Integer, comment='Время смерти не установлено. 0 — нет, 1 — да')
    deathDate_Y = Column(YearInt, comment='1.4. Дата смерти (год)')
    deathDate_M = Column(MonthInt, comment='1.4. Дата смерти (месяц)')
    deathDate_D = Column(DayInt, comment='1.4. Дата смерти (день)')
    deathTime = Column(Time, comment='1.4. Время смерти')
    isChildBeforeMonth = Column(Integer, comment='Флаг - ребенок в возрасте от 168 часов до 1 месяца')
    childBeforeMonthWeight = Column(Integer,
                                    comment='2.11.1. Масса при рождении. Граммы (ребенок в возрасте от 168 часов до 1 месяца)')
    childBeforeMonthNumber = Column(Integer,
                                    comment='2.11.2. Каким по счету был ребёнок (ребенок в возрасте от 168 часов до 1 месяца)')
    isChildBeforeYear = Column(Integer, comment='Флаг - ребенок в возрасте от 168 часов до 1 года')
    childBeforeYearWeight = Column(Integer,
                                   comment='2.11.1. Масса при рождении. Граммы (ребенок в возрасте от 168 часов до 1 года)')
    childBeforeYearNumber = Column(Integer,
                                   comment='2.11.2. Каким по счету был ребёнок (ребенок в возрасте от 168 часов до 1 года)')
    childParameters = Column(Integer, comment='2.10. Для детей,  умерших  в возрасте от 168 час. до 1 месяца '
                                              '(1 — доношенный, 2 — недоношенный, 3 — переношенный)')
    childRegion = Column(String64, comment='2.10. Место рождения. Область')
    childArea = Column(String64, comment='2.10. Место рождения. Район')
    childCity = Column(String64, comment='2.10. Место рождения. Город')
    isMotherUnidentified = Column(Integer, comment='Личность матери не установлена. 0 — нет, 1 — да')
    motherSNILS = Column(String16, comment='Снилс матери')
    motherFamilyName = Column(String64, comment='Фамилия матери')
    motherFirstName = Column(String64, comment='Имя матери')
    motherMiddleName = Column(String64, comment='Отчество матери')
    motherDOB_Y = Column(YearInt, comment='Дата рождения матери (год)')
    motherDOB_M = Column(MonthInt, comment='Дата рождения матери (месяц)')
    motherDOB_D = Column(DayInt, comment='Дата рождения матери (день)')
    motherAge = Column(Integer, comment='Возраст матери')
    motherMartialStatus = Column(Integer,
                                 comment='2.6. Семейное положение матери (1 — состоит в зарегестрированном браке, '
                                         '2 — несостоит в зарегестрированном браке, 3 — неизвестно)')
    motherEducation = Column(Integer,
                             comment='2.7. Образование (1 — Высшее, 2 — неполное высшее, 3 — среднее, 4 — начальное, '
                                     '5 — среднее (полное), 6 — основное, 7 — начальное, '
                                     '8 — не имеет начального образования, 9 — неизвестно)')
    motherWork = Column(Integer,
                        comment='2.8. Занятость (1 — руководители и специалисты высшего уровня квалификации, '
                                '2 — прочие специалисты, 3 — квалифицированные рабочие, '
                                '4 — неквалифицированные рабочие, 5 — занятые на военной службе, 6 — пенсионеры, '
                                '7 — студенты и учащиеся, 8 — работавшие в личном подсобном хозяйстве, '
                                '9 — безработные, 10 — прочие)')

    deathReason = Column(Integer,
                         comment='2.15. Смерть произошла от (1 — заболевания, 2 — несчастного случая, не связанного '
                                 'с производством, 3 — несчастного случая, связанного с производством, 4 — убийства, '
                                 '5 — самоубийства, 6 — в ходе военных действий, 7 — в ходе террористических действий,'
                                 '8 — род смерти не установлен0)')
    deathTraumaDetails = Column(String128, comment='2.16. Место и обстоятельства травмы')
    whoTakeDeathReason = Column(Integer, comment='2.24. Причины смерти установлены (1 — врачом, только что установившим'
                                                 'смерть, 2 — лечащим врачом, 3 — фельдшером/акушеркой, '
                                                 '4 — патологоанатомом, 5 — судебно-медицинским экспертом)')
    doctorWhoTakeDeathReasonFamilyName = Column(String64, comment='Фамилия врача, установившего причины смерти')
    doctorWhoTakeDeathReasonFirstName = Column(String64, comment='Имя врача, установившего причины смерти')
    doctorWhoTakeDeathReasonMiddleName = Column(String64, comment='Отчество врач, установившего причины смерти')
    doctorWhoTakeDeathReasonPost_id = Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                                             comment='Должность врача, установившего причины смерти')
    doctorWhoTakeDeathReasonPost = db.relationship('PostModel', foreign_keys=[doctorWhoTakeDeathReasonPost_id])
    organisationWhoTakeDeathReason = Column(String128, comment='Организация, установившая причины смерти')
    deathReasonBased = Column(Integer, comment='2.18 На основании чего установлены причины смерти (1 — осмотр трупа, '
                                               '2 — записей в медицинской документации, 3 — предшествующего наблюдения '
                                               'за больным(ой), 4 — вскрытия)')

    deathReasonMainMKBId = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                    'приведшее к смерти. МКБ')
    deathReasonMain = Column(String(150),
                             comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно приведшее к смерти')
    deathReasonMainPeriod_Year = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                          'приведшее к смерти. Период между началом патологического '
                                                          'процесса и смертью, Годы')
    deathReasonMainPeriod_Month = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                           'приведшее к смерти. Период между началом патологического '
                                                           'процесса и смертью, Месяцы')
    deathReasonMainPeriod_Week = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                          'приведшее к смерти. Период между началом патологического '
                                                          'процесса и смертью, Недели')
    deathReasonMainPeriod_Day = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                         'приведшее к смерти. Период между началом патологического '
                                                         'процесса и смертью, Дни')
    deathReasonMainPeriod_Hour = Column(String16, comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                          'приведшее к смерти. Период между началом патологического '
                                                          'процесса и смертью, Часы')
    deathReasonMainPeriod_Minutes = Column(String16,
                                           comment='1.10.I.а, 2.19.I.а. Болезнь или состояние, непосредственно '
                                                   'приведшее к смерти. Период между началом патологического '
                                                   'процесса и смертью, Минуты')
    deathReasonCauseMKBId = Column(String16, comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                     'к возникновению вышеуказанной причины МКБ')
    deathReasonCause = Column(String(150), comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело к '
                                                   'возникновению вышеуказанной причины')
    deathReasonCausePeriod_Year = Column(String16,
                                         comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                 'к возникновению вышеуказанной причины, Годы')
    deathReasonCausePeriod_Month = Column(String16,
                                          comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                  'к возникновению вышеуказанной причины, Месяцы')
    deathReasonCausePeriod_Week = Column(String16,
                                         comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                 'к возникновению вышеуказанной причины, Недели')
    deathReasonCausePeriod_Day = Column(String16,
                                        comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                'к возникновению вышеуказанной причины, Дни')
    deathReasonCausePeriod_Hour = Column(String16,
                                         comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                 'к возникновению вышеуказанной причины, Часы')
    deathReasonCausePeriod_Minutes = Column(String16,
                                            comment='1.10.I.б, 2.19.I.б. Патологическое состояние, которое привело '
                                                    'к возникновению вышеуказанной причины, Минуты')
    deathReasonFirstMKBId = Column(String16, comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается  '
                                                     'последней. МКБ')
    deathReasonFirst = Column(String(150), comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается '
                                                   'последней.')
    deathReasonFirstPeriod_Year = Column(String16,
                                         comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается '
                                                 'последней. Годы')
    deathReasonFirstPeriod_Month = Column(String16,
                                          comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается '
                                                  'последней. Месяцы')
    deathReasonFirstPeriod_Week = Column(String16,
                                         comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается '
                                                 'последней. Недели')
    deathReasonFirstPeriod_Day = Column(String16,
                                        comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается'
                                                'последней. Дни')
    deathReasonFirstPeriod_Hour = Column(String16,
                                         comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается'
                                                 'последней. Часы')
    deathReasonFirstPeriod_Minutes = Column(String16,
                                            comment='1.10.I.в, 2.19.I.в. Первоначальная  причина смерти  указывается'
                                                    'последней. Минуты')
    deathReasonOuterMKBId = Column(String16,
                                   comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и отравлениях. МКБ')
    deathReasonOuter = Column(String(150), comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и отравлениях.')
    deathReasonOuterPeriod_Year = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                           'отравлениях. Годы')
    deathReasonOuterPeriod_Month = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                            'отравлениях. Месяцы')
    deathReasonOuterPeriod_Week = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                           'отравлениях. Недели')
    deathReasonOuterPeriod_Day = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                          'отравлениях. Дни')
    deathReasonOuterPeriod_Hour = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                           'отравлениях. Часы')
    deathReasonOuterPeriod_Minutes = Column(String16, comment='1.10.I.г, 2.19.I.г. Внешняя причина при травмах и '
                                                              'отравлениях. Минуты')
    deathReasonOtherMKBId = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. МКБ')
    deathReasonOther = Column(String(150), comment='1.10.II, 2.19.II. Прочие важные состояния.')
    deathReasonOtherPeriod_Year = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Годы')
    deathReasonOtherPeriod_Month = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Месяцы')
    deathReasonOtherPeriod_Week = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Недели')
    deathReasonOtherPeriod_Day = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Дни')
    deathReasonOtherPeriod_Hour = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Часы')
    deathReasonOtherPeriod_Minutes = Column(String16, comment='1.10.II, 2.19.II. Прочие важные состояния. Минуты')

    deathComeDTPPeriod = Column(Integer, comment='1.11, 2.20. В случае смерти в результате ДТП (1 — ничего, 2 — смерть '
                                                 'наступила в течение 30 суток)')

    deathComeDTPPeriod_7days = Column(Integer,
                                      comment='1.11, 2.20. В случае смерти в результате ДТП (1 - наступила в течение 7 суток)')
    pregnantDeath = Column(Integer, comment='1.12, 2.21. В случае смерти беременной (1 — в процессе родов(аборта),'
                                            ' 2 — В течение 42 дней после окончания беременности, 3 — в течение '
                                            '365 дней после окончания беременности)')

    prevCertId = Column(Integer, ForeignKey('DeathCertificate.id'), primary_key=False,
                        comment='Ссылка на прошлый сертификат')
    prevCert = db.relationship('DeathCertificateModel', foreign_keys=[prevCertId])

    privatePractitionerDoctorPost_id = Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                                              comment='Должность частнопрактикующего врача')
    privatePractitionerDoctorPost = db.relationship('PostModel', foreign_keys=[privatePractitionerDoctorPost_id])
    privatePractitionerDoctorFamilyName = Column(String64, comment='Фамилия частнопрактикующего врача')
    privatePractitionerDoctorFirstName = Column(String64, comment='Имя частнопрактикующего врача')
    privatePractitionerDoctorMiddleName = Column(String64, comment='Отчество частнопрактикующего врача')
    choiceDoctorOrMedicalOrganisation = Column(Integer,
                                               comment='Выбор между руководителем мед. организации и частнопракт. врачом. 0 - Руководитель, 1 - частнопракт. врач.')

    noAccurateDATOD = Column(Integer, comment='Точная дата смерти не известна')
    approximatelyDATOD = Column(String64, comment='Дата смерти (строкой)')

    filledByRelatives = Column(Integer, comment='Заполнено со слов родственников')
    filledByRelativesMother = Column(Integer, comment='Заполнено со слов родственников матери')
    filledByProtocol = Column(Integer, comment='Заполнено на основании протокола')
    filledByAccompDocuments = Column(Integer, comment='Заполнено на основании сопроводительных документов')

    organisation_id = Column(Integer, ForeignKey('Organisation.id'), primary_key=False,
                             comment='Организация, выдавшая сертификат')
    organisation = db.relationship('OrganisationModel', foreign_keys=[organisation_id])

    childBirthPlace = Column(String128, comment='Дата рождения в свободной форме')

    traumaDate_Y = Column(YearInt, comment='Дата травмы(отравления) (год)')
    traumaDate_M = Column(MonthInt, comment='Дата травмы(отравления) (месяц)')
    traumaDate_D = Column(DayInt, comment='Дата травмы(отравления) (день)')
    traumaTime = Column(Time, comment='Время травмы(отравления)')

    @property
    def full_name(self):
        return combine_name(self.familyName, self.firstName, self.middleName)

    @property
    def age_days(self):
        if self.deathDate is not None and self.birthDate is not None:
            return (self.deathDate - self.birthDate).days
        return 0

    @property
    def age_months(self):
        if self.deathDate is not None and self.birthDate is not None:
            return relativedelta(self.deathDate, self.birthDate).months
        return 0

    @classmethod
    def get_serial(cls, year=None):
        if year is None:
            year = datetime.date.today().year
        return '24С{}'.format(year % 100)

    @property
    def birthDate(self):
        return combine_date(self.birthDate_Y, self.birthDate_M, self.birthDate_D)

    @property
    def deathDate(self):
        return combine_date(self.deathDate_Y, self.deathDate_M, self.deathDate_D)

    @property
    def motherDOB(self):
        return combine_date(self.motherDOB_Y, self.motherDOB_M, self.motherDOB_D)

    @property
    def mother_name(self):
        return ' '.join(it for it in (self.motherFamilyName, self.motherFirstName, self.motherMiddleName) if it)

    @property
    def deathReasonMainPeriod(self):
        return format_period(self.deathReasonMainPeriod_Year, self.deathReasonMainPeriod_Month,
                             self.deathReasonMainPeriod_Week, self.deathReasonMainPeriod_Day,
                             self.deathReasonMainPeriod_Hour, self.deathReasonMainPeriod_Minutes)

    @property
    def deathReasonCausePeriod(self):
        return format_period(self.deathReasonCausePeriod_Year, self.deathReasonCausePeriod_Month,
                             self.deathReasonCausePeriod_Week, self.deathReasonCausePeriod_Day,
                             self.deathReasonCausePeriod_Hour, self.deathReasonCausePeriod_Minutes)

    @property
    def deathReasonFirstPeriod(self):
        return format_period(self.deathReasonFirstPeriod_Year, self.deathReasonFirstPeriod_Month,
                             self.deathReasonFirstPeriod_Week, self.deathReasonFirstPeriod_Day,
                             self.deathReasonFirstPeriod_Hour, self.deathReasonFirstPeriod_Minutes)

    @property
    def deathReasonOuterPeriod(self):
        return format_period(self.deathReasonOuterPeriod_Year, self.deathReasonOuterPeriod_Month,
                             self.deathReasonOuterPeriod_Week, self.deathReasonOuterPeriod_Day,
                             self.deathReasonOuterPeriod_Hour, self.deathReasonOuterPeriod_Minutes)

    @property
    def deathReasonOtherPeriod(self):
        return format_period(self.deathReasonOtherPeriod_Year, self.deathReasonOtherPeriod_Month,
                             self.deathReasonOtherPeriod_Week, self.deathReasonOtherPeriod_Day,
                             self.deathReasonOtherPeriod_Hour, self.deathReasonOtherPeriod_Minutes)

    @property
    def traumaDate(self):
        return combine_date(self.traumaDate_Y, self.traumaDate_M, self.traumaDate_D)

    @property
    def doctorWhoTakeDeathReasonName(self):
        return combine_name(self.doctorWhoTakeDeathReasonFamilyName,
                            self.doctorWhoTakeDeathReasonFirstName,
                            self.doctorWhoTakeDeathReasonMiddleName)

    related_columns = [
        ('updateUserLogin', str(UserModel.login.type)),
    ]

    def to_json(self):
        res = super().to_json()
        res['data'].extend([
            self.updateUserLogin
        ])
        return res

    def as_dict_with_row_id(self):
        res = super().as_dict_with_row_id()
        res['updateUserLogin'] = self.updateUserLogin
        return res
