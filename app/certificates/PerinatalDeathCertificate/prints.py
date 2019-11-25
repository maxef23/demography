from collections import defaultdict
from typing import Optional
from flask import render_template

from app.Utils import CertStatus
from app.certificates.PerinatalDeathCertificate.models import PerinatalDeathCertificateModel
from app.certificates.util import checkbox, month_name, underline_if, underlined, underlined_width, format_time
from app.refbooks.Address.views import get_address_object_by_guid


def print_certificate(cert: PerinatalDeathCertificateModel,
                      for_test=False,
                      for_test_text=''):
    m_region = get_address_object_by_guid(cert.motherRegistryRegion)
    m_area = get_address_object_by_guid(cert.motherRegistryArea)
    m_city = get_address_object_by_guid(cert.motherRegistryCity)
    m_street = get_address_object_by_guid(cert.motherRegistryStreet)
    c_region = get_address_object_by_guid(cert.childBirthRegion)
    c_area = get_address_object_by_guid(cert.childBirthArea)
    c_city = get_address_object_by_guid(cert.childBirthCity)

    prev = cert.prevCert[0] if cert.prevCert else None  # type: Optional[PerinatalDeathCertificateModel]
    org = cert.organisation

    context = {
        'u': underline_if,
        'un': underlined,
        'uw': underlined_width,
        'mon_name': month_name,
        'ch': checkbox,

        'ORGNAME': org.name if org and org.name else '',
        'OKPO': org.okpo if org and org.okpo else '',
        'OADDR': org.address if org and org.address else '',

        'S': cert.status,
        'T': cert.type,
        'IFINAL': prev.type == 1 if prev is not None else '',
        'IPRELIM': prev.type == 0 if prev is not None else '',
        'SERIAL': cert.serial if cert.serial else '',
        'NUMBER': cert.number if cert.number else '',

        'RSERIAL': cert.recipientDocumentSerial if cert.recipientDocumentSerial else '',
        'RNUMBER': cert.recipientDocumentNumber if cert.recipientDocumentNumber else '',

        'PDDD': cert.perinatalDeathDate_D if cert.perinatalDeathDate_D else '',
        'PDDM': cert.perinatalDeathDate_M if cert.perinatalDeathDate_M else '',
        'PDDY': cert.perinatalDeathDate_Y if cert.perinatalDeathDate_Y else '',
        'PDDh': format_time(cert.perinatalDeathTime, fmt='%H'),
        'PDDm': format_time(cert.perinatalDeathTime, fmt='%M'),
        'BDY': cert.birthDatetime_Y if cert.birthDatetime_Y else '',
        'BDM': cert.birthDatetime_M if cert.birthDatetime_M else '',
        'BDD': cert.birthDatetime_D if cert.birthDatetime_D else '',
        'BDh': format_time(cert.birthTime, fmt='%H'),
        'BDm': format_time(cert.birthTime, fmt='%M'),
        'DD_Y': cert.deathDate_Y if cert.deathDate_Y else '',
        'DD_M': cert.deathDate_M if cert.deathDate_M else '',
        'DD_D': cert.deathDate_D if cert.deathDate_D else '',
        'DD_h': format_time(cert.deathTime, fmt='%H'),
        'DD_m': format_time(cert.deathTime, fmt='%M'),
        'P_T': prev.type if prev else '',
        'P_SERIAL': prev.serial if prev and prev.serial else '',
        'P_NUMBER': prev.number if prev and prev.number else '',
        'P_DDD': prev.deliveryDate_D if prev and prev.deliveryDate_D else '',
        'P_DDM': month_name(prev.deliveryDate_M, True) if prev and prev.deliveryDate_M else '',
        'P_DDY': prev.deliveryDate_Y if prev and prev.deliveryDate_Y else '',
        'D': cert.death,
        'M_NAME': cert.mother_name,
        'SMBDY': '{:04d}'.format(cert.motherDOB_Y) if cert.motherDOB_Y else '',
        'SMBDM': '{:02d}'.format(cert.motherDOB_M) if cert.motherDOB_M else '',
        'SMBDD': '{:02d}'.format(cert.motherDOB_D) if cert.motherDOB_D else '',
        'MDOB_Y': cert.motherDOB_Y or '',
        'MDOB_M': cert.motherDOB_M or '',
        'MDOB_D': cert.motherDOB_D or '',
        'MRR': m_region['obj'] if m_region else '',
        'MRA': m_area['obj'] if m_area else '',
        'MRC': m_city['obj'] if m_city else '',
        'MRS': m_street['obj'] if m_street else '',
        'MRH': cert.motherRegistryHouse or '',
        'MRF': cert.motherRegistryFlat or '',
        'MRLOC': cert.motherLocality,
        'SEX': cert.sex,
        'DP': cert.deathPlace,
        'PNN': str(cert.parturitionNumber) if cert.parturitionNumber else '',
        'MMS': cert.motherMartialStatus,
        'ME': cert.motherEducation,
        'MW': cert.motherWork,
        'CBR': c_region['obj'] if c_region else '',
        'CBA': c_area['obj'] if c_area else '',
        'CBC': c_city['obj'] if c_city else '',
        'CBL': cert.locality,
        'CW': str(cert.childWeight) if cert.childWeight else '',
        'CL': str(cert.childLength) if cert.childLength else '',
        'CFAM': cert.childFamilyName or '',
        'CDR': cert.childDeathReason or '',
        'DR1': cert.deathReasonMain or '',
        'MKB1': cert.deathReasonMainMKBId or '',
        'DR2': cert.deathReasonOther or '',
        'MKB2': cert.deathReasonOtherMKBId or '',
        'DR3': cert.deathReasonMotherMain or '',
        'MKB3': cert.deathReasonMotherMainMKBId or '',
        'DR4': cert.deathReasonMotherOther or '',
        'MKB4': cert.deathReasonMotherOtherMKBId or '',
        'DR5': cert.deathReasonOtherFacts or '',
        'WDR': cert.whoTakeDeathReason,
        'BDR': cert.baseTakeDeathReason,
        'CNUM': cert.childNumber or '',
        'SF': cert.singleFetus,
        'MFN': str(cert.multipleFetusNumber) if cert.multipleFetusNumber else '',
        'MFC': str(cert.multipleFetusCount) if cert.multipleFetusCount else '',
        'WTB': cert.whoTakeBirth,
        'DDY': cert.deliveryDate_Y or '',
        'DDM': cert.deliveryDate_M or '',
        'DDD': cert.deliveryDate_D or '',
        'FILLNAME': cert.doctorWhoFillCertificateName,
        'FILLPOST': cert.doctorWhoFillCertificatePost.name if cert.doctorWhoFillCertificatePost else '',
        'HEADNAME': cert.medicalOrganisationHeadName,
        'CHECKNAME': cert.doctorWhoCheckedCertificateName,
        'RNAME': cert.recipientName,
        'RDOC': cert.recipientDocument,
        'M_CHOICE': cert.choiceDoctorOrMedicalOrganisation,
        'FOR_TEST': for_test or cert.status not in (CertStatus.SIGNED.value, CertStatus.EMPTY.value),
        'FOR_TEST_TEXT': for_test_text or 'для проверки',
    }

    return render_template('PerinatalDeathCertificate.html', **context)


def print_empty_certificate(cert: PerinatalDeathCertificateModel):
    context = defaultdict(str)
    context.update({
        'u': underline_if,
        'un': underlined,
        'uw': underlined_width,
        'month_name': month_name,
        'ch': checkbox,
        'SERIAL': cert.serial if cert.serial else '',
        'NUMBER': cert.number if cert.number else '',
        'FOR_TEST': False
    })

    return render_template('PerinatalDeathCertificate.html', **context)

def print_duplicate(cert: PerinatalDeathCertificateModel):
    return print_certificate(cert, True, 'дубликат')