from django.http import response
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from catalog.models import Author
import datetime

class AuthorAPIViewTest(APITestCase):
    '''This class tests the author CRUD api'''
    def setUp(cls):
        '''creating 4 authors'''
        number_of_authors = 2
        for author in range(number_of_authors):
            Author.objects.create(
                first_name=f'firstname {author}',
                last_name=f'lastname {author}'
            )
    
    def test_read_author_list_response(self):
        '''Checking to see if th authors api exists at the desired location'''
        #Note: according to the django REST framework docs, it is considered best practice to use the absolute url of web apis
        #Also note that if we were to use the url ''http://127.0.0.1:8000/catalog/api/authors' without the forward slash,
        #it would return status code 301 (moved permanently) and then redirect to the address with the forward slash

        response = self.client.get('http://127.0.0.1:8000/catalog/api/authors/')
        self.assertEqual(response.status_code,200)

    def test_read_author_api_list_content(self):
        '''
            This tests to see if the body of the response is what we expect
            i.e a json that contains a list of authors with the correct names and ids
        '''
        response = self.client.get(
                                    'http://127.0.0.1:8000/catalog/api/authors/', 
                                    format='json')
        response_body = response.json()
        expected_response = [
            {
                "id": 1,
                "first_name": "firstname 0",
                "last_name": "lastname 0",
                "date_of_birth": None,
                "date_of_death": None,
            },
            {
                "id": 2,
                "first_name": "firstname 1",
                "last_name": "lastname 1",
                "date_of_birth": None,
                "date_of_death": None,
            }
        ]

        self.assertEqual(response_body,expected_response)

    def test_read_author_id_api_response(self):
        '''Tests to see if the get request to author id 1 returns 200 or not'''
        response = self.client.get('http://127.0.0.1:8000/catalog/api/authors/1/')
        self.assertEqual(response.status_code,200)

    def test_read_author_id_body(self):
        '''Tests the body of the get request to the author with id = 1'''
        response = self.client.get(
                                    'http://127.0.0.1:8000/catalog/api/authors/1/',
                                    format = 'json')
        response_body = response.json()

        expected_response = {
                                "id": 1,
                                "first_name": "firstname 0",
                                "last_name": "lastname 0",
                                "date_of_birth": None,
                                "date_of_death": None,
                            }

        self.assertEqual(response_body,expected_response)

    def test_create_author_response(self):
        '''This tests whether or not an author is created'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/authors/',
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,201)

    def test_create_author_body(self):
        '''This tests the body of the response when an author is created'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/authors/',
            data,
            format="json")
        
        response_body = response.json()
        expected_response = {
            "id": 3,
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": None,
            "date_of_death": None,
        }
        #Checking status code 201 created
        self.assertEqual(response_body,expected_response)

    def test_update_author_response(self):
        '''This tests whether or not an author is updated'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/authors/1/',
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,200)

    def test_update_author(self):
        '''This tests whether or not an author is updated in the database'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        #Get the orginal value of the author to be updated
        author_2 = Author.objects.get(id = 2)

        #Update the chosen author
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/authors/2/',
            data,
            format="json")
        
        #Check whether the author is updated in the database
        self.assertNotEqual(str(author_2),str(Author.objects.get(id = 2)))

    def test_delete_author_response(self):
        '''This tests whether an author gets deleted'''
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/authors/2/')

        #204 means that the request completed but no reponse was returned
        self.assertEqual(response.status_code,204)

    def test_author_was_deleted(self):
        '''This tests whether or not an author was deleted successfuly in the database'''

        #Count the number of authors before the delete
        count_before_delete = Author.objects.count()
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/authors/2/')
        
        #Count number of authors after delete
        count_after_delete = Author.objects.count()
        self.assertLess(count_after_delete,count_before_delete)










    

