import datetime

from app.certificates.util import BaseCertificate, combine_date, combine_name
from app.other import UserModel
from app.other.Base import *


class BirthCertificateModel(db.Model, ModelMixIn, BaseCertificate):
    __tablename__ = 'BirthCertificate'
    __table_args__ = {'mysql_engine': 'InnoDB', 'comment': 'Форма 103/у'}

    counter_code = 'bc_counter'

    id = Column(Integer, primary_key=True)

    childDATOB_Y = Column(YearInt, comment='1.1. Дата рождения ребёнка (год)')
    childDATOB_M = Column(MonthInt, comment='1.1. Дата рождения ребёнка (месяц)')
    childDATOB_D = Column(DayInt, comment='1.1. Дата рождения ребёнка (день)')
    childTIMEOB = Column(Time, nullable=True, comment='1.1. Время рождения ребёнка')

    isMotherUnidentified = Column(Integer, comment='Личность матери не установлена. 0 — нет, 1 — да')
    isMotherRegistryUnidentified = Column(Integer, comment='Место регистрации матери не установлено. 0 — нет, 1 — да')
    motherSNILS = Column(String64, comment='1.*** Снилс матери')
    motherFamilyName = Column(String64, comment='1.2. Фамилия матери')
    motherFirstName = Column(String64, comment='1.2. Имя матери')
    motherMiddleName = Column(String64, comment='1.2. Отчество матери')
    motherDOB_Y = Column(YearInt, comment='1.3. Дата рождения матери (год)')
    motherDOB_M = Column(MonthInt, comment='1.3. Дата рождения матери (месяц)')
    motherDOB_D = Column(DayInt, comment='1.3. Дата рождения матери (день)')
    motherRegistryRegion = Column(String64, comment='1.4. Место постоянного жительства матери. Область')
    motherRegistryArea = Column(String64, comment='1.4. Место постоянного жительства матери. Район')
    motherRegistryCity = Column(String64, comment='1.4. Место постоянного жительства матери. Город')
    motherRegistryStreet = Column(String64, comment='1.4. Место постоянного жительства матери. Улица')
    motherRegistryHouse = Column(String64, comment='1.4. Место постоянного жительства матери. Дом')
    motherRegistryFlat = Column(String64, comment='1.4. Место постоянного жительства матери. Квартира')
    locality = Column(Integer, comment='1.5. Местность (1 — городская, 2 — сельская)')
    sex = Column(Integer, comment='1.6. Пол (1 — мальчик, 2 — девочка)')
    birthPlace = Column(Integer,
                        comment='1.7. Роды произошли (1 — в стационаре, 2 — дома, 3 — в другом месте, 4 — неизвестно)')
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
    motherAttendance = Column(Integer, comment='2.9. Срок первой явки к врачу. Недели')
    childNumber = Column(Integer, comment='2.10. Которым по счету ребёнок является у матери')

    childFamilyName = Column(String64, comment='2.11. Фамилия ребёнка')
    childBirthRegion = Column(String64, comment='2.12. Место рождения ребёнка. Область')
    childBirthArea = Column(String64, comment='2.12. Место рождения ребёнка. Район')
    childBirthCity = Column(String64, comment='2.12. Место рождения ребёнка. Город')
    childWeight = Column(Integer, comment='2.16. Масса тела при рождении. Граммы')
    childLength = Column(Integer, comment='2.17. Длина тела при рождении. Сантиметры')
    singleFetus = Column(Integer, comment='2.18. Ребёнок родился при одноплодных родах')
    multipleFetusNumber = Column(Integer, comment='2.18. Ребёнок родился при многоплодных родах. Номер по счёту')
    multipleFetusCount = Column(Integer, comment='2.18. Ребёнок родился при многоплодных родах. Число родившихся')

    whoTakeBirth = Column(Integer, comment='2.19. Лицо, принимавшее роды (1 — врач-акушер-гинеколог, '
                                           '2 — фельдшер, акушерка, 3 — другое лицо)')

    prevCertId = Column(Integer, ForeignKey('BirthCertificate.id'), primary_key=False,
                        comment='Ссылка на прошлый сертификат')

    privatePractitionerDoctorPost_id = Column(Integer, ForeignKey('rbPost.id'), primary_key=False,
                                              comment='Должность частнопрактикующего врача')
    privatePractitionerDoctorPost = db.relationship('PostModel', foreign_keys=[privatePractitionerDoctorPost_id])
    privatePractitionerDoctorFamilyName = Column(String64, comment='Фамилия частнопрактикующего врача')
    privatePractitionerDoctorFirstName = Column(String64, comment='Имя частнопрактикующего врача')
    privatePractitionerDoctorMiddleName = Column(String64, comment='Отчество частнопрактикующего врача')

    choiceDoctorOrMedicalOrganisation = Column(Integer,
                                               comment='Выбор между руководителем мед. организации и частнопракт. врачом. 0 - Руководитель, 1 - частнопракт. врач.')

    noAccurateChildDATOB = Column(Integer, comment='Точная дата рождения не известна')
    approximatelyChildDATOB = Column(String64, comment='Дата рождения (строкой)')

    filledByRelativesMother = Column(Integer, comment='Заполнено со слов родственников матери')

    organisation_id = Column(Integer, ForeignKey('Organisation.id'), primary_key=False,
                             comment='Организация, выдавшая сертификат')
    organisation = db.relationship('OrganisationModel', foreign_keys=[organisation_id])

    @classmethod
    def get_serial(cls, year=None):
        if year is None:
            year = datetime.date.today().year
        return '24Р{}'.format(year % 100)

    @property
    def childDATOB(self):
        return combine_date(self.childDATOB_Y, self.childDATOB_M, self.childDATOB_D)

    @property
    def motherDOB(self):
        return combine_date(self.motherDOB_Y, self.motherDOB_M, self.motherDOB_D)

    @property
    def motherName(self):
        return combine_name(self.motherFamilyName, self.motherFirstName, self.motherMiddleName)

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
