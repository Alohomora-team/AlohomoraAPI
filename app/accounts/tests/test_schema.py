import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from django.utils import timezone
from alohomora.schema import schema
from condos.models import Apartment, Block
from accounts.models import Visitor, Resident, Service, Entry, Admin
import accounts.utility as Utility
from graphql_jwt.testcases import JSONWebTokenTestCase
class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""
    maxDiff = None
    current_date_time = timezone.now()

    def setUp(self):
        self._client = Client(schema)
        self.user = get_user_model().objects.create(email='user@example',
                                                    password='123',
                                                    username='user',
                                                    is_active=True,)

        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')

        self.admin = Admin.objects.create(
                admin=self.user,
                creator=self.super_user
            )

        self.client.authenticate(self.super_user)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def assertNoResponseErrors(self, resp: dict):
        self.assertNotIn('erros', resp, 'Response has erros')


    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(
            email='creator@example.com',
            password='creator-password',
            username='creator-username',
            is_active=True,
            is_admin=True,
            admin=True,
        )
        get_user_model().objects.create(
          email='admin2@example.com',
          password='admin2-password',
          is_active=True,
        )
        get_user_model().objects.create(
            email='service@example.com',
            password='service-password',
            username='service-username',
            is_active=True,
            is_service=True,
        )
        get_user_model().objects.create(
            email='resident@example.com',
            password='resident-password',
            username='resident-username',
            is_active=True,
            is_resident=True,
        )
        get_user_model().objects.create(
            email='desativado@example.com',
            password='desativado-password',
            username='desativado-username',
            is_active=False,
        )
        block = Block.objects.create(number="1")
        apartment = Apartment.objects.create(number="101", block=block)
        Resident.objects.create(
            complete_name='resident-evil',
            password='resident-password',
            email='resident@example.com',
            cpf='12345678910',
            phone='42',
            mfcc_audio_speaking_phrase=[1.0, 2.0, 3.0, 4.0, 5.0],
            admin=False,
            user=get_user_model().objects.get(email='resident@example.com'),
            apartment=apartment,
            block=block,
        )
        Visitor.objects.create(
            complete_name='visitor',
            cpf='29950509041',
        )
        Service.objects.create(
            complete_name='bob esponja',
            password='service-password',
            email='service@example.com',
            user=get_user_model().objects.get(email='service@example.com'),
        )
        Entry.objects.create(
            resident=Resident.objects.get(email='resident@example.com'),
            apartment=Apartment.objects.get(number='101')
        )
    def test_mutation_createAdmin(self):
        mutation = '''
                    mutation{
                      createAdmin(
                        email: "admin3@example.com",
                        password: "admin3-password"
                      ){
                        email
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createAdmin": {
                "email": "admin3@example.com"
            }
        }, result.data)

    def test_mutation_deleteAdmin(self):
        mutation = '''
                    mutation{
                      deleteAdmin(email: "user@example"){
                        email
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "deleteAdmin": {
                "email": "user@example"
            }
        }, result.data)

    def test_query_all_admins(self):
        query = '''
                query{
                  allAdmins{
                    admin{
                      email
                    }
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "allAdmins": [
                {
                  "admin": {
                    "email": "user@example"
                  }
                }
            ]
        }, result.data)

    def test_query_admin(self):
        query = '''
                query{
                  admin(adminEmail:"user@example"){
                    admin{
                      email
                    }
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "admin": 
                {
                  "admin": {
                    "email": "user@example"
                  }
               }
        }, result.data)

    def test_query_admins(self):
        query = '''
                query{
                  admins(creatorEmail:"admin@example"){
                    admin{
                      email
                    }
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "admins": [
                {
                  "admin": {
                    "email": "user@example"
                  }
               }
            ]
        }, result.data)

    def test_mutation_user(self):
                mutation = '''
                            mutation{
                              createUser(
                                username: "service",
                                email: "service@exemplo.com",
                                password: "123"
                              ){ user{
                                 username
                                 email
                              }
                              }
                            }
                '''

                result = self.client.execute(mutation)
                self.assertIsNone(result.errors)
                self.assertDictEqual({"createUser": {
                                          "user": {
                                            "username": "service",
                                            "email": "service@exemplo.com"
                                          }
                                        }
                                      }, result.data)

    def test_query_users(self):
        query = '''
                query{
                  users{
                   email
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"users": [
                              {"email": "creator@example.com"},
                              {"email": "admin2@example.com"},
                              {"email": "service@example.com"},
                              {"email": "resident@example.com"},
                              {"email": "desativado@example.com"},
                              {"email": "user@example"},
                              {"email": "admin@example"},
                            ]
                  }, result.data)

    def test_mutation_resident(self):


        mutation = '''
                    mutation{
                      createResident(
                        completeName: "bob o construtor",
                        email: "resident2@example.com",
                        cpf: "12345678910",
                        phone: "42",
                        apartment: "101",
                        block: "1",
                        password: "resident",
                        audioSpeakingPhrase: [1.0, 2.0, 3.0, 4.0, 5.0],
                        audioSpeakingName: [1.0, 2.0, 3.0, 4.0, 5.0]
                      ){ resident{
                         completeName
                         email
                      }
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createResident": {
                "resident": {
                    "completeName": "bob o construtor",
                    "email": "resident2@example.com"
                }
            }
        }, result.data)

    def test_query_residents(self):

        query = '''
                query{
                  residents{
                   completeName
                   email
                   phone
                   cpf
                  }
                }
        '''

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "residents": [
                {
                    "completeName": "resident-evil",
                    "email": "resident@example.com",
                    "phone": "42",
                    "cpf": "12345678910"
                }
            ]
        }, result.data)


    def test_query_resident_email(self):

        query = """
        {
            resident(email:"resident@example.com"){
                completeName
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"resident":
                              {
                                  "completeName": "resident-evil"}
                             }, result.data)

    def test_query_resident_cpf(self):

        query = """
        {
            resident(cpf: "12345678910"){
                completeName
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"resident":
                              {
                                  "completeName": "resident-evil"}
                              }, result.data)


    def test_query_visitors(self):

        query = '''
                    query{
                      allVisitors{
                       id
                       completeName
                       cpf
                      }
                    }
        '''

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"allVisitors": [
                                  {
                                    "id": "2",
                                    "completeName": "visitor",
                                    "cpf": "29950509041"
                                  }
                                ]
                              }, result.data)

    def test_mutation_visitors(self):

        mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        id
                        completeName
                        cpf
                      }
                    }
                    }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
    "createVisitor": {
      "visitor": {
        "id": "4",
        "completeName": "visitor2",
        "cpf": "40982705018"
      }
    }
  }, result.data)

    def test_query_services(self):

        query = '''
                    query {
                      services {
                        completeName
                        email
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "services": [
                {
                    "completeName": "bob esponja",
                    "email": "service@example.com"
                }
            ]
        }, result.data)

    def test_query_unactive_users(self):

        query = '''
                    query {
                      unactivesUsers {
                        username
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "unactivesUsers": [
                {
                    "username": "desativado-username"
                }
            ]
        }, result.data)

    def test_mutation_services(self):

        mutation = '''
                mutation{
                  createService(
                    completeName: "colheita-feliz",
                    email: "ibis@ni",
                    password: "123"
                  ){ service{
                     email
                     completeName
                  }
                  }
                }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createService": {
                "service": {
                    "email": "ibis@ni",
                    "completeName": "colheita-feliz"
                }
            }
        }, result.data)
        self.assertNotEqual(get_user_model().objects.get(email="ibis@ni").password, '123')

    def test_authentication_error(self):

        mutation = '''
                    mutation{
                      createUser(
                        username: "goten",
                        email: "goten@example.com",
                        password: "123"
                      ){ user{
                         username
                         email
                      }
                      }
                    }
        '''
        self.client.execute(mutation)
        self.user.is_active = True
        self.user=get_user_model().objects.get(email="goten@example.com")
        result = self.client.authenticate(self.user)
        query = '''
                    query {
                      me {
                        username
                        email
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNotNone(result.errors)
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)
        result = self.client.execute(query)
        self.assertIsNone(result.errors)

    def test_deactivated_user(self):
        mutation = '''
                    mutation{
                      deactivateUser(
                        userEmail: "resident@example.com",)
                      { user{
                           isActive
                      }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.user = get_user_model().objects.get(email="resident@example.com")
        with self.assertRaises(Exception):
            self.client.authenticate(self.user)
            mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        id
                        completeName
                        cpf
                      }
                    }
                    }
                '''
            result = self.client.execute(mutation)
            self.assertIsNone(result.errors)
    def test_activated_user(self):
        mutation = '''
                    mutation{
                      activateUser(
                        userEmail: "resident@example.com",)
                      { user{
                           isActive
                      }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        id
                        completeName
                        cpf
                      }
                    }
                    }

            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)

    def test_delete_service(self):

        mutation = '''
                    mutation{
                      deleteService(serviceEmail: "service@example.com")
                      {
                        serviceEmail
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Service.objects.count(), 0)

    def test_delete_resident(self):

        mutation = '''
                    mutation{
                      deleteResident(residentEmail: "resident@example.com")
                      {
                        residentEmail
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Resident.objects.count(), 0)

    def test_delete_visitor(self):
        mutation = '''
                    mutation{
                      deleteVisitor(cpf: "29950509041")
                      {
                      	cpf
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Visitor.objects.count(), 0)

    def test_update_service(self):

        self.user = get_user_model().objects.get(email='service@example.com')
        self.client.authenticate(self.user)

        mutation = '''
                    mutation {
                      updateService(serviceData: {serviceEmail: "service@example.com", email: "service2@exemplo.com", completeName: "k"}){
                        service {
                          email
                    	  	completeName
                        }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Resident.objects.count(), 1)
        self.assertDictEqual({"updateService": {
                                  "service": {
                                    "email": "service2@exemplo.com",
                                    "completeName": "k"
                                  }
                                }
                              }, result.data)

    def test_update_visitor(self):

        mutation = '''
                    mutation {
                      updateVisitor(visitorData: {visitorCpf: "29950509041", cpf: "80272869058", completeName: "goku"}){
                        visitor {
                          cpf
                    	  completeName
                        }
                      }
                    }
              '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateVisitor":
                              {
                                  "visitor": {
                                    "cpf": "80272869058",
                                    "completeName": "goku"
                                  }
                                }
                              }, result.data)

    def test_update_resident(self):

        mutation = '''
                    mutation {
                      updateResident(residentData: {residentCpf: "12345678910", cpf: "00012312300", completeName: "k"}){
                        resident {
                          cpf
                    	  	completeName
                        }
                      }
                    }
              '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateResident": {
                                  "resident": {
                                    "cpf": "00012312300",
                                    "completeName": "k"
                                  }
                                }
                              }, result.data)

    def test_query_entry(self):
        query = '''
            query{
              entries{
                resident{
                  cpf
                }
                apartment{
                  number
                }
            	}
            }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"entries": [
                              {
                                "resident": {
                                  "cpf": "12345678910"
                                },
                                "apartment": {
                                  "number": "101"
                                }
                              }
                            ]
                          }, result.data)

    def test_mutation_entry(self):
        block = Block.objects.get(number='1')
        apartment = Apartment.objects.create(number="202", block=block)
        mutation = '''
                mutation{
                  createEntry(apartmentNumber: "202", residentCpf: "12345678910"){
                	resident{
                    cpf
                  }
                }
                }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        entry = Entry.objects.get(apartment=apartment)
        self.assertEqual(entry.date.hour, self.current_date_time.hour)
        self.assertEqual(entry.date.day, self.current_date_time.day)
        self.assertDictEqual({"createEntry":
                              {
                                  "resident": {
                                    "cpf": "12345678910"
                                  }
                                }
                              }, result.data)

    def test_changing_email(self):
                mutation = '''
                            mutation{
                              changeEmail(userEmail: "service@example.com", email: "gohan@example.com"){
                                user{
                                   email
                              	}
                              }
                            }
                '''

                result = self.client.execute(mutation)
                self.assertIsNone(result.errors)
                self.assertDictEqual({"changeEmail": {
                                          "user": {
                                            "email": "gohan@example.com"
                                          }
                                        }
                                      }, result.data)

    def test_changing_password(self):
                mutation = '''
                            mutation{
                              changePassword(userEmail: "service@example.com", password: "123"){
                                user{
                                   password
                              	}
                              }
                            }
                '''

                result = self.client.execute(mutation)
                self.assertIsNone(result.errors)
