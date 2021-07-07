from django.test import TestCase

from catalog.models import Author, Genre, Language, Book, BookInstance

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
    
    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')
    
    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name = 'Urdu')

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_name_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    
    def test_name_is_name_of_language(self):
        language = Language.objects.get(id=1)
        expected_name = f'{language.name}'
        self.assertEqual(str(language),expected_name)


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name = 'Testing')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_name_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    
    def test_name_is_name_of_Genre(self):
        genre = Genre.objects.get(id=1)
        expected_name = f'{genre.name}'
        self.assertEqual(str(genre),expected_name)

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name = 'TestGenre')
        Genre.objects.create(name = 'TestGenre2')
        Genre.objects.create(name = 'TestGenre3')
        Genre.objects.create(name = 'TestGenre4')
        Language.objects.create(name = 'TestLanguage')
        Author.objects.create(first_name='TestFirstName', last_name='TestLastName')
        #genre = Genre.objects.get(id=1)
        language = Language.objects.get(id=1)
        author = Author.objects.get(id=1)

        Book.objects.create(title ='TestBook', 
                            author = author, 
                            language = language, 
                            isbn = '1234567891011', 
                            summary= 'TestSummary')
    
    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
    
    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')
    
    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')
    
    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length,200)
    
    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length,1000)
    
    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length,13)

    def test_summary_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field('summary').help_text
        self.assertEqual(help_text,'Enter a brief description of the book')
    
    def test_isbn_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field('isbn').help_text
        self.assertEqual(help_text,'13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    def test_genre_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field('genre').help_text
        self.assertEqual(help_text,'Select a genre for this book')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1')

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        all_genres = Genre.objects.all()
        book.genre.set(all_genres)
        book.save()
        self.assertEqual(book.display_genre(),'TestGenre, TestGenre2, TestGenre3')

    def test_name_is_title_of_Book(self):
        book = Book.objects.get(id=1)
        expected_name = f'{book.title}'
        self.assertEqual(str(book),expected_name)




