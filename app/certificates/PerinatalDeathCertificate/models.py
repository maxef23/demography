import datetime

from app.certificates.util import BaseCertificate, combine_date
from app.other import UserModel
from app.other.Base import *

TEMPLATE = 'PerinatalDeathCertificate.html'


class PerinatalDeathCertificateModel(db.Model, ModelMixIn, BaseCertificate):
    __tablename__ = 'PerinatalDeathCertificate'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Форма 106-2/у-08'}

    counter_code = 'pdc_counter'

    id = Column(Integer, primary_key=True)

    type = Column(Integer, comment='Тип свидетельства. 0 — предварительное, 1 — окончательное, '
                                   '2 — взамен предварительного, 3 — взамен окончательного')

    previousCertificateSerial = Column(String64, comment='Серия предыдущего документа')
    previousCertificateNumber = Column(String64, comment='Номер предыдущего документа')
    previousCertificateDeliveryDate_Y = Column(YearInt, comment='Дата выдачи предыдущего документа (год)')
    previousCertificateDeliveryDate_M = Column(MonthInt, comment='Дата выдачи предыдущего документа (месяц)')
    previousCertificateDeliveryDate_D = Column(DayInt, comment='Дата выдачи предыдущего документа (день)')

    perinatalDeathDate_Y = Column(YearInt, nullable=True, comment='1.1. Дата родов мёртвым плодом (год)')
    perinatalDeathDate_M = Column(MonthInt, nullable=True, comment='1.1. Дата родов мёртвым плодом (месяц)')
    perinatalDeathDate_D = Column(DayInt, nullable=True, comment='1.1. Дата родов мёртвым плодом (день)')
    perinatalDeathTime = Column(Time, nullable=True, comment='1.1. Время родов мёртвым плодом')
    birthDatetime_Y = Column(YearInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата рождения')
    birthDatetime_M = Column(MonthInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата рождения')
    birthDatetime_D = Column(DayInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата рождения')
    birthTime = Column(Time, nullable=True, comment='1.2. Ребёнок родился живым. Время рождения')
    deathDate_Y = Column(YearInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата смерти (год)')
    deathDate_M = Column(MonthInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата смерти (месяц)')
    deathDate_D = Column(DayInt, nullable=True, comment='1.2. Ребёнок родился живым. Дата смерти (день)')
    deathTime = Column(Time, nullable=True, comment='1.2. Ребёнок родился живым. Время смерти')
    death = Column(Integer, comment='1.3. Смерть наступила ('
                                    '1 — да начала родов, '
                                    '2 — во время родов, '
                                    '3 — после родов, '
                                    '4 — неизвестно)')

    motherFamilyName = Column(String64, comment='1.4. Фамилия матери')
    motherFirstName = Column(String64, comment='1.4. Имя матери')
    motherMiddleName = Column(String64, comment='1.4. Отчество матери')
    motherDOB_Y = Column(YearInt, nullable=True, comment='1.5. Дата рождения матери (год)')
    motherDOB_M = Column(MonthInt, nullable=True, comment='1.5. Дата рождения матери (месяц)')
    motherDOB_D = Column(DayInt, nullable=True, comment='1.5. Дата рождения матери (день)')
    motherRegistryRegion = Column(String64, comment='1.4. Место постоянного жительства матери. Область')
    motherRegistryArea = Column(String64, comment='1.4. Место постоянного жительства матери. Район')
    motherRegistryCity = Column(String64, comment='1.4. Место постоянного жительства матери. Город')
    motherRegistryStreet = Column(String64, comment='1.4. Место постоянного жительства матери. Улица')
    motherRegistryHouse = Column(String64, comment='1.4. Место постоянного жительства матери. Дом')
    motherRegistryFlat = Column(String64, comment='1.4. Место постоянного жительства матери. Квартира')
    locality = Column(Integer, comment='1.5. Местность (1 — городская, 2 — сельская)')
    sex = Column(Integer, comment='1.6. Пол (1 — мальчик, 2 — девочка)')
    deathPlace = Column(Integer,
                        comment='1.10. Смерть произошла (1 — в стационаре, 2 — дома, 3 — в другом месте)')

    deathReasonMainMKBId = Column(String16,
                                  comment='1.11.а. Основное заболевание или патологическое состояние плода или ребенка. МКБ')
    deathReasonMain = Column(String(150),
                             comment='1.11.а. Основное заболевание или патологическое состояние плода или ребенка')
    deathReasonOtherMKBId = Column(String16,
                                   comment='1.11.б. Другие заболевания или патологические состояния плода или ребенка. MKB')
    deathReasonOther = Column(String(150),
                              comment='1.11.б. Другие заболевания или патологические состояния плода или ребенка')
    deathReasonMotherMainMKBId = Column(String16,
                                        comment='1.11.в. Основное заболевание или патологическое состояние матери, оказавшее неблагоприятное влияние на плод или ребенка. МКБ')
    deathReasonMotherMain = Column(String(150),
                                   comment='1.11.в. Основное заболевание или патологическое состояние матери, оказавшее неблагоприятное влияние на плод или ребенка')
    deathReasonMotherOtherMKBId = Column(String16,
                                         comment='1.11.г. Другие заболевания или патологические состояния матери, оказавшее неблагоприятное влияние на плод или ребенка. МКБ')
    deathReasonMotherOther = Column(String(150),
                                    comment='1.11.г. Другие заболевания или патологические состояния матери, оказавшее неблагоприятное влияние на плод или ребенка')
    deathReasonOtherFacts = Column(String64,
                                   comment='1.11.д. Другие обстоятельства, имевшие отношение к мертворождению, смерти')

    motherLocality = Column(Integer, comment='2.5. Местность (1 — городская, 2 — сельская)')
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

    parturitionNumber = Column(Integer, comment='2.11. Которые по счету роды')
    childFamilyName = Column(String64, comment='2.11. Фамилия ребёнка')
    childBirthRegion = Column(String64, comment='2.12. Место рождения ребёнка. Область')
    childBirthArea = Column(String64, comment='2.12. Место рождения ребёнка. Район')
    childBirthCity = Column(String64, comment='2.12. Место рождения ребёнка. Город')
    childWeight = Column(Integer, comment='2.16. Масса тела при рождении. Граммы')
    childLength = Column(Integer, comment='2.17. Длина тела при рождении. Сантиметры')
    singleFetus = Column(Integer, comment='2.18. Ребёнок родился при одноплодных родах')
    multipleFetusNumber = Column(Integer, comment='2.18. Ребёнок родился при многоплодных родах. Номер по счёту')
    multipleFetusCount = Column(Integer, comment='2.18. Ребёнок родился при многоплодных родах. Число родившихся')
    childNumber = Column(Integer, comment='2.10. Которым по счету ребёнок является у матери')
    whoTakeBirth = Column(Integer, comment='2.19. Лицо, принимавшее роды (1 — врач-акушер-гинеколог, '
                                           '2 — фельдшер, акушерка, 3 — другое лицо)')

    childDeathReason = Column(Integer,
                              comment='Смерть ребенка (плода) произошла: 1 - от заболевания;'
                                      ' 2 - несчастного случая; 3 - убийства; 4 - род смерти не установлен')

    whoTakeDeathReason = Column(Integer,
                                comment='2.24. Причины смерти установлены (1 — врачом, только что установившим смерть, 2 — врачом-акушером-гинекологом, принимавшим роды, 3 — врачом-неонатологом (педиатром), лечившим ребёнка, 4 — врачом-патологоанатомом, 5 — судебно-медицинским экспертом, 6 — акушеркой, 7 — фельдшером)')
    baseTakeDeathReason = Column(Integer,
                                 comment='2.24. На основании (1 — осмотра трупа, 2 — записей в медицинской документации, 3 — наблюдения, 4 — вскрытия)')

    prevCertId = Column(Integer, ForeignKey('PerinatalDeathCertificate.id'), primary_key=False,
                        comment='Ссылка на прошлый сертификат')
    prevCert = db.relationship('PerinatalDeathCertificateModel', foreign_keys=[prevCertId])

    privatePractitionerDoctorPost_id = Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                                              comment='Должность частнопрактикующего врача')
    privatePractitionerDoctorPost = db.relationship('PostModel', foreign_keys=[privatePractitionerDoctorPost_id])
    privatePractitionerDoctorFamilyName = Column(String64, comment='Фамилия частнопрактикующего врача')
    privatePractitionerDoctorFirstName = Column(String64, comment='Имя частнопрактикующего врача')
    privatePractitionerDoctorMiddleName = Column(String64, comment='Отчество частнопрактикующего врача')
    choiceDoctorOrMedicalOrganisation = Column(Integer,
                                               comment='Выбор между руководителем мед. организации и частнопракт. врачом. 0 - Руководитель, 1 - Частнопракт. врач.')

    noAccurateDATOD = Column(Integer, comment='Точная дата смерти не известна')
    approximatelyDATOD = Column(String64, comment='Дата смерти (строкой)')

    organisation_id = Column(Integer, ForeignKey('Organisation.id'), primary_key=False,
                             comment='Организация, выдавшая сертификат')
    organisation = db.relationship('OrganisationModel', foreign_keys=[organisation_id])

    @classmethod
    def get_serial(cls, year=None):
        if year is None:
            year = datetime.date.today().year
        return u'24ПС{}'.format(year % 100)

    @property
    def previousCertificateDeliveryDate(self):
        return combine_date(self.previousCertificateDeliveryDate_Y,
                            self.previousCertificateDeliveryDate_M,
                            self.previousCertificateDeliveryDate_D)

    @property
    def perinatalDeathDate(self):
        return combine_date(self.perinatalDeathDate_Y, self.perinatalDeathDate_M, self.perinatalDeathDate_D)

    @property
    def birthDatetime(self):
        return combine_date(self.birthDatetime_Y, self.birthDatetime_M, self.birthDatetime_D)

    @property
    def deathDate(self):
        return combine_date(self.deathDate_Y, self.deathDate_M, self.deathDate_D)

    @property
    def mother_name(self):
        return ' '.join(it for it in (self.motherFamilyName, self.motherFirstName, self.motherMiddleName) if it)

    @property
    def motherDOB(self):
        return combine_date(self.motherDOB_Y, self.motherDOB_M, self.motherDOB_D)

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
