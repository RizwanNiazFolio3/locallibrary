from unittest.case import expectedFailure
from django.http import response
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from catalog.models import Author, Book, Genre
import datetime
from django.contrib.auth.models import User, Group
from http import HTTPStatus
from rest_framework.reverse import reverse

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
        
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        test_user1.save()
        test_user2.save()

    def test_read_author_list_response(self):
        '''Checking to see if th authors api exists at the desired location'''
        #Note: according to the django REST framework docs, it is considered best practice to use the absolute url of web apis
        #Also note that if we were to use the url ''http://127.0.0.1:8000/catalog/api/authors' without the forward slash,
        #it would return status code 301 (moved permanently) and then redirect to the address with the forward slash
        url = reverse('author-api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,HTTPStatus.OK)

    def test_read_author_api_list_content(self):
        '''
            This tests to see if the body of the response is what we expect
            i.e a json that contains a list of authors with the correct names and ids
        '''
        url = reverse('author-api-list')
        response = self.client.get(
                                    url, 
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
        url = reverse('author-api-detail',args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code,HTTPStatus.OK)

    def test_read_author_id_body(self):
        '''Tests the body of the get request to the author with id = 1'''
        url = reverse('author-api-detail',args=[1])
        response = self.client.get(
                                    url,
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

    def test_create_author_response_without_authorization(self):
        '''This tests whether or not an author is created'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        url = reverse('author-api-list')
        response = self.client.post(
            url,
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,HTTPStatus.UNAUTHORIZED)

    def test_create_author_response_with_authorization(self):
        '''This tests the create author response when user is authorized'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        url = reverse('author-api-list')
        response = self.client.post(
            url,
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,HTTPStatus.CREATED)


    def test_create_author_body(self):
        '''This tests the body of the response when an author is created'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        url = reverse('author-api-list')
        response = self.client.post(
            url,
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
        #Checking whether the response was as expected
        self.assertEqual(response_body,expected_response)

    def test_update_author_response_without_authorization(self):
        '''This tests whether or not an author is updated'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        url = reverse('author-api-detail',args=[1])
        response = self.client.put(
            url,
            data,
            format="json")
        
        #Checking status code 401 unauthorized
        self.assertEqual(response.status_code,HTTPStatus.UNAUTHORIZED)

    def test_update_author_response_with_authorization(self):
        '''This tests the update author response when user is authorized'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        url = reverse('author-api-detail',args=[1])
        response = self.client.put(
            url,
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,HTTPStatus.OK)
        

    def test_update_author(self):
        '''This tests whether or not an author is updated in the database'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        #Get the orginal value of the author to be updated
        author_2 = Author.objects.get(id = 2)

        #Update the chosen author
        url = reverse('author-api-detail',args=[2])
        response = self.client.put(
            url,
            data,
            format="json")
        
        #Check whether the author is updated in the database
        self.assertNotEqual(str(author_2),str(Author.objects.get(id = 2)))

    def test_delete_author_response_without_authorization(self):
        '''This tests whether an author gets deleted'''
        url = reverse('author-api-detail',args=[2])
        response = self.client.delete(url)

        #checking whether response was 401 unauthorized
        self.assertEqual(response.status_code,HTTPStatus.UNAUTHORIZED)

    def test_delete_author_response_with_authorization(self):
        '''This tests whether or not an author is deleted'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('author-api-detail',args=[2])
        response = self.client.delete(url)

        #204 means that the request completed but no reponse was returned
        self.assertEqual(response.status_code,HTTPStatus.NO_CONTENT)
        

    def test_author_was_deleted(self):
        '''This tests whether or not an author was deleted successfuly in the database'''

        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        #Count the number of authors before the delete
        count_before_delete = Author.objects.count()
        url = reverse('author-api-detail',args=[2])
        response = self.client.delete(url)
        
        #Count number of authors after delete
        count_after_delete = Author.objects.count()
        self.assertLess(count_after_delete,count_before_delete)

class RegisterUserTest(APITestCase):
    def setUp(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
    
    def test_create_new_user_response(self):
        '''Tis tests the response when a new user is created'''
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('user-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.OK)

    def test_create_existing_user_response(self):
        '''This tests the response when a user with an existing name is created'''
        data = {
            "username": "testuser1",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('user-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.BAD_REQUEST)

    def test_create_new_user_body(self):
        '''This tests the response body when new user is created'''
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('user-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        expected_response = {
            "user": {
                "id": 2,
                "username": "testuser2",
                "groups": []
            },
            "message": "User Created Successfully.  Now perform Login to get your token"
        }


        response_body = response.json()

        self.assertEqual(response_body,expected_response)

    def test_create_existing_user_body(self):
        '''This tests the response body when an existing user is created'''
        data = {
            "username": "testuser1",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('user-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        expected_response = {
            "username": [
                "A user with that username already exists."
            ]
        }


        response_body = response.json()

        self.assertEqual(response_body,expected_response)

    def test_user_is_created(self):
        '''This tests the response body when an existing user is created'''
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        num_before_creation = User.objects.count()

        url = reverse('user-register-api')
        self.client.post(
            url,
            data,
            format="json"
        )

        num_after_creation = User.objects.count()

        self.assertLess(num_before_creation,num_after_creation)

    def test_user_is_not_librarian(self):
        '''This tests the response body when an existing user is created'''
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('user-register-api')
        self.client.post(
            url,
            data,
            format="json"
        )

        user = User.objects.get(username="testuser2")
        is_librarian = user.groups.filter(name="Librarians").count()

        self.assertEqual(is_librarian,0)


class RegisterLibrarianTest(APITestCase):
    def setUp(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        test_user1.save()
        test_user2.save()

    def test_create_user_without_authorization(self):
        '''This tests the response when a user is created without being authenticated'''
        data = {
            "username": "testuser3",
            "password": "2HJ1vRV0Z&3iD"
        }
        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.UNAUTHORIZED)

    def test_create_user_with_wrong_authorization(self):
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            "username": "testuser3",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.FORBIDDEN)

    def test_user_is_librarian(self):
        '''This tests the response body when an existing user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "username": "testuser3",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        user = User.objects.get(username="testuser3")
        is_librarian = user.groups.filter(name="Librarians").count()

        self.assertEqual(is_librarian,1)


    def test_create_new_user_response_with_authorization(self):
        '''Tis tests the response when a new user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "username": "testuser3",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.OK)

    def test_create_existing_user_response(self):
        '''This tests the response when a user with an existing name is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code,HTTPStatus.BAD_REQUEST)

    def test_create_new_user_body(self):
        '''This tests the response body when new user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "username": "testuser3",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        expected_response = {
            "user": {
                "id": 3,
                "username": "testuser3",
                "groups": [1]
            },
            "message": "User Created Successfully.  Now perform Login to get your token"
        }


        response_body = response.json()

        self.assertEqual(response_body,expected_response)

    def test_create_existing_user_body(self):
        '''This tests the response body when an existing user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        expected_response = {
            "username": [
                "A user with that username already exists."
            ]
        }


        response_body = response.json()

        self.assertEqual(response_body,expected_response)

    def test_user_is_created(self):
        '''This tests the response body when an existing user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = self.client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            "username": "testuser4",
            "password": "2HJ1vRV0Z&3iD"
        }

        num_before_creation = User.objects.count()

        url = reverse('librarian-register-api')
        response = self.client.post(
            url,
            data,
            format="json"
        )

        num_after_creation = User.objects.count()

        self.assertLess(num_before_creation,num_after_creation)


class BookAPIViewTest(TestCase):
    """This class tests the working of book crud api"""

    def setUp(self):

        # Create a book
        test_genre = Genre.objects.create(name='Fiction')
        test_genre.save()
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='1234567891234',
        )

        test_book_2 = Book.objects.create(
            title='Book Title 2',
            summary= 'My book summary',
            isbn='1234567891235',
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book_2.genre.set(genre_objects_for_book)
        test_book.save()
        test_book_2

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        test_user1.save()
        test_user2.save()

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/api/books/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_books_status(self):
        url = reverse('book-api-list')
        client = APIClient()
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_list_books_status_with_normal_user_authorization(self):
        url = reverse('book-api-list')
        client = APIClient()

        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_books_with_librarian_authorization(self):
        url = reverse('book-api-list')
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_list_book_response_body(self):
        url = reverse('book-api-list')
        client =APIClient()
        response = client.get(url)

        response_body = response.json()

        expected_response = [
            {
                "id":1,
                "title":'Book Title',
                "summary":'My book summary',
                "isbn":"1234567891234",
                "author":None,
                "language":None,
                "genre":[
                    1
                ]
            },
            {
                "id":2,
                "title":'Book Title 2',
                "summary":'My book summary',
                "isbn":"1234567891235",
                "author":None,
                "language":None,
                "genre":[
                    1
                ]
            }
        ]

        self.assertEqual(response_body, expected_response)

    def test_create_book_status_without_authorization(self):
        client = APIClient()
        url = reverse('book-api-list')

        response = client.post(url,
            {
                "title":"book_title2",
                "summary": "summary2",
                "isbn": "1234567891248",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED) 

    def test_create_book_status_with_normal_user_authorization(self):
        client = APIClient()
        url = reverse('book-api-list')

        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.post(url,
            {
                "title":"book_title2",
                "summary": "summary2",
                "isbn": "1234567891248",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_create_book_status_with_librarian_authorization(self):
        
        client = APIClient()
        url = reverse('book-api-list')

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.post(url,
            {
                "title":"book_title2",
                "summary": "summary2",
                "isbn": "1234567891248",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED) # 201 means object successfully created

    def test_create_book_response_body(self):
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.post('http://127.0.0.1:8000/catalog/api/books/',
            {
                "title":"book_title_3",
                "summary": "summary2",
                "isbn": "1234567891248",
                "genre": [1]
            },
            format='json'
        )

        expected_response = {
                "id":3,
                "title":'book_title_3',
                "summary":'summary2',
                "isbn":"1234567891248",
                "author":None,
                "language":None,
                "genre":[
                    1
                ]
        }

        response_body = response.json()

        self.assertEqual(response_body,expected_response)

    def test_get_book_using_id_without_authorization(self):
        
        client = APIClient()
        url = reverse('book-api-detail',[1])
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_book_using_id_body(self):
        client = APIClient()
        url = reverse('book-api-detail',[1])
        response = client.get(url)

        response_body = response.json()

        expected_response = {
            "id":1,
            "title":'Book Title',
            "summary":'My book summary',
            "isbn":"1234567891234",
            "author":None,
            "language":None,
            "genre":[
                1
            ]
        }

        self.assertEqual(response_body,expected_response)
    
    def get_book_using_id_with_normal_user_authorization(self):
        client = APIClient()
        url = reverse('book-api-list')

        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('book-api-detail',[1])
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def get_book_using_id_response_with_librarian_authorization(self):
        client = APIClient()
        url = reverse('book-api-list')

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('book-api-detail',[1])
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_book_using_id_without_authorization(self):
        client = APIClient()

        url = reverse('book-api-detail',[1])
        response = client.delete(url)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_delete_book_using_id_with_normal_user_authorization(self):
        client = APIClient()

        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('book-api-detail',[1])
        response = client.delete(url)

        # Status code 204 means that the request completed successfully but no response was returned
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_book_using_id_with_librarian_authorization(self):
        
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('book-api-detail',[1])
        response = client.delete(url)

        # Status code 204 means that the request completed successfully but no response was returned
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_book_was_deleted(self):
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        book_count_before_delete = Book.objects.count()
        url = reverse('book-api-detail',[1])
        response = client.delete(url)
        book_count_after_delete = Book.objects.count()

        # Status code 204 means that the request completed successfully but no response was returned
        self.assertLess(book_count_after_delete, book_count_before_delete)

    def test_update_book_using_id_without_authorization(self):
        
        client = APIClient()
        url = reverse('book-api-detail',[1])
        response = client.put(url,
            {
                "title":"book_title_updated",
                "summary": "summary_updated",
                "isbn": "1234567891247",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_update_book_using_id_with_normal_user_authorization(self):
        client = APIClient()

        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('book-api-detail',[1])
        response = client.put(url,
            {
                "title":"book_title_updated",
                "summary": "summary_updated",
                "isbn": "1234567891247",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_update_book_using_id_with_librarian_authorization(self):
        
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        token_url = reverse('token_obtain_pair')

        response = client.post(
            token_url,
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('book-api-detail',[1])
        response = client.put(url,
            {
                "title":"book_title_updated",
                "summary": "summary_updated",
                "isbn": "1234567891247",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_was_updated(self):
        client = APIClient()

        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        book_before_update = str(Book.objects.get(id=1))
        url = reverse('book-api-detail',[1])
        response = client.put(url,
            {
                "title":"book_title_updated",
                "summary": "summary_updated",
                "isbn": "1234567891247",
                "genre": [1]
            },
            format='json'
        )
        book_after_update = str(Book.objects.get(id=1))

        self.assertNotEqual(book_before_update, book_after_update)






    

