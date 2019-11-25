import unittest

import requests
from flask import json

from app import certificates, db
from app.Utils import FETCH_LIMIT, CertStatus
from app.refbooks.Address.views import ADDRESS_FETCH_LIMIT

BASE_URL = 'http://127.0.0.1:5000/api/'
LOGIN_URL = BASE_URL + 'login'


class Test001Organisation(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_get_catalog_organisation(self):
        r = requests.get(BASE_URL + 'catalog/organisation', params={'token': self.token})
        self.assertEqual(r.status_code, 200)

    def test_get_organisation(self):
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token})
        self.assertEqual(r.status_code, 200)
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_id': 1})
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.content.decode('utf8')), 73)
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_name': 'МО'})
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.content.decode('utf8')), 73)
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_name': 'МО', 'org_id': '999999'})
        self.assertEqual(r.status_code, 200)
        self.assertLessEqual(len(r.content.decode('utf8')), 73)

    def test_insert_organisation(self):
        r = requests.post(BASE_URL + 'organisation',
                          params={'token': self.token},
                          json={'action': 'inserted', 'data': {'name': 'TEST_TEST'}})
        self.assertEqual(r.status_code, 200)

    def test_update_organisation(self):
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_name': 'TEST_TEST'})
        result = json.loads(r.content.decode())
        for x in result['rows']:
            r = requests.post(BASE_URL + 'organisation',
                              params={'token': self.token},
                              json={'action': 'updated', 'data': {'row_id': x['id'], 'shortName': 'test'}})
            self.assertEqual(r.status_code, 200)
            r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_id': x['id']})
            result = json.loads(r.content.decode())
            self.assertEqual(result['rows'][0]['data'][3], 'test')

    def test_deleted_organisation(self):
        r = requests.get(BASE_URL + 'organisation', params={'token': self.token, 'org_name': 'TEST_TEST'})
        result = json.loads(r.content.decode())
        for x in result['rows']:
            r = requests.post(BASE_URL + 'organisation',
                              params={'token': self.token},
                              json={'action': 'deleted', 'data': {'row_id': x['id']}})
            self.assertEqual(r.status_code, 200)


class Test002MKB(unittest.TestCase):
    def test_get_classes(self):
        r = requests.get(BASE_URL + 'mkb/classes')
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 21)

    def test_get_class_by_name(self):
        r = requests.get(BASE_URL + 'mkb/classes', params={'class': 'II'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['rows'][0]['code'], 'II')

    def test_get_groups(self):
        r = requests.get(BASE_URL + 'mkb/groups')
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 260)

    def test_get_group_by_name(self):
        r = requests.get(BASE_URL + 'mkb/groups', params={'group': '(Z30-Z39)'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['rows'][0]['code'], '(Z30-Z39)')

    def test_get_codes(self):
        r = requests.get(BASE_URL + 'mkb/codes')
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), FETCH_LIMIT)

    def test_get_code_by_name(self):
        r = requests.get(BASE_URL + 'mkb/codes', params={'code': 'A00.0'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['rows'][0]['code'], 'A00.0')


class Test003DocumentType(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_get_document_type(self):
        r = requests.get(BASE_URL + 'document_type', params={'token': self.token})
        self.assertEqual(r.status_code, 200)


class Test004ClientValidation(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_get_catalog_client_validation(self):
        r = requests.get(BASE_URL + 'catalog/client_validation', params={'token': self.token})
        self.assertEqual(r.status_code, 200)

    def test_get_client_validation(self):
        r = requests.get(BASE_URL + 'client_validation', params={'token': self.token})
        self.assertEqual(r.status_code, 200)

    def test_insert_client_validation(self):
        r = requests.post(BASE_URL + 'client_validation',
                          params={'token': self.token},
                          json={'action': 'inserted', 'data': {'ageFrom': 1, 'ageTo': 12, 'sex': 2, 'mkb': 'Z00'}})
        self.assertEqual(r.status_code, 200)

    def test_is_valid_client_data(self):
        r = requests.get(BASE_URL + 'is_valid_client_data', params={'birth_date': '2016-01-01',
                                                                    'sex': 2,
                                                                    'mkb': 'Z00'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['is_valid'], False)

    def test_update_client_validation(self):
        r = requests.get(BASE_URL + 'client_validation', params={'token': self.token,
                                                                 'ageFrom': 1,
                                                                 'ageTo': 12,
                                                                 'sex': 2,
                                                                 'mkb': 'Z00'})
        result = json.loads(r.content.decode())
        for x in result['rows']:
            r = requests.post(BASE_URL + 'client_validation',
                              params={'token': self.token},
                              json={'action': 'updated', 'data': {'row_id': x['id'], 'mkb': 'Z11'}})
            self.assertEqual(r.status_code, 200)
            r = requests.get(BASE_URL + 'client_validation', params={'token': self.token, 'org_id': x['id']})
            result = json.loads(r.content.decode())
            self.assertEqual(result['rows'][0]['data'][4], 'Z11')

    def test_deleted_client_validation(self):
        r = requests.get(BASE_URL + 'client_validation', params={'token': self.token,
                                                                 'ageFrom': 1,
                                                                 'ageTo': 12,
                                                                 'sex': 2,
                                                                 'mkb': 'Z11'})
        result = json.loads(r.content.decode())
        for x in result['rows']:
            r = requests.post(BASE_URL + 'client_validation',
                              params={'token': self.token},
                              json={'action': 'deleted', 'data': {'row_id': x['id']}})
            self.assertEqual(r.status_code, 200)


class Test005Client(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_get_client(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token})
        self.assertEqual(r.status_code, 200)

    def test_get_client_by_name1(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token, 'client_name1': 'Имя 1'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0]['data'][6], 'Имя 10')

    def test_get_client_by_name2(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token, 'client_name2': 'Отчество 1'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertGreater(len(result['rows']), 1)
        self.assertEqual(result['rows'][0]['data'][7], 'Отчество 1')
        self.assertEqual(result['rows'][1]['data'][7], 'Отчество 10')

    def test_get_client_by_surname(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token, 'client_surname': 'Фамилия 1'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertGreater(len(result['rows']), 1)
        self.assertEqual(result['rows'][0]['data'][5], 'Фамилия 1')
        self.assertEqual(result['rows'][1]['data'][5], 'Фамилия 10')

    def test_get_client_by_policy_number(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token, 'policy_number': '3772650896000017'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0]['data'][5], 'Фамилия 3')
        self.assertEqual(result['rows'][0]['data'][3], '3772650896000017')

    def test_get_client_by_temp_policy_number(self):
        r = requests.get(BASE_URL + 'client', params={'token': self.token, 'policy_number': '032320737'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0]['data'][5], 'Фамилия 10')
        self.assertEqual(result['rows'][0]['data'][2], '032320737')


class Test006Address(unittest.TestCase):
    def test_get_subject(self):
        r = requests.get(BASE_URL + 'address_object/subject')
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), ADDRESS_FETCH_LIMIT)

    def test_get_subject_by_name(self):
        r = requests.get(BASE_URL + 'address_object/subject', {'name': 'Архангел'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0],
                         {'id': '294277aa-e25d-428c-95ad-46719c4ddb44', 'obj': 'Архангельская обл'})

    def test_get_district_by_guid(self):
        r = requests.get(BASE_URL + 'address_object/district/294277aa-e25d-428c-95ad-46719c4ddb44')
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 20)

    def test_get_district_by_guid_and_name(self):
        r = requests.get(BASE_URL + 'address_object/district/294277aa-e25d-428c-95ad-46719c4ddb44',
                         params={'name': 'Пинеж'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0],
                         {'id': '57d43938-2c4c-43f7-a24d-e0e2fbdd478e', 'obj': 'Пинежский р-н'})

    def test_get_city_by_guid(self):
        r = requests.get(BASE_URL + 'address_object/city/57d43938-2c4c-43f7-a24d-e0e2fbdd478e')
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 100)

    def test_get_city_by_guid_and_name(self):
        r = requests.get(BASE_URL + 'address_object/city/57d43938-2c4c-43f7-a24d-e0e2fbdd478e',
                         params={'name': 'Пахур'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0],
                         {'id': '55571dd5-16f2-47f2-a539-2913250cc9ca', 'obj': 'Пахурово д'})

    def test_get_street_by_guid(self):
        r = requests.get(BASE_URL + 'address_object/street/55571dd5-16f2-47f2-a539-2913250cc9ca')
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 2)

    def test_get_street_by_guid_and_name(self):
        r = requests.get(BASE_URL + 'address_object/street/55571dd5-16f2-47f2-a539-2913250cc9ca',
                         params={'name': 'Новая'})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(len(result['rows']), 1)
        self.assertEqual(result['rows'][0],
                         {'id': 'f33bf815-f579-44c4-9cb1-a4e5d1a51d85', 'obj': 'Новая ул'})

    def test_get_object_by_guid(self):
        r = requests.get(BASE_URL + 'get_address_object_list/55571dd5-16f2-47f2-a539-2913250cc9ca')
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result,
                         {'id': '55571dd5-16f2-47f2-a539-2913250cc9ca', 'obj': 'Пахурово д'})


class Test007BirthCertificateCreate(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_birth_certificate_1_create(self):
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'signed', 'number': '1111', 'childDATOB': '2018-09-11',
                                    'childTIMEOB': None,
                                    'isMotherUnidentified': None, 'isMotherRegistryUnidentified': '0',
                                    'motherSNILS': '123-123-123-12', 'motherFamilyName': 'Фамилия 5',
                                    'motherFirstName': 'Имя 5', 'motherMiddleName': 'Отчество 5',
                                    'motherDOB': '1985-04-19', 'motherRegistryRegion': None, 'motherRegistryArea': None,
                                    'motherRegistryCity': None, 'motherRegistryStreet': None,
                                    'motherRegistryHouse': None, 'motherRegistryFlat': None, 'locality': '1',
                                    'sex': None, 'birthPlace': None, 'motherLocality': None, 'motherMartialStatus': '2',
                                    'motherEducation': '3', 'motherWork': '4', 'motherAttendance': None,
                                    'childNumber': None, 'childFamilyName': 'Фамилия 5',
                                    'childBirthRegion': 'ed36085a-b2f5-454f-b9a9-1c9a678ee618',
                                    'childBirthArea': '9d847a27-080a-4c3e-964e-7a4750fd801a',
                                    'childBirthCity': '60781211-387b-43ba-a7fb-71754eb938fe', 'childWeight': None,
                                    'childLength': None, 'singleFetus': None, 'multipleFetusNumber': None,
                                    'multipleFetusCount': None, 'whoTakeBirth': None, 'recipientFamilyName': 'выфвф',
                                    'recipientFirstName': None, 'recipientMiddleName': None,
                                    'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                    'recipientDocumentNumber': None, 'deliveryDate': '2018-09-18', 'createUserId': '11',
                                    'closedDatetime': None, 'closedUserId': None}
                                })
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'spoiled', 'number': '2222', 'childDATOB': '2018-09-11',
                                    'childTIMEOB': None,
                                    'isMotherUnidentified': None, 'isMotherRegistryUnidentified': '0',
                                    'motherSNILS': '123-123-123-12', 'motherFamilyName': 'Фамилия 5',
                                    'motherFirstName': 'Имя 5', 'motherMiddleName': 'Отчество 5',
                                    'motherDOB': '1985-04-19', 'motherRegistryRegion': None, 'motherRegistryArea': None,
                                    'motherRegistryCity': None, 'motherRegistryStreet': None,
                                    'motherRegistryHouse': None, 'motherRegistryFlat': None, 'locality': '1',
                                    'sex': None, 'birthPlace': None, 'motherLocality': None, 'motherMartialStatus': '2',
                                    'motherEducation': '3', 'motherWork': '4', 'motherAttendance': None,
                                    'childNumber': None, 'childFamilyName': 'Фамилия 5',
                                    'childBirthRegion': 'ed36085a-b2f5-454f-b9a9-1c9a678ee618',
                                    'childBirthArea': '9d847a27-080a-4c3e-964e-7a4750fd801a',
                                    'childBirthCity': '60781211-387b-43ba-a7fb-71754eb938fe', 'childWeight': None,
                                    'childLength': None, 'singleFetus': None, 'multipleFetusNumber': None,
                                    'multipleFetusCount': None, 'whoTakeBirth': None, 'recipientFamilyName': 'выфвф',
                                    'recipientFirstName': None, 'recipientMiddleName': None,
                                    'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                    'recipientDocumentNumber': None, 'deliveryDate': '2018-09-18', 'createUserId': '11',
                                    'closedDatetime': None, 'closedUserId': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.spoiled_cert_id = json.loads(r.content.decode())['data']['row_id']
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'lost', 'number': '3333', 'childDATOB': '2018-09-11', 'childTIMEOB': None,
                                    'isMotherUnidentified': None, 'isMotherRegistryUnidentified': '0',
                                    'motherSNILS': '123-123-123-12', 'motherFamilyName': 'Фамилия 5',
                                    'motherFirstName': 'Имя 5', 'motherMiddleName': 'Отчество 5',
                                    'motherDOB': '1985-04-19', 'motherRegistryRegion': None, 'motherRegistryArea': None,
                                    'motherRegistryCity': None, 'motherRegistryStreet': None,
                                    'motherRegistryHouse': None, 'motherRegistryFlat': None, 'locality': '1',
                                    'sex': None, 'birthPlace': None, 'motherLocality': None, 'motherMartialStatus': '2',
                                    'motherEducation': '3', 'motherWork': '4', 'motherAttendance': None,
                                    'childNumber': None, 'childFamilyName': 'Фамилия 5',
                                    'childBirthRegion': 'ed36085a-b2f5-454f-b9a9-1c9a678ee618',
                                    'childBirthArea': '9d847a27-080a-4c3e-964e-7a4750fd801a',
                                    'childBirthCity': '60781211-387b-43ba-a7fb-71754eb938fe', 'childWeight': None,
                                    'childLength': None, 'singleFetus': None, 'multipleFetusNumber': None,
                                    'multipleFetusCount': None, 'whoTakeBirth': None, 'recipientFamilyName': 'выфвф',
                                    'recipientFirstName': None, 'recipientMiddleName': None,
                                    'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                    'recipientDocumentNumber': None, 'deliveryDate': '2018-09-18', 'createUserId': '11',
                                    'closedDatetime': None, 'closedUserId': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.lost_cert_id = json.loads(r.content.decode())['data']['row_id']


class Test008BirthCertificateSign(unittest.TestCase):
    def setUp(self):
        db.session.commit()
        self.query = certificates.BirthCertificateModel.query.filter_by
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_birth_certificate_2_done(self):
        signed_cert_id = self.query(serial='signed', number='1111').first().id
        r = requests.post(BASE_URL + 'birth_certificate_done',
                          params={'token': self.token},
                          json={'row_id': signed_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        signed_cert = self.query(serial='signed', number='1111').first()
        self.assertEqual(signed_cert.status, CertStatus.SIGNED.value)

        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'birth_certificate_done',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SIGNED.value)

        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'birth_certificate_done',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.SIGNED.value)

    def test_birth_certificate_3_spoiled(self):
        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'birth_certificate_spoiled',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'spoiled')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SPOILED.value)

    def test_birth_certificate_4_lost(self):
        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'birth_certificate_lost',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'lost')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.LOST.value)


class Test009BirthCertificateOther(unittest.TestCase):
    signed_cert = None
    spoiled_cert = None
    new_spoiled_cert = None
    lost_cert = None
    new_lost_cert = None
    query = None

    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    @classmethod
    def setUpClass(cls):
        db.session.commit()
        db.session.expire_all()
        cls.query = certificates.BirthCertificateModel.query.filter_by
        cls.signed_cert = cls.query(serial='signed', number='1111', status=CertStatus.SIGNED.value).first()
        cls.spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.SPOILED.value).first()
        cls.new_spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.PROJECT.value).first()
        cls.lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.LOST.value).first()
        cls.new_lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.PROJECT.value).first()

    @classmethod
    def tearDownClass(cls):
        db.engine.execute(
            "DELETE FROM {table} "
            "WHERE serial IN ({serial_list})".format(
                table=certificates.BirthCertificateModel.__tablename__,
                serial_list=','.join(["'spoiled'", "'lost'", "'signed'"]))
        )

    def test_birth_certificate_5_print(self):
        r = requests.get(BASE_URL + 'birth_certificate/print',
                         params={'token': self.token, 'id': self.lost_cert.id})
        self.assertEqual(r.status_code, 200)

    def test_birth_certificate_6_delete_signed(self):
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.signed_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.spoiled_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.lost_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_spoiled_cert.id}})
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'birth_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_lost_cert.id}})
        self.assertEqual(r.status_code, 200)


class Test010DeathCertificateCreate(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_death_certificate_1_create(self):
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {'serial': 'signed', 'number': '1111', 'type': None, 'isUnidentified': None,
                                         'SNILS': '121-231-231-23', 'familyName': 'Фамилия 1', 'firstName': 'Им1',
                                         'middleName': 'Отчество 1', 'birthDate': '1961-06-15', 'sex': '1',
                                         'isRegistryUnidentified': None,
                                         'registryRegion': '52618b9c-bcbb-47e7-8957-95c63f0b17cc',
                                         'registryArea': 'a09e3cff-361c-4f1c-a6c6-a5af13cead2f',
                                         'registryCity': '73c29a8c-d61e-45dc-afb8-c3d0b0753cb8',
                                         'registryStreet': 'b807f381-68ca-412d-8c9f-704b701b344f', 'registryHouse': '1',
                                         'registryFlat': '1', 'registryLocality': '1', 'isDeathPlaceUnidentified': None,
                                         'deathPlace': None, 'deathRegion': '53ec9705-ec3e-4cbf-921f-229968e10aeb',
                                         'deathArea': '21156dc1-ebf7-404c-b009-fc4afe637436', 'deathCity': None,
                                         'deathStreet': None, 'deathHouse': None, 'deathFlat': None,
                                         'deathLocality': '1', 'isDeathDateAndTimeUnidentified': None,
                                         'isDeathTimeUnidentified': None, 'deathDate': None, 'deathTime': '00:00:00',
                                         'isChildBeforeMonth': None, 'childBeforeMonthWeight': None,
                                         'childBeforeMonthNumber': None, 'isChildBeforeYear': '0',
                                         'childBeforeYearWeight': None, 'childBeforeYearNumber': None,
                                         'childParameters': '1', 'childRegion': None, 'childCity': None,
                                         'isMotherUnidentified': None, 'motherSNILS': '0', 'motherFamilyName': None,
                                         'motherFirstName': None, 'motherMiddleName': None, 'motherDOB': None,
                                         'motherAge': None, 'motherMartialStatus': None, 'motherEducation': None,
                                         'motherWork': None, 'deathReason': None, 'deathTraumaDetails': None,
                                         'whoTakeDeathReason': None, 'doctorWhoTakeDeathReason': None,
                                         'doctorWhoTakeDeathReasonSpeciality': None,
                                         'organisationWhoTakeDeathReason': None, 'deathReasonBased': None,
                                         'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                         'deathReasonMainPeriod_Year': None, 'deathReasonMainPeriod_Month': None,
                                         'deathReasonMainPeriod_Week': None, 'deathReasonMainPeriod_Day': None,
                                         'deathReasonMainPeriod_Hour': None, 'deathReasonMainPeriod_Minutes': None,
                                         'deathReasonCauseMKBId': None, 'deathReasonCause': None,
                                         'deathReasonCausePeriod_Year': None, 'deathReasonCausePeriod_Month': None,
                                         'deathReasonCausePeriod_Week': None, 'deathReasonCausePeriod_Day': None,
                                         'deathReasonCausePeriod_Hour': None, 'deathReasonCausePeriod_Minutes': None,
                                         'deathReasonFirstMKBId': None, 'deathReasonFirst': None,
                                         'deathReasonFirstPeriod_Year': None, 'deathReasonFirstPeriod_Month': None,
                                         'deathReasonFirstPeriod_Week': None, 'deathReasonFirstPeriod_Day': None,
                                         'deathReasonFirstPeriod_Hour': None, 'deathReasonFirstPeriod_Minutes': None,
                                         'deathReasonOuterMKBId': None, 'deathReasonOuter': None,
                                         'deathReasonOuterPeriod_Year': None, 'deathReasonOuterPeriod_Month': None,
                                         'deathReasonOuterPeriod_Week': None, 'deathReasonOuterPeriod_Day': None,
                                         'deathReasonOuterPeriod_Hour': None, 'deathReasonOuterPeriod_Minutes': None,
                                         'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                         'deathReasonOtherPeriod_Year': None, 'deathReasonOtherPeriod_Month': None,
                                         'deathReasonOtherPeriod_Week': None, 'deathReasonOtherPeriod_Day': None,
                                         'deathReasonOtherPeriod_Hour': None, 'deathReasonOtherPeriod_Minutes': None,
                                         'deathComeDTPPeriod': '1', 'pregnantDeath': None, 'recipientFamilyName': None,
                                         'recipientFirstName': None, 'recipientMiddleName': None,
                                         'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                         'recipientDocumentNumber': None, 'deliveryDate': None, 'createUserId': '1',
                                         'closedDatetime': None, 'closedUserId': None, 'prevCertId': None}})
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'spoiled', 'number': '2222', 'type': None, 'isUnidentified': None,
                                    'SNILS': '121-231-231-23', 'familyName': 'Фамилия 1', 'firstName': 'Им1',
                                    'middleName': 'Отчество 1', 'birthDate': '1961-06-15', 'sex': '1',
                                    'isRegistryUnidentified': None,
                                    'registryRegion': '52618b9c-bcbb-47e7-8957-95c63f0b17cc',
                                    'registryArea': 'a09e3cff-361c-4f1c-a6c6-a5af13cead2f',
                                    'registryCity': '73c29a8c-d61e-45dc-afb8-c3d0b0753cb8',
                                    'registryStreet': 'b807f381-68ca-412d-8c9f-704b701b344f', 'registryHouse': '1',
                                    'registryFlat': '1', 'registryLocality': '1', 'isDeathPlaceUnidentified': None,
                                    'deathPlace': None, 'deathRegion': '53ec9705-ec3e-4cbf-921f-229968e10aeb',
                                    'deathArea': '21156dc1-ebf7-404c-b009-fc4afe637436', 'deathCity': None,
                                    'deathStreet': None, 'deathHouse': None, 'deathFlat': None,
                                    'deathLocality': '1', 'isDeathDateAndTimeUnidentified': None,
                                    'isDeathTimeUnidentified': None, 'deathDate': None, 'deathTime': '00:00:00',
                                    'isChildBeforeMonth': None, 'childBeforeMonthWeight': None,
                                    'childBeforeMonthNumber': None, 'isChildBeforeYear': '0',
                                    'childBeforeYearWeight': None, 'childBeforeYearNumber': None,
                                    'childParameters': '1', 'childRegion': None, 'childCity': None,
                                    'isMotherUnidentified': None, 'motherSNILS': '0', 'motherFamilyName': None,
                                    'motherFirstName': None, 'motherMiddleName': None, 'motherDOB': None,
                                    'motherAge': None, 'motherMartialStatus': None, 'motherEducation': None,
                                    'motherWork': None, 'deathReason': None, 'deathTraumaDetails': None,
                                    'whoTakeDeathReason': None, 'doctorWhoTakeDeathReason': None,
                                    'doctorWhoTakeDeathReasonSpeciality': None,
                                    'organisationWhoTakeDeathReason': None, 'deathReasonBased': None,
                                    'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                    'deathReasonMainPeriod_Year': None, 'deathReasonMainPeriod_Month': None,
                                    'deathReasonMainPeriod_Week': None, 'deathReasonMainPeriod_Day': None,
                                    'deathReasonMainPeriod_Hour': None, 'deathReasonMainPeriod_Minutes': None,
                                    'deathReasonCauseMKBId': None, 'deathReasonCause': None,
                                    'deathReasonCausePeriod_Year': None, 'deathReasonCausePeriod_Month': None,
                                    'deathReasonCausePeriod_Week': None, 'deathReasonCausePeriod_Day': None,
                                    'deathReasonCausePeriod_Hour': None, 'deathReasonCausePeriod_Minutes': None,
                                    'deathReasonFirstMKBId': None, 'deathReasonFirst': None,
                                    'deathReasonFirstPeriod_Year': None, 'deathReasonFirstPeriod_Month': None,
                                    'deathReasonFirstPeriod_Week': None, 'deathReasonFirstPeriod_Day': None,
                                    'deathReasonFirstPeriod_Hour': None, 'deathReasonFirstPeriod_Minutes': None,
                                    'deathReasonOuterMKBId': None, 'deathReasonOuter': None,
                                    'deathReasonOuterPeriod_Year': None, 'deathReasonOuterPeriod_Month': None,
                                    'deathReasonOuterPeriod_Week': None, 'deathReasonOuterPeriod_Day': None,
                                    'deathReasonOuterPeriod_Hour': None, 'deathReasonOuterPeriod_Minutes': None,
                                    'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                    'deathReasonOtherPeriod_Year': None, 'deathReasonOtherPeriod_Month': None,
                                    'deathReasonOtherPeriod_Week': None, 'deathReasonOtherPeriod_Day': None,
                                    'deathReasonOtherPeriod_Hour': None, 'deathReasonOtherPeriod_Minutes': None,
                                    'deathComeDTPPeriod': '1', 'pregnantDeath': None, 'recipientFamilyName': None,
                                    'recipientFirstName': None, 'recipientMiddleName': None,
                                    'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                    'recipientDocumentNumber': None, 'deliveryDate': None, 'createUserId': '1',
                                    'closedDatetime': None, 'closedUserId': None, 'prevCertId': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.spoiled_cert_id = json.loads(r.content.decode())['data']['row_id']
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'lost', 'number': '3333', 'type': None, 'isUnidentified': None,
                                    'SNILS': '121-231-231-23', 'familyName': 'Фамилия 1', 'firstName': 'Им1',
                                    'middleName': 'Отчество 1', 'birthDate': '1961-06-15', 'sex': '1',
                                    'isRegistryUnidentified': None,
                                    'registryRegion': '52618b9c-bcbb-47e7-8957-95c63f0b17cc',
                                    'registryArea': 'a09e3cff-361c-4f1c-a6c6-a5af13cead2f',
                                    'registryCity': '73c29a8c-d61e-45dc-afb8-c3d0b0753cb8',
                                    'registryStreet': 'b807f381-68ca-412d-8c9f-704b701b344f', 'registryHouse': '1',
                                    'registryFlat': '1', 'registryLocality': '1', 'isDeathPlaceUnidentified': None,
                                    'deathPlace': None, 'deathRegion': '53ec9705-ec3e-4cbf-921f-229968e10aeb',
                                    'deathArea': '21156dc1-ebf7-404c-b009-fc4afe637436', 'deathCity': None,
                                    'deathStreet': None, 'deathHouse': None, 'deathFlat': None,
                                    'deathLocality': '1', 'isDeathDateAndTimeUnidentified': None,
                                    'isDeathTimeUnidentified': None, 'deathDate': None, 'deathTime': '00:00:00',
                                    'isChildBeforeMonth': None, 'childBeforeMonthWeight': None,
                                    'childBeforeMonthNumber': None, 'isChildBeforeYear': '0',
                                    'childBeforeYearWeight': None, 'childBeforeYearNumber': None,
                                    'childParameters': '1', 'childRegion': None, 'childCity': None,
                                    'isMotherUnidentified': None, 'motherSNILS': '0', 'motherFamilyName': None,
                                    'motherFirstName': None, 'motherMiddleName': None, 'motherDOB': None,
                                    'motherAge': None, 'motherMartialStatus': None, 'motherEducation': None,
                                    'motherWork': None, 'deathReason': None, 'deathTraumaDetails': None,
                                    'whoTakeDeathReason': None, 'doctorWhoTakeDeathReason': None,
                                    'doctorWhoTakeDeathReasonSpeciality': None,
                                    'organisationWhoTakeDeathReason': None, 'deathReasonBased': None,
                                    'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                    'deathReasonMainPeriod_Year': None, 'deathReasonMainPeriod_Month': None,
                                    'deathReasonMainPeriod_Week': None, 'deathReasonMainPeriod_Day': None,
                                    'deathReasonMainPeriod_Hour': None, 'deathReasonMainPeriod_Minutes': None,
                                    'deathReasonCauseMKBId': None, 'deathReasonCause': None,
                                    'deathReasonCausePeriod_Year': None, 'deathReasonCausePeriod_Month': None,
                                    'deathReasonCausePeriod_Week': None, 'deathReasonCausePeriod_Day': None,
                                    'deathReasonCausePeriod_Hour': None, 'deathReasonCausePeriod_Minutes': None,
                                    'deathReasonFirstMKBId': None, 'deathReasonFirst': None,
                                    'deathReasonFirstPeriod_Year': None, 'deathReasonFirstPeriod_Month': None,
                                    'deathReasonFirstPeriod_Week': None, 'deathReasonFirstPeriod_Day': None,
                                    'deathReasonFirstPeriod_Hour': None, 'deathReasonFirstPeriod_Minutes': None,
                                    'deathReasonOuterMKBId': None, 'deathReasonOuter': None,
                                    'deathReasonOuterPeriod_Year': None, 'deathReasonOuterPeriod_Month': None,
                                    'deathReasonOuterPeriod_Week': None, 'deathReasonOuterPeriod_Day': None,
                                    'deathReasonOuterPeriod_Hour': None, 'deathReasonOuterPeriod_Minutes': None,
                                    'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                    'deathReasonOtherPeriod_Year': None, 'deathReasonOtherPeriod_Month': None,
                                    'deathReasonOtherPeriod_Week': None, 'deathReasonOtherPeriod_Day': None,
                                    'deathReasonOtherPeriod_Hour': None, 'deathReasonOtherPeriod_Minutes': None,
                                    'deathComeDTPPeriod': '1', 'pregnantDeath': None, 'recipientFamilyName': None,
                                    'recipientFirstName': None, 'recipientMiddleName': None,
                                    'recipientDocumentType': '1', 'recipientDocumentSerial': None,
                                    'recipientDocumentNumber': None, 'deliveryDate': None, 'createUserId': '1',
                                    'closedDatetime': None, 'closedUserId': None, 'prevCertId': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.lost_cert_id = json.loads(r.content.decode())['data']['row_id']


class Test011DeathCertificateSign(unittest.TestCase):
    def setUp(self):
        db.session.commit()
        self.query = certificates.DeathCertificateModel.query.filter_by
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_death_certificate_2_done(self):
        signed_cert_id = self.query(serial='signed', number='1111').first().id
        r = requests.post(BASE_URL + 'death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': signed_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        signed_cert = self.query(serial='signed', number='1111').first()
        self.assertEqual(signed_cert.status, CertStatus.SIGNED.value)

        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SIGNED.value)

        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.SIGNED.value)

    def test_death_certificate_3_spoiled(self):
        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'death_certificate_spoiled',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'spoiled')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SPOILED.value)

    def test_death_certificate_4_lost(self):
        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'death_certificate_lost',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'lost')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.LOST.value)


class Test012DeathCertificateOther(unittest.TestCase):
    signed_cert = None
    spoiled_cert = None
    new_spoiled_cert = None
    lost_cert = None
    new_lost_cert = None
    query = None

    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    @classmethod
    def setUpClass(cls):
        db.session.commit()
        db.session.expire_all()
        cls.query = certificates.DeathCertificateModel.query.filter_by
        cls.signed_cert = cls.query(serial='signed', number='1111', status=CertStatus.SIGNED.value).first()
        cls.spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.SPOILED.value).first()
        cls.new_spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.PROJECT.value).first()
        cls.lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.LOST.value).first()
        cls.new_lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.PROJECT.value).first()

    @classmethod
    def tearDownClass(cls):
        db.engine.execute(
            "DELETE FROM {table} "
            "WHERE serial IN ({serial_list})".format(
                table=certificates.DeathCertificateModel.__tablename__,
                serial_list=','.join(["'spoiled'", "'lost'", "'signed'"]))
        )

    def test_death_certificate_5_print(self):
        r = requests.get(BASE_URL + 'death_certificate/print',
                         params={'token': self.token, 'id': self.lost_cert.id})
        self.assertEqual(r.status_code, 200)

    def test_death_certificate_6_delete_signed(self):
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.signed_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.spoiled_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.lost_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_spoiled_cert.id}})
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_lost_cert.id}})
        self.assertEqual(r.status_code, 200)


class Test013PerinatalDeathCertificateCreate(unittest.TestCase):
    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_perinatal_death_certificate_1_create(self):
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {'serial': 'signed', 'number': '1111',
                                         'deliveryDate': '2018-09-06', 'recipientDocumentType': '1',
                                         'previousCertificateSerial': None, 'previousCertificateNumber': None,
                                         'previousCertificateDeliveryDate': None, 'perinatalDeathDate': None,
                                         'perinatalDeathTime': None, 'birthDatetime': '2018-09-05', 'birthTime': None,
                                         'deathDate': None, 'deathTime': None, 'death': None,
                                         'motherFamilyName': 'фывфывфывфывфывфы', 'motherFirstName': 'выфвфы',
                                         'motherMiddleName': None, 'motherDOB': None, 'motherRegistryRegion': None,
                                         'motherRegistryArea': None, 'motherRegistryCity': None,
                                         'motherRegistryStreet': None, 'motherRegistryHouse': None,
                                         'motherRegistryFlat': None, 'locality': '1', 'sex': '1', 'deathPlace': '2',
                                         'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                         'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                         'deathReasonMotherMainMKBId': None, 'deathReasonMotherMain': None,
                                         'deathReasonMotherOtherMKBId': None, 'deathReasonMotherOther': None,
                                         'deathReasonOtherFacts': None, 'motherLocality': '2',
                                         'motherMartialStatus': None, 'motherEducation': None, 'motherWork': '3',
                                         'parturitionNumber': None, 'childFamilyName': 'фывфывфывфывфывфы',
                                         'childBirthRegion': None, 'childBirthArea': None, 'childBirthCity': None,
                                         'childWeight': None, 'childLength': None, 'singleFetus': None,
                                         'multipleFetusNumber': None, 'multipleFetusCount': None, 'childNumber': None,
                                         'whoTakeBirth': None, 'whoTakeDeathReason': None,
                                         'baseTakeDeathReason': None}})
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'spoiled', 'number': '2222',
                                    'deliveryDate': '2018-09-06', 'recipientDocumentType': '1',
                                    'previousCertificateSerial': None, 'previousCertificateNumber': None,
                                    'previousCertificateDeliveryDate': None, 'perinatalDeathDate': None,
                                    'perinatalDeathTime': None, 'birthDatetime': '2018-09-05', 'birthTime': None,
                                    'deathDate': None, 'deathTime': None, 'death': None,
                                    'motherFamilyName': 'фывфывфывфывфывфы', 'motherFirstName': 'выфвфы',
                                    'motherMiddleName': None, 'motherDOB': None, 'motherRegistryRegion': None,
                                    'motherRegistryArea': None, 'motherRegistryCity': None,
                                    'motherRegistryStreet': None, 'motherRegistryHouse': None,
                                    'motherRegistryFlat': None, 'locality': '1', 'sex': '1', 'deathPlace': '2',
                                    'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                    'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                    'deathReasonMotherMainMKBId': None, 'deathReasonMotherMain': None,
                                    'deathReasonMotherOtherMKBId': None, 'deathReasonMotherOther': None,
                                    'deathReasonOtherFacts': None, 'motherLocality': '2',
                                    'motherMartialStatus': None, 'motherEducation': None, 'motherWork': '3',
                                    'parturitionNumber': None, 'childFamilyName': 'фывфывфывфывфывфы',
                                    'childBirthRegion': None, 'childBirthArea': None, 'childBirthCity': None,
                                    'childWeight': None, 'childLength': None, 'singleFetus': None,
                                    'multipleFetusNumber': None, 'multipleFetusCount': None, 'childNumber': None,
                                    'whoTakeBirth': None, 'whoTakeDeathReason': None,
                                    'baseTakeDeathReason': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.spoiled_cert_id = json.loads(r.content.decode())['data']['row_id']
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'inserted',
                                'data': {
                                    'serial': 'lost', 'number': '3333',
                                    'deliveryDate': '2018-09-06', 'recipientDocumentType': '1',
                                    'previousCertificateSerial': None, 'previousCertificateNumber': None,
                                    'previousCertificateDeliveryDate': None, 'perinatalDeathDate': None,
                                    'perinatalDeathTime': None, 'birthDatetime': '2018-09-05', 'birthTime': None,
                                    'deathDate': None, 'deathTime': None, 'death': None,
                                    'motherFamilyName': 'фывфывфывфывфывфы', 'motherFirstName': 'выфвфы',
                                    'motherMiddleName': None, 'motherDOB': None, 'motherRegistryRegion': None,
                                    'motherRegistryArea': None, 'motherRegistryCity': None,
                                    'motherRegistryStreet': None, 'motherRegistryHouse': None,
                                    'motherRegistryFlat': None, 'locality': '1', 'sex': '1', 'deathPlace': '2',
                                    'deathReasonMainMKBId': 'Z99.0', 'deathReasonMain': None,
                                    'deathReasonOtherMKBId': None, 'deathReasonOther': None,
                                    'deathReasonMotherMainMKBId': None, 'deathReasonMotherMain': None,
                                    'deathReasonMotherOtherMKBId': None, 'deathReasonMotherOther': None,
                                    'deathReasonOtherFacts': None, 'motherLocality': '2',
                                    'motherMartialStatus': None, 'motherEducation': None, 'motherWork': '3',
                                    'parturitionNumber': None, 'childFamilyName': 'фывфывфывфывфывфы',
                                    'childBirthRegion': None, 'childBirthArea': None, 'childBirthCity': None,
                                    'childWeight': None, 'childLength': None, 'singleFetus': None,
                                    'multipleFetusNumber': None, 'multipleFetusCount': None, 'childNumber': None,
                                    'whoTakeBirth': None, 'whoTakeDeathReason': None,
                                    'baseTakeDeathReason': None}
                                })
        self.assertEqual(r.status_code, 200)
        self.lost_cert_id = json.loads(r.content.decode())['data']['row_id']


class Test014PerinatalDeathCertificateSign(unittest.TestCase):
    def setUp(self):
        db.session.commit()
        self.query = certificates.PerinatalDeathCertificateModel.query.filter_by
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    def test_perinatal_death_certificate_2_done(self):
        signed_cert_id = self.query(serial='signed', number='1111').first().id
        r = requests.post(BASE_URL + 'perinatal_death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': signed_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        signed_cert = self.query(serial='signed', number='1111').first()
        self.assertEqual(signed_cert.status, CertStatus.SIGNED.value)

        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'perinatal_death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SIGNED.value)

        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'perinatal_death_certificate_done',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode())['action'], 'done')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.SIGNED.value)

    def test_perinatal_death_certificate_3_spoiled(self):
        spoiled_cert_id = self.query(serial='spoiled', number='2222').first().id
        r = requests.post(BASE_URL + 'perinatal_death_certificate_spoiled',
                          params={'token': self.token},
                          json={'row_id': spoiled_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'spoiled')
        db.session.commit()
        spoiled_cert = self.query(serial='spoiled', number='2222').first()
        self.assertEqual(spoiled_cert.status, CertStatus.SPOILED.value)

    def test_perinatal_death_certificate_4_lost(self):
        lost_cert_id = self.query(serial='lost', number='3333').first().id
        r = requests.post(BASE_URL + 'perinatal_death_certificate_lost',
                          params={'token': self.token},
                          json={'row_id': lost_cert_id})
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.content.decode())
        self.assertEqual(result['action'], 'lost')
        db.session.commit()
        lost_cert = self.query(serial='lost', number='3333').first()
        self.assertEqual(lost_cert.status, CertStatus.LOST.value)


class Test015PerinatalDeathCertificateOther(unittest.TestCase):
    signed_cert = None
    spoiled_cert = None
    new_spoiled_cert = None
    lost_cert = None
    new_lost_cert = None
    query = None

    def setUp(self):
        self.token = requests.post(
            LOGIN_URL, json={'login': 'admin', 'password': '7ddee529d572c2c0a339768c5eaf9e97'}).json()['token']

    @classmethod
    def setUpClass(cls):
        db.session.commit()
        db.session.expire_all()
        cls.query = certificates.PerinatalDeathCertificateModel.query.filter_by
        cls.signed_cert = cls.query(serial='signed', number='1111', status=CertStatus.SIGNED.value).first()
        cls.spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.SPOILED.value).first()
        cls.new_spoiled_cert = cls.query(serial='spoiled', number='2222', status=CertStatus.PROJECT.value).first()
        cls.lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.LOST.value).first()
        cls.new_lost_cert = cls.query(serial='lost', number='3333', status=CertStatus.PROJECT.value).first()

    @classmethod
    def tearDownClass(cls):
        db.engine.execute(
            "DELETE FROM {table} "
            "WHERE serial IN ({serial_list})".format(
                table=certificates.PerinatalDeathCertificateModel.__tablename__,
                serial_list=','.join(["'spoiled'", "'lost'", "'signed'"]))
        )

    def test_perinatal_death_certificate_5_print(self):
        r = requests.get(BASE_URL + 'perinatal_death_certificate/print',
                         params={'token': self.token, 'id': self.lost_cert.id})
        self.assertEqual(r.status_code, 200)

    def test_perinatal_death_certificate_6_delete_signed(self):
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.signed_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.spoiled_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.lost_cert.id}})
        self.assertEqual(r.status_code, 400)
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_spoiled_cert.id}})
        self.assertEqual(r.status_code, 200)
        r = requests.post(BASE_URL + 'perinatal_death_certificate',
                          params={'token': self.token},
                          json={'action': 'deleted',
                                'data': {'row_id': self.new_lost_cert.id}})
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
