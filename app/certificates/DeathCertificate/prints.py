import datetime
from collections import defaultdict

from dateutil.relativedelta import relativedelta
from flask import render_template

from app.Utils import CertStatus
from app.certificates.DeathCertificate.models import DeathCertificateModel
from app.certificates.util import checkbox, month_name, underline_if, underlined, underlined_style, underlined_width, LocType, format_time
from app.refbooks.Address.views import get_address_object_by_guid


def print_certificate(cert: DeathCertificateModel,
                      for_test=False,
                      for_test_text=''):
    isL1Y = cert.isChildBeforeMonth or cert.isChildBeforeYear

    b_region = get_address_object_by_guid(cert.childRegion) if cert.childRegion is not None else None
    b_city = get_address_object_by_guid(cert.childCity) if cert.childCity is not None else None

    reg_region = get_address_object_by_guid(cert.registryRegion) if cert.registryRegion is not None else None
    reg_area = get_address_object_by_guid(cert.registryArea) if cert.registryArea is not None else None
    reg_city = get_address_object_by_guid(cert.registryCity) if cert.registryCity is not None else None
    reg_street = get_address_object_by_guid(cert.registryStreet) if cert.registryStreet is not None else None

    d_region = get_address_object_by_guid(cert.deathRegion) if cert.deathRegion is not None else None
    d_area = get_address_object_by_guid(cert.deathArea) if cert.deathArea is not None else None
    d_city = get_address_object_by_guid(cert.deathCity) if cert.deathCity is not None else None
    d_street = get_address_object_by_guid(cert.deathStreet) if cert.deathStreet is not None else None

    m_age = relativedelta(datetime.date.today(), cert.motherDOB).years if cert.motherDOB else None

    prev = cert.prevCert[0] if cert.prevCert else None  # type: DeathCertificateModel
    org = cert.organisation

    undef = cert.isUnidentified
    bd_undef = undef or any((cert.birthDate_D, cert.birthDate_M, cert.birthDate_Y)) and cert.birthDate is None
    dd_undef = undef or any((cert.deathDate_D, cert.deathDate_M, cert.deathDate_Y)) and cert.deathDate is None
    rp_undef = cert.isRegistryUnidentified == 1
    dp_undef = cert.isDeathPlaceUnidentified == 1

    context = {
        'ch': checkbox,
        'u': underline_if,
        'un': underlined,
        'us': underlined_style,
        'uw': underlined_width,
        'month_name': month_name,
        'ORGNAME': org.name if org and org.name else '',
        'OKPO': org.okpo if org and org.okpo else '',
        'OADDR': org.address if org and org.address else '',
        'S': cert.status,
        'T': cert.type,
        'IFINAL': prev.type == 1 if prev is not None else '',
        'IPRELIM': prev.type == 0 if prev is not None else '',
        'SERIAL': cert.serial if cert.serial else '',  # Серия сертификата
        'NUMBER': cert.number if cert.number else '',  # Номер сертификата
        'DDD': cert.deliveryDate_D if cert.deliveryDate_D else '',  # Дата выдачи сертификата
        'DDM': month_name(cert.deliveryDate_M, True) if cert.deliveryDate_M else '',  # Дата выдачи сертификата
        'DDY': cert.deliveryDate_Y if cert.deliveryDate_Y else '',  # Дата выдачи сертификата
        'P_T': prev.type if prev else '',
        'P_SERIAL': prev.serial if prev and prev.serial else '',
        'P_NUMBER': prev.number if prev and prev.number else '',
        'P_DDD': prev.deliveryDate_D if prev and prev.deliveryDate_D else '',
        'P_DDM': month_name(prev.deliveryDate_M, True) if prev and prev.deliveryDate_M else '',
        'P_DDY': prev.deliveryDate_Y if prev and prev.deliveryDate_Y else '',
        'FULL_NAME': cert.full_name or ('не установлено' if undef else ''),
        'P': cert.sex,
        'BDD': cert.birthDate_D or ('XX' if bd_undef else ''),
        'BDM': month_name(cert.birthDate_M) or ('XXXX' if bd_undef else ''),
        'BDY': cert.birthDate_Y or ('XXXX' if bd_undef else ''),
        'LE1': isL1Y,
        'DD_D': cert.deathDate_D or ('XX' if dd_undef else ''),
        'DD_M': month_name(cert.deathDate_M) or ('XXXX' if dd_undef else ''),
        'DD_Y': cert.deathDate_Y or ('XXXX' if dd_undef else ''),
        'DD_T': format_time(cert.deathTime, undefined=dd_undef),
        'MRR': reg_region['obj'] if reg_region else ('XXXXXX' if rp_undef else ''),  # Место постоянного жительства. Область
        'MRA': reg_area['obj'] if reg_area else ('XXXXXXXX' if rp_undef else ''),  # Место постоянного жительства. Район
        'MRC': reg_city['obj'] if reg_city and cert.registryLocality == LocType.City else ('XXXXXXXX' if rp_undef else ''),
        # Место постоянного жительства. Город
        'MRL': reg_city['obj'] if reg_city and cert.registryLocality != LocType.City else ('XXXXXXXX' if rp_undef else ''),
        'MRS': reg_street['obj'] if reg_street else ('XXXXXXXX' if rp_undef else ''),  # Место постоянного жительства. Улица
        'MRH': cert.registryHouse if cert.registryHouse else ('XXX' if rp_undef else ''),  # Место постоянного жительства. Дом
        'MRF': cert.registryFlat if cert.registryFlat else ('XXX' if rp_undef else ''),  # Место постоянного жительства. Квартира
        'LOC': cert.registryLocality,
        'DP': cert.deathPlace or '',
        'BDD1': cert.birthDate_D if isL1Y else ('XX' if undef else ''),
        'BDM1': cert.birthDate_M if isL1Y else ('XXXX' if undef else ''),
        'BDY1': cert.birthDate_Y if isL1Y else ('XXXX' if undef else ''),
        'AGE_MONTHS': cert.age_months if isL1Y and cert.age_months else '',
        'AGE_DAYS': cert.age_days if isL1Y and cert.age_days else '',
        'B_PLACE': ' '.join((b_region['obj'] if b_region else '', b_city['obj'] if b_city else '')),
        'M_NAME': cert.mother_name if isL1Y else '',
        'DPR': d_region['obj'] if d_region else ('XXXXXXXX' if dp_undef else ''),
        'DPA': d_area['obj'] if d_area else ('XXXXXXXX' if dp_undef else ''),
        'DPC': d_city['obj'] if d_city and cert.deathLocality == LocType.City else ('XXXXXXXX' if dp_undef else ''),
        'DPL': d_city['obj'] if d_city and cert.deathLocality != LocType.City else ('XXXXXXXX' if dp_undef else ''),
        'DPS': d_street['obj'] if d_street else ('XXXXXXXX' if dp_undef else ''),
        'DPH': cert.deathHouse if cert.deathHouse else ('XXX' if dp_undef else ''),
        'DPF': cert.deathFlat if cert.deathFlat else ('XXX' if dp_undef else ''),
        'DLOC': cert.deathLocality,
        'CP': cert.childParameters,
        'MMS': cert.motherMartialStatus,
        'ME': cert.motherEducation,
        'MW': cert.motherWork,
        'DR': cert.deathReason,
        'CBM_W': cert.childBeforeMonthWeight or '',
        'CBY_W': cert.childBeforeYearWeight or cert.childBeforeMonthWeight or '',
        'CBM_N': cert.childBeforeMonthNumber or '',
        'CBY_N': cert.childBeforeYearNumber or cert.childBeforeMonthNumber or '',
        'M_BDY': cert.motherDOB_Y,
        'M_BDM': cert.motherDOB_M,
        'M_BDD': cert.motherDOB_D,
        'M_DOB': cert.motherDOB.strftime('%d.%m.%Y') if cert.motherDOB else '',
        'M_AGE': m_age or '',
        'M_FAM': cert.motherFamilyName if cert.motherFamilyName and isL1Y else '',
        'M_NAME1': cert.motherFirstName if cert.motherFirstName and isL1Y else '',
        'M_NAME2': cert.motherMiddleName if cert.motherMiddleName and isL1Y else '',
        'DR1': cert.deathReasonMain if cert.deathReasonMain else '',
        'DP1': cert.deathReasonMainPeriod,
        'MKB1': cert.deathReasonMainMKBId or '',
        'DR2': cert.deathReasonCause if cert.deathReasonCause else '',
        'DP2': cert.deathReasonCausePeriod,
        'MKB2': cert.deathReasonCauseMKBId or '',
        'DR3': cert.deathReasonFirst if cert.deathReasonFirst else '',
        'DP3': cert.deathReasonFirstPeriod,
        'MKB3': cert.deathReasonFirstMKBId or '',
        'DR4': cert.deathReasonOuter if cert.deathReasonOuter else '',
        'DP4': cert.deathReasonOuterPeriod,
        'MKB4': cert.deathReasonOuterMKBId or '',
        'DR5': cert.deathReasonOther if cert.deathReasonOther else '',
        'DP5': cert.deathReasonOtherPeriod,
        'MKB5': cert.deathReasonOtherMKBId or '',
        'DTP': cert.deathComeDTPPeriod,
        'DTP7': cert.deathComeDTPPeriod_7days,
        'PREGD': cert.pregnantDeath,
        'WTD': cert.whoTakeDeathReason,
        'WTD_NAME': cert.doctorWhoTakeDeathReasonName,
        'WTD_POST': cert.doctorWhoTakeDeathReasonPost.name if cert.doctorWhoTakeDeathReasonPost is not None else '',
        'DRB': cert.deathReasonBased,
        'FILLNAME': cert.doctorWhoFillCertificateName,
        'HEADNAME': cert.medicalOrganisationHeadName,
        'CHECKNAME': cert.doctorWhoCheckedCertificateName,
        'RNAME': cert.recipientName,
        'RDOC': cert.recipientDocument,
        'M_CHOICE': cert.choiceDoctorOrMedicalOrganisation,
        'TD_Y': cert.traumaDate_Y,
        'TD_M': cert.traumaDate_M,
        'TD_D': cert.traumaDate_D,
        'TD_T': format_time(cert.traumaTime),
        'TRAUMA': cert.deathTraumaDetails,
        'FILLED_BY': ('Заполнено со слов родственников' if cert.filledByRelatives or cert.filledByRelativesMother else
                      'Заполнено на основании протокола' if cert.filledByProtocol else
                      'Заполнено на основании сопроводительных документов' if cert.filledByAccompDocuments else ''),
        'FOR_TEST': for_test or cert.status not in (CertStatus.SIGNED.value, CertStatus.EMPTY.value),
        'FOR_TEST_TEXT': for_test_text or 'для проверки',
        'EMPTY': not undef
    }

    return render_template('DeathCertificate.html', **context)


def print_empty_certificate(cert: DeathCertificateModel):
    context = defaultdict(str)
    context.update({
        'ch': checkbox,
        'u': underline_if,
        'un': underlined,
        'us': underlined_style,
        'uw': underlined_width,
        'month_name': month_name,
        'OKPO': '',
        'OADDR': '',
        'S': '',
        'T': '',
        'IFINAL': '',
        'IPRELIM': '',
        'SERIAL': cert.serial if cert.serial else '',  # Серия сертификата
        'NUMBER': cert.number if cert.number else '',  # Номер сертификата
        'DDD': '',
        'DDM': '',  # Дата выдачи сертификата
        'DDY': '',  # Дата выдачи сертификата
        'P_T': '',
        'P_SERIAL': '',
        'P_NUMBER': '',
        'P_DDD': '',
        'P_DDM': '',
        'P_DDY': '',
        'FULL_NAME': '',
        'P': '',
        'BDD': '',
        'BDM': '',
        'BDY': '',
        'LE1': '',
        'DD_D': '',
        'DD_M': '',
        'DD_Y': '',
        'DD_T': '',
        'MRR': '',  # Место постоянного жительства. Область
        'MRA': '',  # Место постоянного жительства. Район
        'MRC': '',
        # Место постоянного жительства. Город
        'MRL': '',
        'MRS': '',  # Место постоянного жительства. Улица
        'MRH': '',  # Место постоянного жительства. Дом
        'MRF': '',  # Место постоянного жительства. Квартира
        'LOC': '',
        'DP': '',
        'BDD1': '',
        'BDM1': '',
        'BDY1': '',
        'AGE_MONTHS': '',
        'AGE_DAYS': '',
        'B_PLACE': '',
        'M_NAME': '',
        'DPR': '',
        'DPA': '',
        'DPC': '',
        'DPL': '',
        'DPS': '',
        'DPH': '',
        'DPF': '',
        'DLOC': '',
        'CP': '',
        'MMS': '',
        'ME': '',
        'MW': '',
        'DR': '',
        'CBM_W': '',
        'CBY_W': '',
        'CBM_N': '',
        'CMBY_N': '',
        'M_BDY': '',
        'M_BDM': '',
        'M_BDD': '',
        'M_DOB': '',
        'M_AGE': '',
        'M_FAM': '',
        'M_NAME1': '',
        'M_NAME2': '',
        'DR1': '',
        'DP1': '',
        'MKB1': '',
        'DR2': '',
        'DP2': '',
        'MKB2': '',
        'DR3': '',
        'DP3': '',
        'MKB3': '',
        'DR4': '',
        'DP4': '',
        'MKB4': '',
        'DR5': '',
        'DP5': '',
        'MKB5': '',
        'DTP': '',
        'DTP7': '',
        'PREGD': '',
        'WTD': '',
        'WTD_NAME': '',
        'WTD_POST': '',
        'DRB': '',
        'FILLNAME': '',
        'HEADNAME': '',
        'CHECKNAME': '',
        'RNAME': '',
        'RDOC': '',
        'M_CHOICE': '',
        'TD_Y': '',
        'TD_M': '',
        'TD_D': '',
        'TD_T': '',
        'TRAUMA': '',
        'FILLED_BY': '',
        'FOR_TEST': False,
        'EMPTY': True
    })

    return render_template('DeathCertificate.html', **context)


def print_duplicate(cert: DeathCertificateModel):
    return print_certificate(cert, True, 'дубликат')
