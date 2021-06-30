from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Book, Author, BookInstance, Genre

from django.views import generic

def index(request: HttpRequest) -> HttpResponse:
    """View function for home page of site."""
    '''This function takes an HttpRequest for the homepage and uses the index.html template to render it'''

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_fantasy_genres = Genre.objects.filter(name__icontains='Fantasy').count()

    num_lotr_books = Book.objects.filter(title__icontains='Lord of the rings').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fantasy_genres' : num_fantasy_genres,
        'num_lotr_books' : num_lotr_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author        
