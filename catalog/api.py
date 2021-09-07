from rest_framework.serializers import ModelSerializer
from catalog.models import Author, Book, BookInstance, Genre
from rest_framework import (
    generics, 
    viewsets, 
    permissions, 
    mixins,
)
from .serializers import (
    AuthorSerializer, 
    RegisterSerializer, 
    UserSerializer, 
    RegisterLibrarianSerializer, 
    HomePageSerializer,
    BookInstanceSerializer,
)
from .permissions import IsLibrarian, OnlyLibrarians, JWT_authenticator #importing our custom permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import  APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    #Adding our own custom permission to the viewset
    permission_classes = [
        IsLibrarian
    ]
    serializer_class = AuthorSerializer


class BlacklistRefreshView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


#Register API
class RegisterApiView(generics.GenericAPIView):
    '''This class allows us to register new users for the api'''
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class RegisterLibrarianApiView(RegisterApiView):
    '''API view used to register librarians'''
    #overriding the permission_classes of the parent class to only give permission to librarians
    #this is because we do not want normal users to be able to make librarians
    permission_classes = [
        IsLibrarian
    ]

    serializer_class = RegisterLibrarianSerializer

class HomePageApiView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request):
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()

        # Available books (status = 'a')
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()

        num_fantasy_genres = Genre.objects.filter(name__icontains='Fantasy').count()

        num_lotr_books = Book.objects.filter(title__icontains='Lord of the rings').count()

        # The 'all()' is implied by default.
        num_authors = Author.objects.count()

        home_page_data = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fantasy_genres' : num_fantasy_genres,
        'num_lotr_books' : num_lotr_books,
        }

        result = HomePageSerializer(home_page_data).data

        return Response(result)

class UserBorrowedBooksApiView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = BookInstanceSerializer
    JWT_authenticator = JWTAuthentication()

    def get(self, request):
        user, _ = self.JWT_authenticator.authenticate(request)
        query_set = BookInstance.objects.filter(borrower=user).filter(status__exact='o').order_by('due_back')
        serializer = self.serializer_class(query_set,many=True)

        return Response(serializer.data)

class AllBorrowedBooksApiViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
    ):

    permission_classes = [
        OnlyLibrarians,
    ]

    queryset = BookInstance.objects.filter(status__exact = 'o').order_by('due_back')
    serializer_class = BookInstanceSerializer
