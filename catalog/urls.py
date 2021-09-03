from django.urls import path
from . import views
from rest_framework import routers
from .api  import (
    AuthorViewSet, 
    RegisterApiView, 
    BlacklistRefreshView, 
    RegisterLibrarianApiView, 
    HomePageApiView,
    UserBorrowedBooksApiView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from . import custom_tokens

router = routers.DefaultRouter()
router.register('api/authors',AuthorViewSet,'author-api')

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('api/token/', custom_tokens.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),#Views needed to use the simplejwt package
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#View needed to create a new access token once the current one expires
    path('api/register',RegisterApiView.as_view(), name='user-register-api'),#View needed to create
    path('api/logout', BlacklistRefreshView.as_view(), name="logout"),#API used to blacklist refresh token
    path('api/register-librarian', RegisterLibrarianApiView.as_view(), name='librarian-register-api'),#API used to register librarians
    path('api/home', HomePageApiView.as_view(),name = 'home-page'),
    path('api/mybooks', UserBorrowedBooksApiView.as_view(), name='mybooks-api'),
]

urlpatterns += router.urls
