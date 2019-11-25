from sqlalchemy import Column, Date, String, Table, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import foreign

from app import app
from app.other.Base import db


class FIASMixin(object):
    __table_args__ = {'schema': app.config.get('FIAS_DB')}


class LocType:
    City = 1
    NonCity = 2


class ActStatus:
    Inactive = 0
    Active = 1


class ADDROBJ(db.Model, FIASMixin):
    """ Адресообразующие элементы (субъект РФ -> район -> населенный пункт -> улица) """
    __tablename__ = 'ADDROBJ'

    AOGUID = Column(String(36), nullable=False, index=True)
    FORMALNAME = Column(String(120), nullable=False, index=True)
    REGIONCODE = Column(String(2), nullable=False, index=True)
    AUTOCODE = Column(String(1), nullable=False)
    AREACODE = Column(String(3), nullable=False)
    CITYCODE = Column(String(3), nullable=False)
    CTARCODE = Column(String(3), nullable=False)
    PLACECODE = Column(String(3), nullable=False)
    PLANCODE = Column(String(4), nullable=False)
    STREETCODE = Column(String(4))
    EXTRCODE = Column(String(4), nullable=False)
    SEXTCODE = Column(String(3), nullable=False)
    OFFNAME = Column(String(120))
    POSTALCODE = Column(String(6))
    IFNSFL = Column(String(4))
    TERRIFNSFL = Column(String(4))
    IFNSUL = Column(String(4))
    TERRIFNSUL = Column(String(4))
    OKATO = Column(String(11))
    OKTMO = Column(String(11))
    UPDATEDATE = Column(Date, nullable=False)
    SHORTNAME = Column(String(10), nullable=False, index=True)
    AOLEVEL = Column(INTEGER(10), nullable=False, index=True)
    PARENTGUID = Column(String(36), index=True)
    AOID = Column(String(36), primary_key=True)
    PREVID = Column(String(36))
    NEXTID = Column(String(36))
    CODE = Column(String(17))
    PLAINCODE = Column(String(15))
    ACTSTATUS = Column(INTEGER(10), nullable=False, index=True)
    CENTSTATUS = Column(INTEGER(10), nullable=False, index=True)
    OPERSTATUS = Column(INTEGER(10), nullable=False, index=True)
    CURRSTATUS = Column(INTEGER(10), nullable=False, index=True)
    STARTDATE = Column(Date, nullable=False)
    ENDDATE = Column(Date, nullable=False)
    NORMDOC = Column(String(36), index=True)
    LIVESTATUS = Column(INTEGER(1), nullable=False)
    DIVTYPE = Column(INTEGER(11), nullable=False)

    @hybrid_property
    def obj_name(self):
        return f'{self.FORMALNAME} {self.SHORTNAME}'

    @obj_name.expression
    def obj_name(cls):
        return func.CONCAT_WS(' ', cls.FORMALNAME, cls.SHORTNAME)

    @hybrid_property
    def loc_type(self):
        return LocType.City if self.SHORTNAME.lower() in ('г', 'г.') else LocType.NonCity

    @loc_type.expression
    def loc_type(cls):
        return func.IF(cls.SHORTNAME.in_(['г', 'г.']), LocType.City, LocType.NonCity)

    parent = db.relationship('ADDROBJ', primaryjoin=PARENTGUID == foreign(AOGUID))


class CENTERST(db.Model, FIASMixin):
    """ Статус центра """
    __tablename__ = 'CENTERST'

    CENTERSTID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(100), nullable=False)


class CURENTST(db.Model, FIASMixin):
    """  Статус актуальности """
    __tablename__ = 'CURENTST'

    CURENTSTID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(100), nullable=False)


class ESTSTAT(db.Model, FIASMixin):
    """ Признак владения """
    __tablename__ = 'ESTSTAT'

    ESTSTATID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(20), nullable=False)
    SHORTNAME = Column(String(20))


FLATTYPE = Table(
    'FLATTYPE', ADDROBJ.metadata,
    Column('FLTYPEID', INTEGER(10), nullable=False),
    Column('NAME', String(20), nullable=False),
    Column('SHORTNAME', String(20))
)


class HOUSE(db.Model, FIASMixin):
    """  Сведения по номерам домов улиц городов и населенных пунктов, номера земельных участков """
    __tablename__ = 'HOUSE'

    POSTALCODE = Column(String(6))
    REGIONCODE = Column(String(2))
    IFNSFL = Column(String(4))
    TERRIFNSFL = Column(String(4))
    IFNSUL = Column(String(4))
    TERRIFNSUL = Column(String(4))
    OKATO = Column(String(11))
    OKTMO = Column(String(11))
    UPDATEDATE = Column(Date, nullable=False)
    HOUSENUM = Column(String(20))
    ESTSTATUS = Column(INTEGER(1), nullable=False, index=True)
    BUILDNUM = Column(String(10))
    STRUCNUM = Column(String(10))
    STRSTATUS = Column(INTEGER(10), index=True)
    HOUSEID = Column(String(36), primary_key=True)
    HOUSEGUID = Column(String(36), nullable=False)
    AOGUID = Column(String(36), nullable=False)
    STARTDATE = Column(Date, nullable=False)
    ENDDATE = Column(Date, nullable=False)
    STATSTATUS = Column(INTEGER(10), nullable=False, index=True)
    NORMDOC = Column(String(36), index=True)
    COUNTER = Column(INTEGER(10), nullable=False)
    CADNUM = Column(String(100))
    DIVTYPE = Column(INTEGER(11), nullable=False)


class HSTSTAT(db.Model, FIASMixin):
    """ Статус состояния объектов недвижимости """
    __tablename__ = 'HSTSTAT'

    HOUSESTID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(60), nullable=False)


class INTVSTAT(db.Model, FIASMixin):
    """ Статус интервала домов """
    __tablename__ = 'INTVSTAT'

    INTVSTATID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(60), nullable=False)


class NDOCTYPE(db.Model, FIASMixin):
    """  Тип нормативного документа (закон, приказ, справка) """
    __tablename__ = 'NDOCTYPE'

    NDTYPEID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(250), nullable=False)


class NORMDOC(db.Model, FIASMixin):
    """ Сведения по нормативному документу, являющемуся основанием присвоения адресному элементу наименования """
    __tablename__ = 'NORMDOC'

    NORMDOCID = Column(String(36), primary_key=True)
    DOCNAME = Column(String(128))
    DOCDATE = Column(Date)
    DOCNUM = Column(String(20))
    DOCTYPE = Column(INTEGER(10), nullable=False, index=True)
    DOCIMGID = Column(String(36))


class OPERSTAT(db.Model, FIASMixin):
    """ Статус действия """
    __tablename__ = 'OPERSTAT'

    OPERSTATID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(100), nullable=False)


# Помещения
ROOM = Table(
    'ROOM', ADDROBJ.metadata,
    Column('ROOMGUID', String(36), nullable=False),
    Column('FLATNUMBER', String(50), nullable=False),
    Column('FLATTYPE', INTEGER(11), nullable=False),
    Column('ROOMNUMBER', String(50)),
    Column('ROOMTYPE', INTEGER(11)),
    Column('REGIONCODE', String(2), nullable=False),
    Column('POSTALCODE', String(6)),
    Column('UPDATEDATE', Date, nullable=False),
    Column('HOUSEGUID', String(36), nullable=False),
    Column('ROOMID', String(36), nullable=False),
    Column('PREVID', String(36)),
    Column('NEXTID', String(36)),
    Column('STARTDATE', Date, nullable=False),
    Column('ENDDATE', Date, nullable=False),
    Column('LIVESTATUS', INTEGER(1), nullable=False),
    Column('NORMDOC', String(36)),
    Column('OPERSTATUS', INTEGER(10), nullable=False),
    Column('CADNUM', String(100)),
    Column('ROOMCADNUM', String(100))
)

# Типы помещений
ROOMTYPE = Table(
    'ROOMTYPE', ADDROBJ.metadata,
    Column('RMTYPEID', INTEGER(10), nullable=False),
    Column('NAME', String(20), nullable=False),
    Column('SHORTNAME', String(20))
)

# Типы адресных объектов (условные сокращения и уровни подчинения)
SOCRBASE = Table(
    'SOCRBASE', ADDROBJ.metadata,
    Column('LEVEL', INTEGER(10), nullable=False),
    Column('SCNAME', String(10), index=True),
    Column('SOCRNAME', String(50), nullable=False),
    Column('KOD_ST', String(4), nullable=False)
)

# Земельные участки
STEAD = Table(
    'STEAD', ADDROBJ.metadata,
    Column('STEADGUID', String(36), nullable=False),
    Column('NUMBER', String(120)),
    Column('REGIONCODE', String(2), nullable=False),
    Column('POSTALCODE', String(6)),
    Column('IFNSFL', String(4)),
    Column('TERRIFNSFL', String(4)),
    Column('IFNSUL', String(4)),
    Column('TERRIFNSUL', String(4)),
    Column('OKATO', String(11)),
    Column('OKTMO', String(11)),
    Column('UPDATEDATE', Date, nullable=False),
    Column('PARENTGUID', String(36)),
    Column('STEADID', String(36), nullable=False),
    Column('PREVID', String(36)),
    Column('NEXTID', String(36)),
    Column('OPERSTATUS', INTEGER(10), nullable=False),
    Column('STARTDATE', Date, nullable=False),
    Column('ENDDATE', Date, nullable=False),
    Column('NORMDOC', String(36)),
    Column('LIVESTATUS', INTEGER(1), nullable=False),
    Column('CADNUM', String(100)),
    Column('DIVTYPE', INTEGER(11), nullable=False)
)


class STRSTAT(db.Model, FIASMixin):
    """ Признак строения """
    __tablename__ = 'STRSTAT'

    STRSTATID = Column(INTEGER(10), primary_key=True)
    NAME = Column(String(20), nullable=False)
    SHORTNAME = Column(String(20))
