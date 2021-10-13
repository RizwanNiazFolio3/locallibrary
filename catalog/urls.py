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
    AllBorrowedBooksApiViewset,
    BookViewSet,
)
from rest_framework_simplejwt.views import TokenRefreshView
from . import custom_tokens


router = routers.DefaultRouter()
router.register('api/authors',AuthorViewSet,'author-api')
router.register('api/borrowed',AllBorrowedBooksApiViewset, 'borrowed-books-api')
router.register('api/books',BookViewSet,'book-api')

urlpatterns = [
    path('api/token/', custom_tokens.AddIsLibrarianClaimView.as_view(), name='token_obtain_pair'),#Views needed to use the simplejwt package
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#View needed to create a new access token once the current one expires
    path('api/register',RegisterApiView.as_view(), name='user-register-api'),#View needed to create
    path('api/logout', BlacklistRefreshView.as_view(), name="logout"),#API used to blacklist refresh token
    path('api/register-librarian', RegisterLibrarianApiView.as_view(), name='librarian-register-api'),#API used to register librarians
    path('api/home', HomePageApiView.as_view(),name = 'home-page'),
    path('api/mybooks', UserBorrowedBooksApiView.as_view(), name='mybooks-api'),
]

urlpatterns += router.urls
