from django.http import response
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from catalog.models import (
    Author, 
    Book, 
    BookInstance, 
    Genre, 
    Language,
)
import datetime
from django.contrib.auth.models import User, Group

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

    def test_create_author_response_without_authorization(self):
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
        self.assertEqual(response.status_code,401)

    def test_create_author_response_with_authorization(self):
        '''This tests the create author response when user is authorized'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/authors/',
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,201)


    def test_create_author_body(self):
        '''This tests the body of the response when an author is created'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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
        #Checking whether the response was as expected
        self.assertEqual(response_body,expected_response)

    def test_update_author_response_without_authorization(self):
        '''This tests whether or not an author is updated'''
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/authors/1/',
            data,
            format="json")
        
        #Checking status code 401 unauthorized
        self.assertEqual(response.status_code,401)

    def test_update_author_response_with_authorization(self):
        '''This tests the update author response when user is authorized'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/authors/1/',
            data,
            format="json")
        
        #Checking status code 201 created
        self.assertEqual(response.status_code,200)
        

    def test_update_author(self):
        '''This tests whether or not an author is updated in the database'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/authors/2/',
            data,
            format="json")
        
        #Check whether the author is updated in the database
        self.assertNotEqual(str(author_2),str(Author.objects.get(id = 2)))

    def test_delete_author_response_without_authorization(self):
        '''This tests whether an author gets deleted'''
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/authors/2/')

        #checking whether response was 401 unauthorized
        self.assertEqual(response.status_code,401)

    def test_delete_author_response_with_authorization(self):
        '''This tests whether or not an author is deleted'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.delete('http://127.0.0.1:8000/catalog/api/authors/2/')

        #204 means that the request completed but no reponse was returned
        self.assertEqual(response.status_code,204)
        

    def test_author_was_deleted(self):
        '''This tests whether or not an author was deleted successfuly in the database'''

        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        #Count the number of authors before the delete
        count_before_delete = Author.objects.count()
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/authors/2/')
        
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,200)

    def test_create_existing_user_response(self):
        '''This tests the response when a user with an existing name is created'''
        data = {
            "username": "testuser1",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,400)

    def test_create_new_user_body(self):
        '''This tests the response body when new user is created'''
        data = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
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

        self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
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

        self.client.post(
            'http://127.0.0.1:8000/catalog/api/register',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,401)

    def test_create_user_with_wrong_authorization(self):
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,403)

    def test_user_is_librarian(self):
        '''This tests the response body when an existing user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,200)

    def test_create_existing_user_response(self):
        '''This tests the response when a user with an existing name is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
            data,
            format="json"
        )

        self.assertEqual(response.status_code,400)

    def test_create_new_user_body(self):
        '''This tests the response body when new user is created'''
        #Getting authorization credentials
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
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

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
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

        self.client.post(
            'http://127.0.0.1:8000/catalog/api/register-librarian',
            data,
            format="json"
        )

        num_after_creation = User.objects.count()

        self.assertLess(num_before_creation,num_after_creation)

class HomePageApiTest(APITestCase):
    def setUp(self):
        #Create Users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        #Give user 1 librarian permissions
        test_user1.save()
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        test_user1.save()
        test_user2.save()

        #Create Authors
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_author_2 = Author.objects.create(first_name='John', last_name='Doe')

        #Create Genres
        Genre.objects.create(name='Fantasy')
        Genre.objects.create(name='High Fantasy')
        Genre.objects.create(name='Science Fiction')

        #Create Languages
        test_language = Language.objects.create(name='English')

        #Create Books
        Book_list = []
        Num_books_auth_1 = 4
        for books in range(Num_books_auth_1):
            test_book = Book.objects.create(
                title='Book Title'+' '+ str(books),
                summary='My book summary',
                isbn='ABCDEF'+'1'+str(books),
                author=test_author,
                language=test_language,
            )

            Book_list.append(test_book)


        Num_books_auth_2 = 3
        for books in range(Num_books_auth_2):
            test_book = Book.objects.create(
                title='Book Title 2'+' '+ str(books),
                summary='My book summary',
                isbn='ABCDEFG'+'2'+str(books),
                author=test_author_2,
                language=test_language,
            )

            Book_list.append(test_book)

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()

        for book in Book_list:
            book.genre.set(genre_objects_for_book)
            book.save()

        # Create a BookInstance object for test_users
        book_instance_list = []

        for book_object in Book_list:
            book_instance_1 = BookInstance.objects.create(
                book = book_object,
                imprint = 'Some Imprint',
                status = 'a'
            )

            book_instance_2 = BookInstance.objects.create(
                book = book_object,
                imprint = 'Some Other Imprint',
                status = 'a'
            )

            book_instance_list.append(book_instance_1)
            book_instance_list.append(book_instance_2)

        #Setting the status of some books to be borrowed
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        num_borrowed_books = 5
        for i in range(num_borrowed_books):
            borrowed_book = book_instance_list[i]
            borrowed_book.due_back = return_date
            borrowed_book.borrower = test_user1
            borrowed_book.status = 'o'
            borrowed_book.save()
        
        #Creating Lord of the Rings
        Book.objects.create(
            title='Lord of the rings',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

    def test_hompage_response_without_authorization(self):
        '''Testing the response of the home page api'''
        response = self.client.get('http://127.0.0.1:8000/catalog/api/home')
        self.assertEqual(response.status_code,200)

    def test_homepage_response_body(self):
        '''Testing whether the homepage api shows the correct information'''
        response = self.client.get(
                                    'http://127.0.0.1:8000/catalog/api/home',
                                    format = 'json')
        response_body = response.json()

        expected_response = {
                                "num_books": 8,
                                "num_instances": 14,
                                "num_instances_available": 9,
                                "num_authors": 2,
                                "num_fantasy_genres": 2,
                                "num_lotr_books": 1
                            }

        self.assertEqual(response_body,expected_response)

    def test_homepage_response_with_librarian_authorization(self):
        '''Testing the response when the user is authorized as a librarian and makes a GET request'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_homepage_response_with_normal_authorization(self):
        '''Testing the response for a GET request from a non librarian user'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_homepage_post_response(self):
        '''Testing the response for a POST request'''
        response = self.client.post('http://127.0.0.1:8000/catalog/api/home')
        self.assertEqual(response.status_code,405)

    def test_homepage_put_response(self):
        '''Testing the response for a PUT request'''
        response = self.client.put('http://127.0.0.1:8000/catalog/api/home')
        self.assertEqual(response.status_code,405)

    def test_homepage_delete_response(self):
        '''Testing the response for a DELETE request'''
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/home')
        self.assertEqual(response.status_code,405)

    def test_homepage_post_response_with_librarian_authorization(self):
        '''Testing the response for a POST request whent he user is a librarian'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_homepage_put_response_with_librarian_authorization(self):
        '''Testing the response for a PUT request when the user is a librarian'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_homepage_delete_response_with_librarian_authorization(self):
        '''Testing the response for a DELETE request with Librarian Authorization'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_homepage_post_response_with_normal_authorization(self):
        '''Testing the response for POST request when the user is authorized'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_homepage_put_response_with_normal_authorization(self):
        '''Testing the response for a PUT request when the user is authorized'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_homepage_delete_response_with_normal_authorization(self):
        '''Testing the response for a DELETE request when the user is authorized'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/home',
            format="json")
        
        self.assertEqual(response.status_code,405)

class UserBorrowedBooksAPIViewTest(APITestCase):
    def setUp(self):
        #Creating Users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(username='testuser3', password='SomeStrongPassword')

        #One of the users is a librarian
        test_user1.save()
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        test_user1.save()
        test_user2.save()
        test_user3.save()

        #Create Authors
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_author_2 = Author.objects.create(first_name='John', last_name='Doe')

        #Create language
        test_language = Language.objects.create(name='English')

        #create Books
        book_1 = Book.objects.create(
            title='Book Title 1',
            summary='My book summary',
            isbn='ABCDEF 1',
            author=test_author,
            language=test_language
        )

        book_2 = Book.objects.create(
            title='Book Title 2',
            summary='My book summary',
            isbn='ABCDEF 2',
            author=test_author,
            language=test_language,
        )

        book_3 = Book.objects.create(
            title='Book Title 3',
            summary='My book summary',
            isbn='ABCDEF 3',
            author=test_author_2,
            language=test_language,
        )

        '''Creating Book Instances'''
        book_1_instance_list = []
        book_2_instance_list = []
        book_3_instance_list = []
        #Creating 2 instances of the first book
        for i in range(2):
            bookinstance_1 = BookInstance.objects.create(
                    id = 'e06f04a7-0ab7-4a43-b3b9-d288196393e'+str(i),
                    book = book_1,
                    imprint = 'Some Imprint',
                    status = 'a'
            )
            book_1_instance_list.append(bookinstance_1)

        #Creating 3 instances of the second book
        for i in range(3):
            bookinstance_1 = BookInstance.objects.create(
                id = '99ea43f7-5b60-4031-8a69-9e613790587'+str(i),
                book = book_2,
                imprint = 'Some imprint',
                status = 'a'
            )
            book_2_instance_list.append(bookinstance_1)

        #Creating 2 instances of the third book
        for i in range(2):
            bookinstance_1 = BookInstance.objects.create(
                id = '4f147358-7209-4ca5-ac7b-386902bdf19'+str(i),
                book = book_3,
                imprint = 'Some imprint',
                status = 'a'
            )
            book_3_instance_list.append(bookinstance_1)

        '''Setting the status of books 1 and 2 to being borrowed by user 1'''
        #This instance is due in 5 days
        return_date_1 = datetime.date.today() + datetime.timedelta(days=5)
        user_1_borrowed_book_1 = book_1_instance_list[0]
        user_1_borrowed_book_1.borrower = test_user1
        user_1_borrowed_book_1.status = 'o'
        user_1_borrowed_book_1.due_back = return_date_1
        user_1_borrowed_book_1.save()

        #This instance is due in 3 days
        return_date_2 = datetime.date.today() + datetime.timedelta(days=3)
        user_1_borrowed_book_2 = book_2_instance_list[0]
        user_1_borrowed_book_2.borrower = test_user1
        user_1_borrowed_book_2.status = 'o'
        user_1_borrowed_book_2.due_back = return_date_2
        user_1_borrowed_book_2.save()

        '''Setting the status of one of the instances of book 2 to borrowed by user 2'''
        #This instance is due in 4 days
        return_date_3 = datetime.date.today() + datetime.timedelta(days=4)
        user_2_borrowed_book_2 = book_2_instance_list[1]
        user_2_borrowed_book_2.borrower = test_user2
        user_2_borrowed_book_2.status = 'o'
        user_2_borrowed_book_2.due_back = return_date_3
        user_2_borrowed_book_2.save()

    def test_get_my_books_without_authorization(self):
        '''Trying to get books borrowed without giving authentication credentials'''
        response = self.client.get('http://127.0.0.1:8000/catalog/api/mybooks')
        self.assertEqual(response.status_code,401)

    def test_put_my_books_without_authorization(self):
        '''Trying to perform a PUT requests without authorization'''
        response = self.client.put('http://127.0.0.1:8000/catalog/api/mybooks')
        self.assertEqual(response.status_code,401)

    def test_post_my_books_without_authorization(self):
        '''Tests trying to perform POST request without authorization'''
        response = self.client.post('http://127.0.0.1:8000/catalog/api/mybooks')
        self.assertEqual(response.status_code,401)

    def test_delete_my_books_without_authorization(self):
        '''Tests Trying to perform DELETE request without authorization'''
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/mybooks')
        self.assertEqual(response.status_code,401)

    def test_get_my_books_response_user_1(self):
        '''Tests the response of trying to get books borrowed by user 1'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,200)


    def test_get_my_books_response_body_user_1(self):
        '''Tests the response of trying to get books borrowed by user 1'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        response_body = response.json()

        return_date_1 = (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        return_date_2 = (datetime.date.today() + datetime.timedelta(days=3)).strftime('%Y-%m-%d')

        expected_response = [
            {
                "id": '99ea43f7-5b60-4031-8a69-9e613790587'+'0',
                "book": 'Book Title 2',
                "due_back": return_date_2,
                "borrower": 'testuser1'
            }, 
            {
                "id": 'e06f04a7-0ab7-4a43-b3b9-d288196393e'+'0',
                "book": 'Book Title 1',
                "due_back": return_date_1,
                "borrower": 'testuser1'
            }
        ]

        self.assertEqual(response_body,expected_response)

    def test_post_my_books_response_user_1(self):
        '''Tests the response of trying to post books borrowed by user 1'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_put_my_books_response_user_1(self):
        '''Tests the response of trying to PUT books borrowed by user 1'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_delete_my_books_response_user_1(self):
        '''Tests the response of trying to DELETE books borrowed by user 1'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)
        
    def test_get_my_books_response_user_2(self):
        '''Tests the response of trying to get books borrowed by user 2'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_get_my_books_response_body_user_2(self):
        '''Tests the response body of trying to get books borrowed by user 2'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        response_body = response.json()

        return_date_1 = (datetime.date.today() + datetime.timedelta(days=4)).strftime('%Y-%m-%d')

        expected_response = [
            {
                "id": '99ea43f7-5b60-4031-8a69-9e613790587'+'1',
                "book": 'Book Title 2',
                "due_back": return_date_1,
                "borrower": 'testuser2'
            }
        ]

        self.assertEqual(response_body,expected_response)
    
    def test_post_my_books_response_user_2(self):
        '''Tests the response of trying to post books borrowed by user 2'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_put_my_books_response_user_2(self):
        '''Tests the response of trying to put books borrowed by user 2'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_delete_my_books_response_user_2(self):
        '''Tests the response of trying to delete books borrowed by user 2'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_get_my_books_response_user_3(self):
        '''Tests the response of trying to get books borrowed by user 1'''
        user_credentials = {
            "username": "testuser3",
            "password": "SomeStrongPassword"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_get_my_books_response_body_user_3(self):
        '''Tests the response of trying to get books borrowed by user 1'''
        user_credentials = {
            "username": "testuser3",
            "password": "SomeStrongPassword"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/mybooks',
            format="json")
        
        response_body = response.json()

        expected_response = [
        ]

        self.assertEqual(response_body,expected_response)

class AllBorrowedBooksAPIViewTest(APITestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(username='testuser3', password='SomeStrongPassword')
        test_user4 = User.objects.create_user(username='testuser4', password='SomeStrongPassword2')

        #One of the users is a librarian
        test_user1.save()
        Group.objects.create(name="Librarians")
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(test_user1)
        librarian_group.user_set.add(test_user4)
        test_user1.save()
        test_user2.save()
        test_user3.save()
        test_user4.save()

        #Create Authors
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_author_2 = Author.objects.create(first_name='John', last_name='Doe')

        #Create language
        test_language = Language.objects.create(name='English')

        #create Books
        book_1 = Book.objects.create(
            title='Book Title 1',
            summary='My book summary',
            isbn='ABCDEF 1',
            author=test_author,
            language=test_language
        )

        book_2 = Book.objects.create(
            title='Book Title 2',
            summary='My book summary',
            isbn='ABCDEF 2',
            author=test_author,
            language=test_language,
        )

        book_3 = Book.objects.create(
            title='Book Title 3',
            summary='My book summary',
            isbn='ABCDEF 3',
            author=test_author_2,
            language=test_language,
        )

        '''Creating Book Instances'''
        book_1_instance_list = []
        book_2_instance_list = []
        book_3_instance_list = []
        #Creating 2 instances of the first book
        for i in range(2):
            bookinstance_1 = BookInstance.objects.create(
                    id = 'e06f04a7-0ab7-4a43-b3b9-d288196393e'+str(i),
                    book = book_1,
                    imprint = 'Some Imprint',
                    status = 'a'
            )
            book_1_instance_list.append(bookinstance_1)

        #Creating 3 instances of the second book
        for i in range(3):
            bookinstance_1 = BookInstance.objects.create(
                id = '99ea43f7-5b60-4031-8a69-9e613790587'+str(i),
                book = book_2,
                imprint = 'Some imprint',
                status = 'a'
            )
            book_2_instance_list.append(bookinstance_1)

        #Creating 2 instances of the third book
        for i in range(2):
            bookinstance_1 = BookInstance.objects.create(
                id = '4f147358-7209-4ca5-ac7b-386902bdf19'+str(i),
                book = book_3,
                imprint = 'Some imprint',
                status = 'a'
            )
            book_3_instance_list.append(bookinstance_1)

        return_date_1 = datetime.date.today() + datetime.timedelta(days=5) #Due in 5 days
        return_date_2 = datetime.date.today() + datetime.timedelta(days=3) #Due in 3 days
        return_date_3 = datetime.date.today() + datetime.timedelta(days=4) #Due in 4 days

        '''Setting the status of books 1 and 2 to being borrowed by user 1(Librarian)'''
        #This instance is due in 5 days
        user_1_borrowed_book_1 = book_1_instance_list[0]
        user_1_borrowed_book_1.borrower = test_user1
        user_1_borrowed_book_1.status = 'o'
        user_1_borrowed_book_1.due_back = return_date_1
        user_1_borrowed_book_1.save()

        #This instance is due in 3 days
        user_1_borrowed_book_2 = book_2_instance_list[0]
        user_1_borrowed_book_2.borrower = test_user1
        user_1_borrowed_book_2.status = 'o'
        user_1_borrowed_book_2.due_back = return_date_2
        user_1_borrowed_book_2.save()

        '''Setting the status of one of the instances of all three books to borrowed by user 2'''
        #This instance is due in 4 days
        user_2_borrowed_book_2 = book_2_instance_list[1]
        user_2_borrowed_book_2.borrower = test_user2
        user_2_borrowed_book_2.status = 'o'
        user_2_borrowed_book_2.due_back = return_date_3
        user_2_borrowed_book_2.save()

        #Due in 4 days
        user_2_borrowed_book_3 = book_3_instance_list[0]
        user_2_borrowed_book_3.borrower = test_user2
        user_2_borrowed_book_3.status = 'o'
        user_2_borrowed_book_3.due_back = return_date_3
        user_2_borrowed_book_3.save()

        #Due in 5 days
        user_2_borrowed_book_1 = book_1_instance_list[1]
        user_2_borrowed_book_1.borrower = test_user2
        user_2_borrowed_book_1.status = 'o'
        user_2_borrowed_book_1.due_back = return_date_1
        user_2_borrowed_book_1.save()


    def test_get_all_borrowed_books_response_without_authorization(self):
        '''Test the response when using the API with no authorization credentials'''
        response = self.client.get('http://127.0.0.1:8000/catalog/api/borrowed/',follow=True)
        self.assertEqual(response.status_code,401)

    def test_post_borrowed_books_response_without_authorization(self):
        '''Test the response when using the API for a POST request with no authorization'''
        response = self.client.post('http://127.0.0.1:8000/catalog/api/borrowed/',follow=True)
        self.assertEqual(response.status_code,401)

    def test_put_borrowed_books_response_without_authorization(self):
        '''Test the response when using the API for a PUT request with no authorization credentials'''
        response = self.client.put('http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',follow=True)
        self.assertEqual(response.status_code,401)

    def test_delete_borrowed_books_response_without_authorization(self):
        '''Test the response when using the API for a DELETE request with no authorization credentials'''
        response = self.client.delete('http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',follow=True)
        self.assertEqual(response.status_code,401)

    def test_get_all_borrowed_books_response_with_user_authorization(self):
        '''Tests the response when using the API for a GET request with non librarian authorization credentials'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/borrowed/',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,403)

    def test_post_borrowed_books_response_with_user_authorization(self):
        '''Tests the response when using the API for a POST request with non librarian authorization credentials'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/borrowed/',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,403)

    def test_put_borrowed_books_response_with_user_authorization(self):
        '''Tests the response when using the API for a PUT request with non librarian authorization credentials'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,403)

    def test_delete_borrowed_books_response_with_user_authorization(self):
        '''Tests the response when using the API for a DELETE request with non librarian authorization credentials'''
        user_credentials = {
            "username": "testuser2",
            "password": "2HJ1vRV0Z&3iD"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,403)

    def test_get_borrowed_books_response_with_librarian_authorization(self):
        '''Tests the response when using the API for a GET request with libratian authorization credentials'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/borrowed/',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_post_borrowed_books_response_with_librarian_authorization(self):
        '''Tests the response when using the API for a POST request with libratian authorization credentials'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/borrowed/',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,405)

    def test_put_borrowed_books_response_with_librarian_authorization(self):
        '''Tests the response when using the API for a PUT request with libratian authorization credentials'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.put(
            'http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_delete_borrowed_books_response_with_librarian_authorization(self):
        '''Tests the response when using the API for a PUT request with libratian authorization credentials'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.delete(
            'http://127.0.0.1:8000/catalog/api/borrowed/99ea43f7-5b60-4031-8a69-9e6137905870',
            follow=True,
            format="json")
        
        self.assertEqual(response.status_code,200)

    def test_get_borrowed_books_response_body(self):
        '''Tests the body of the response when using the API for a GET request with libratian authorization credentials'''
        user_credentials = {
            "username": "testuser1",
            "password": "1X<ISRUkw+tuK"
        }

        response = self.client.post(
            'http://127.0.0.1:8000/catalog/api/token/',
            user_credentials,
            format="json"
        )

        response_body = response.json()
        access_token = response_body['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(
            'http://127.0.0.1:8000/catalog/api/borrowed/',
            follow=True,
            format="json")
        
        response_body = response.json()

        return_date_1 = (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d') #Due in 5 days
        return_date_2 = (datetime.date.today() + datetime.timedelta(days=3)).strftime('%Y-%m-%d') #Due in 3 days
        return_date_3 = (datetime.date.today() + datetime.timedelta(days=4)).strftime('%Y-%m-%d') #Due in 4 days

        book1_uuids = 'e06f04a7-0ab7-4a43-b3b9-d288196393e'
        book2_uuids = '99ea43f7-5b60-4031-8a69-9e613790587'
        book3_uuids = '4f147358-7209-4ca5-ac7b-386902bdf19'
        expected_response = [
            {
                "id": book2_uuids+'0',
                "book": "Book Title 2",
                "due_back": return_date_2,
                "borrower": "testuser1"
            },
            {
                "id": book2_uuids+'1',
                "book": "Book Title 2",
                "due_back": return_date_3,
                "borrower": "testuser2"
            },
            {
                "id": book3_uuids+'0',
                "book": "Book Title 3",
                "due_back": return_date_3,
                "borrower": "testuser2"
            },
            {
                "id": book1_uuids+'0',
                "book": "Book Title 1",
                "due_back": return_date_1,
                "borrower": "testuser1"
            },
            {
                "id": book1_uuids+'1',
                "book": "Book Title 1",
                "due_back": return_date_1,
                "borrower": "testuser2"
            }
        ]

        self.assertEqual(response_body,expected_response)


