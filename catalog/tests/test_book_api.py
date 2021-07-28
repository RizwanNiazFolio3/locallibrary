from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Book, Genre

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

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/api/books/')
        self.assertEqual(response.status_code, 200)

    def test_list_books_status(self):
        
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/catalog/api/books/')

        self.assertEqual(response.status_code, 200)

    def test_create_book_status(self):
        
        client = APIClient()
        response = client.post('http://127.0.0.1:8000/catalog/api/books/',
            {
                "title":"book_title2",
                "summary": "summary2",
                "isbn": "1234567891248",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201) # 201 means object successfully created

    def test_get_book_using_id(self):
        
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/catalog/api/books/1/')

        self.assertEqual(response.status_code, 200)

    def test_delete_book_using_id(self):
        
        client = APIClient()
        response = client.delete('http://127.0.0.1:8000/catalog/api/books/1/')

        # Status code 204 means that the request completed successfully but no response was returned
        self.assertEqual(response.status_code, 204)

    def test_update_book_using_id(self):
        
        client = APIClient()
        response = client.put('http://127.0.0.1:8000/catalog/api/books/1/',
            {
                "title":"book_title_updated",
                "summary": "summary_updated",
                "isbn": "1234567891247",
                "genre": [1]
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
