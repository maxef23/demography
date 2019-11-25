from collections import defaultdict

from flask import render_template

from app.Utils import CertStatus
from app.certificates.BirthCertificate.models import BirthCertificateModel
from app.certificates.util import checkbox, month_name, underline_if, underlined, underlined_style, underlined_width, format_time
from app.refbooks.Address.views import get_address_object_by_guid


def print_certificate(cert: BirthCertificateModel,
                      for_test=False,
                      for_test_text=''):
    MRR = get_address_object_by_guid(cert.motherRegistryRegion) if cert.motherRegistryRegion is not None else None
    MRA = get_address_object_by_guid(cert.motherRegistryArea) if cert.motherRegistryArea is not None else None
    MRC = get_address_object_by_guid(cert.motherRegistryCity) if cert.motherRegistryCity is not None else None
    MRS = get_address_object_by_guid(cert.motherRegistryStreet) if cert.motherRegistryStreet is not None else None
    CRR = get_address_object_by_guid(cert.childBirthRegion) if cert.childBirthRegion is not None else None
    CRA = get_address_object_by_guid(cert.childBirthArea) if cert.childBirthArea is not None else None
    CRC = get_address_object_by_guid(cert.childBirthCity) if cert.childBirthCity is not None else None

    org = cert.organisation

    context = {
        'ch': checkbox,
        'u': underline_if,
        'un': underlined,
        'uw': underlined_width,
        'us': underlined_style,
        'mon_name': month_name,
        'ORG_OKPO': org.okpo if org else '',
        'ORG_NAME': org.name if org else '',
        'ORG_ADDR': org.address if org else '',
        'MTHR_FN': cert.motherFamilyName if cert.motherFamilyName else '',  # Фамилия матери
        'MTHR_N': cert.motherFirstName if cert.motherFirstName else '',  # Имя матери
        'MTHR_SN': cert.motherMiddleName if cert.motherMiddleName else '',  # Отчество матери
        'MTHR_NSN': ' '.join(it for it in (cert.motherFirstName, cert.motherMiddleName) if it),
        'MTHR_NAME': cert.motherName,
        'M_BD': cert.motherDOB,
        'M_BDY': cert.motherDOB_Y or '',
        'M_BDM': cert.motherDOB_M or '',
        'M_BDD': cert.motherDOB_D or '',
        'SMBDY': '{:04d}'.format(cert.motherDOB_Y) if cert.motherDOB_Y else '',
        'SMBDM': '{:02d}'.format(cert.motherDOB_M) if cert.motherDOB_M else '',
        'SMBDD': '{:02d}'.format(cert.motherDOB_D) if cert.motherDOB_D else '',
        'MTHR_BD': cert.motherDOB_D if cert.motherDOB_D else '',  # День рождения матери
        'MTHR_BM': cert.motherDOB_M if cert.motherDOB_M else 0,  # Месяц рождения матери
        'MTHR_BM_N': month_name(cert.motherDOB_M) if cert.motherDOB_M else '',  # Месяц рождения матери
        'MTHR_BY': cert.motherDOB_Y if cert.motherDOB_Y else '',  # Год рождения матери
        'SERIAL': cert.serial if cert.serial else '',  # Серия сертификата
        'NUMBER': cert.number if cert.number else '',  # Номер сертификата
        'CBDY': cert.childDATOB_Y or '',
        'CBDM': cert.childDATOB_M or '',
        'CBDD': cert.childDATOB_D or '',
        'CBD': cert.childDATOB,
        'CBT_H': format_time(cert.childTIMEOB, fmt='%H'),
        'CBT_M': format_time(cert.childTIMEOB, fmt='%M'),
        'MRR': MRR['obj'] if MRR else '',  # Место постоянного жительства матери. Область
        'MRA': MRA['obj'] if MRA else '',  # Место постоянного жительства матери. Район
        'MRC': MRC['obj'] if MRC else '',  # Место постоянного жительства матери. Город
        'MRS': MRS['obj'] if MRS else '',  # Место постоянного жительства матери. Улица
        'MRH': cert.motherRegistryHouse if cert.motherRegistryHouse else '',  # Место постоянного жительства матери. Дом
        'MRF': cert.motherRegistryFlat if cert.motherRegistryFlat else '',
        # Место постоянного жительства матери. Квартира
        'CFN': cert.childFamilyName or '',
        'DDD': cert.deliveryDate_D if cert.deliveryDate_D else '',  # Дата выдачи сертификата
        'DDM': month_name(cert.deliveryDate_M, True) if cert.deliveryDate_M else '',  # Дата выдачи сертификата
        'DDY': cert.deliveryDate_Y if cert.deliveryDate_Y else '',  # Дата выдачи сертификата
        'MLOC': cert.motherLocality,
        'SEX': cert.sex,
        'MMS': cert.motherMartialStatus,
        'CRR': CRR['obj'] if CRR else '',
        'CRA': CRA['obj'] if CRA else '',
        'CRC': CRC['obj'] if CRC else '',
        'CLOC': cert.locality,
        'BP': cert.birthPlace,
        'GBC_POST': cert.doctorWhoGaveCertificatePost.name if cert.doctorWhoGaveCertificatePost else '',
        'GBC_NAME': cert.doctorWhoGaveCertificateName,
        'RNAME': cert.recipientName,
        'RDOC': cert.recipientDocument,
        'ME': cert.motherEducation,
        'MW': cert.motherWork,
        'MATT': cert.motherAttendance,
        'CN': cert.childNumber,
        'WTB': cert.whoTakeBirth,
        'CW': str(cert.childWeight) if cert.childWeight else '',
        'CL': str(cert.childLength) if cert.childLength else '',
        'SF': cert.singleFetus,
        'MF_N': cert.multipleFetusNumber or 0,
        'MF_C': cert.multipleFetusCount or 0,
        'FBC_POST': cert.doctorWhoFillCertificatePost.name if cert.doctorWhoFillCertificatePost else '',
        'FBC_NAME': cert.doctorWhoFillCertificateName,
        'HEAD_CHOICE': cert.choiceDoctorOrMedicalOrganisation,
        'HEAD_NAME': cert.medicalOrganisationHeadName,
        'FOR_TEST': for_test or cert.status not in (CertStatus.SIGNED.value, CertStatus.EMPTY.value),
        'FOR_TEST_TEXT': for_test_text or 'для проверки',
    }

    return render_template('BirthCertificate.html', **context)


def print_empty_certificate(cert):
    context = defaultdict(str)
    context.update({
        'ch': checkbox,
        'u': underline_if,
        'un': underlined,
        'uw': underlined_width,
        'us': underlined_style,
        'mon_name': month_name,
        'SERIAL': cert.serial if cert.serial else '',  # Серия сертификата
        'NUMBER': cert.number if cert.number else '',  # Номер сертификата
        'FOR_TEST': False
    })

    return render_template('BirthCertificate.html', **context)


def print_duplicate(cert: BirthCertificateModel):
    return print_certificate(cert, True, 'дубликат')
