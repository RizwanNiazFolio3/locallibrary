from rest_framework.response import Response
from rest_framework.request import Request
from catalog.models import Author, Book
from rest_framework import viewsets, permissions
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsLibrarian #importing our custom permission
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import datetime, jwt

class BookViewSet(viewsets.ModelViewSet):
    """This viewset provides create, retrieve, update and delete apis for books"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [
        IsLibrarian
    ]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    #Adding our own custom permission to the viewset
    permission_classes = [
        IsLibrarian
    ]
    serializer_class = AuthorSerializer


class LoginView(APIView):
    """Provides login api for user"""

    def post(self, request: Request) -> Response:

        username = request.data["username"]
        password = request.data["password"]

        # We fetch the user. Since username is unique, we can filter and fetch first
        user = User.objects.filter(username=username).first()

        if user is not None:
            
            if user.check_password(password):

                # Username and password are correct so creating jwt token

                payload = {
                    "id" : user.id,
                    "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # Expires in 60 minutes
                    "iat" : datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")

                return Response({
                    "user id" : user.id,
                    "token" : token
                })

            else:
                raise AuthenticationFailed("Incorrect password")
            
        else:
            raise AuthenticationFailed("Incorrect username")
