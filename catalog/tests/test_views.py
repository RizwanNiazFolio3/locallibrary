from django.contrib.auth.decorators import login_required
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.views.generic.edit import DeleteView
from catalog.models import Author
import datetime
from django.utils import timezone
from django.contrib.auth.models import User # Required to assign User as a borrower
from catalog.models import BookInstance, Book, Genre, Language
import uuid
from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)

class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely Imprint, 2016',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        # Now change all books to be on loan
        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my-borrowed'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)

        # Confirm all books belong to testuser1 and are on loan
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')

    def test_pages_ordered_by_due_date(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
        self.assertRedirects(response, reverse('borrowed'))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')

class AuthorCreateViewTest(TestCase):
    def setUp(self):
        #Create user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        #Give user permission
        permission = Permission.objects.get(name='Set book as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()
    
    def test_redirect_if_not_logged_in(self):
        '''Checks if the user is redirected to the login page if they are not already logged in'''
        response = self.client.get(reverse('author-create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_forbidden_if_logged_in_without_permission(self):
        '''Checks if user has correct permission if they are logged in. If the user does not have permission they given a 403 forbidden message'''
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        ''''Checks if the user is logging in with permission. If they have permission the respoonse is 200 OK'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-create'))

        # Check that it lets us login and that we have the correct permissions
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_is_used(self):
        '''Checks if the correct template is being used'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is being used
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_correct_initial_date_is_used(self):
        '''This checks if the date of death is initially 11/6/2020'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-create'))

        #Get initial date of death and check
        initial_date_of_death = '11/06/2020'
        self.assertEqual(response.context['form'].initial['date_of_death'], initial_date_of_death)

    def test_redirects_to_author_details(self):
        '''This checks if the user is redirected to the author details page when they enter a valid author'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        #Creating a valid author
        author_first_name = 'FirstName'
        author_last_name = 'LastName'
        author_date_of_Birth = datetime.date.today() - datetime.timedelta(weeks=70*12*52)
        author_date_of_death = datetime.date.today()

        #Inputting Data
        response = self.client.post(reverse('author-create'), {'first_name': author_first_name,
                                                                'last_name': author_last_name,
                                                                'date_of_death': author_date_of_death,
                                                                'date_of_birth': author_date_of_Birth})
        
        #Checking if it redirects to the author details page of the author we just made
        self.assertRedirects(response,reverse('author-detail',kwargs={'pk':1}))


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_authors = 3
        num_of_books_per_author = 2

        test_language = Language.objects.create(name='English')
        test_genre = Genre.objects.create(name='Fantasy')

        for author_id in range(num_of_authors):
            test_author = Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

            test_author.save()

            for author_book_id in range(num_of_books_per_author):
                test_book = Book.objects.create(
                    title = f'BookTitle {author_id} {author_book_id}',
                    author = test_author,
                    summary = 'Book Summary',
                    isbn = f'ABCDEFG{author_id}{author_book_id}',
                    language = test_language,
                )
                test_book.genre.set = Genre.objects.all()

                test_book.save()

                BookInstance.objects.create(
                    book = test_book,
                    imprint='Unlikely Imprint, 2016'
                )
            
        tolkien = Author.objects.create(
            first_name = "J.R.R",
            last_name = "Tolkien"
        )
        tolkien.save()

        lotr_book = Book.objects.create(
            title = "Lord of The Rings",
            author = tolkien,
            summary = 'Some summary',
            isbn = "ABCDEFG",
            language = test_language,
        )

        lotr_book.genre.set(Genre.objects.all())
        lotr_book.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_number_books(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_books'],7)

    def test_number_book_instances(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_instances'],6)

    def test_number_book_instances_available(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_instances_available'],0)

    def test_number_authors(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_authors'],4)

    def test_number_fantasy_genres(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_fantasy_genres'],1)

    def test_number_lotr_books(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_lotr_books'],1)

    def test_number_visits(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['num_visits'],0)


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_books = 13
        test_language = Language.objects.create(name = 'English')
        test_language.save()
        for book_id in range(number_of_books):
            test_author = Author.objects.create(
                first_name=f'Christian {book_id}',
                last_name=f'Surname {book_id}',
            )

            Book.objects.create(
                title = f'BookTitle {book_id}',
                author = test_author,
                summary = 'Book Summary',
                isbn = f'ABCDEFG{book_id}',
                language = test_language
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 10)

    def test_lists_all_books(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('books')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 3)


class AuthorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        Author.objects.create(
            first_name='Christian',
            last_name='Surname',
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/author/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('author-detail',kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('author-detail',kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_detail.html')

    def test_http404_for_invalid_book(self):
        response = self.client.get(reverse('author-detail',kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)

class BookDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        test_language = Language.objects.create(name = 'English')
        test_author = Author.objects.create(
            first_name='Christian',
            last_name='Surname'
        )
        test_author.save()
        test_language.save()

        Book.objects.create(
            title = 'Book Name',
            summary = 'Some summary',
            isbn = 'ABCDEFGHI',
            author = test_author,
            language = test_language
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/book/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('book-detail',kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('book-detail',kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_detail.html')

    def test_http404_for_invalid_book(self):
        response = self.client.get(reverse('book-detail',kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)


class AuthorUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        #Give user permission
        permission = Permission.objects.get(name='Set book as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()

        test_author = Author.objects.create(
            first_name='Christian',
            last_name='Surname',
            date_of_birth = datetime.date.today() - datetime.timedelta(days=12000),
            date_of_death = datetime.date.today() - datetime.timedelta(days=2)
        )
        test_author.save()
    
    def test_redirect_if_not_logged_in(self):
        '''Checks if the user is redirected to the login page if they are not already logged in'''
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_forbidden_if_logged_in_without_permission(self):
        '''Checks if user has correct permission if they are logged in. If the user does not have permission they given a 403 forbidden message'''
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)

    def test_allowed_if_logged_in_with_permission(self):
        ''''Checks if the user is logging in with permission. If they have permission the respoonse is 200 OK'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))

        # Check that it lets us login and that we have the correct permissions
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_is_used(self):
        '''Checks if the correct template is being used'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is being used
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_http404_for_invalid_author(self):
        '''Enter the url for an author that does not exist'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-update',kwargs={'pk':2}))
        self.assertEqual(response.status_code, 404)

    def test_correct_data_in_fields(self):
        '''Get the information of the author using a get request'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))

        '''Check if info is correct'''
        self.assertEqual(response.context['form'].initial['first_name'],'Christian')
        self.assertEqual(response.context['form'].initial['last_name'],'Surname')
        self.assertEqual(response.context['form'].initial['date_of_birth'],datetime.date.today() - datetime.timedelta(days=12000))
        self.assertEqual(response.context['form'].initial['date_of_death'],datetime.date.today() - datetime.timedelta(days=2))

    def test_update(self):
        '''Login and go to author update page for the author that needs to be updated'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-update',kwargs={'pk':1}))

        '''Get information of author from the context'''
        test_first_name = response.context['form'].initial['first_name']
        test_last_name = response.context['form'].initial['last_name']
        test_date_of_birth = response.context['form'].initial['date_of_birth']
        test_date_of_death = response.context['form'].initial['date_of_death']

        '''Update information using a post request'''
        response = self.client.post(
            reverse('author-update', kwargs={'pk': 1}), 
            {
                'first_name': 'J.D', 
                'last_name': 'Salinger',
                'date_of_birth': datetime.date(1919,1,1),
                'date_of_death': datetime.date(2010,1,27)})

        '''Check if status is 302: Found'''
        self.assertEqual(response.status_code,302)

        '''Check if the values for the author have been changed in the database'''
        test_author = Author.objects.get(id=1)
        self.assertEqual(test_author.first_name,'J.D')
        self.assertEqual(test_author.last_name,'Salinger')
        self.assertEqual(test_author.date_of_birth,datetime.date(1919,1,1))
        self.assertEqual(test_author.date_of_death,datetime.date(2010,1,27))


class AuthorDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        #Give user permission
        permission = Permission.objects.get(name='Set book as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()

        num_authors = 2
        for authors in range(num_authors):
            test_author = Author.objects.create(
                first_name=f'Christian {authors}',
                last_name=f'Surname {authors}',
                date_of_birth = datetime.date.today() - datetime.timedelta(days=12000),
                date_of_death = datetime.date.today() - datetime.timedelta(days=2)
            )
            test_author.save()
    
    def test_redirect_if_not_logged_in(self):
        '''Checks if the user is redirected to the login page if they are not already logged in'''
        response = self.client.get(reverse('author-delete',kwargs={'pk':1}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_forbidden_if_logged_in_without_permission(self):
        '''Checks if user has correct permission if they are logged in. If the user does not have permission they given a 403 forbidden message'''
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 403)

    def test_allowed_if_logged_in_with_permission(self):
        ''''Checks if the user is logging in with permission. If they have permission the respoonse is 200 OK'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-delete',kwargs={'pk':1}))

        # Check that it lets us login and that we have the correct permissions
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_is_used(self):
        '''Checks if the correct template is being used'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is being used
        self.assertTemplateUsed(response, 'catalog/author_confirm_delete.html')

    def test_http404_for_invalid_author(self):
        '''Enter the url for an author that does not exist'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-delete',kwargs={'pk':3}))
        self.assertEqual(response.status_code, 404)

    def test_page_has_correct_author(self):
        '''Enter url for the delete page of an author'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-delete',kwargs={'pk':1}))

        '''Check if author is correct'''
        test_author = response.context['author']
        self.assertEqual(str(test_author),'Surname 0, Christian 0')
    
    def test_redirects(self):
        '''Login, then delete author'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('author-delete',kwargs={'pk':1}),follow=True)

        '''Check if page redirects'''
        self.assertRedirects(response, reverse('authors'), status_code=302)

    def test_if_response_code_is_correct(self):
        '''Login then delete author'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('author-delete',kwargs={'pk':1}))

        '''Check if the status code is 302:Found'''
        self.assertEqual(response.status_code, 302)
    
    def test_if_author_is_deleted(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response_delete = self.client.post(reverse('author-delete',kwargs={'pk':1}))

        '''Check if author exists'''
        authors = Author.objects.count()
        self.assertEqual(authors,1)

class BookCreateViewTest(TestCase):
    def setUp(self):
        #Create user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        #Give user permission
        permission = Permission.objects.get(name='Set book as returned')
        test_user1.user_permissions.add(permission)
        test_user1.save()
    
    def test_redirect_if_not_logged_in(self):
        '''Checks if the user is redirected to the login page if they are not already logged in'''
        response = self.client.get(reverse('book-create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_forbidden_if_logged_in_without_permission(self):
        '''Checks if user has correct permission if they are logged in. If the user does not have permission they given a 403 forbidden message'''
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        ''''Checks if the user is logging in with permission. If they have permission the respoonse is 200 OK'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('book-create'))

        # Check that it lets us login and that we have the correct permissions
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_is_used(self):
        '''Checks if the correct template is being used'''
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)

        #Check if the correct template is being used
        self.assertTemplateUsed(response, 'catalog/book_form.html')

    def test_redirects_to_book_detail_view(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        test_language = Language.objects.create(
            name = "English"
        )

        test_author = Author.objects.create(
            first_name = 'FirstName',
            last_name = "LastName"
        )

        test_genre = Genre.objects.create(
            name = "Fantasy"
        )

        book_title = 'Book Name',
        book_summary = 'Some summary',
        book_isbn = 'ABCDEFGHI',
        book_author = test_author,
        book_language = test_language
        book_genre = test_genre

        response = self.client.post(reverse("book-create"),{'title': book_title,
                                                            'summary': book_summary,
                                                            'isbn': book_isbn,
                                                            'author':book_author,
                                                            'language':book_language,
                                                            'genre':book_genre})

        self.assertRedirects(response,reverse('book-detail',kwargs={'pk': 1}), status_code=200)

