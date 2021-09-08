from catalog.models import Author
from rest_framework import generics, viewsets, permissions
from .serializers import AuthorSerializer, RegisterSerializer, UserSerializer, RegisterLibrarianSerializer
from .permissions import IsLibrarian #importing our custom permission
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import  APIView


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
    def post(self, request: Request) -> Response:
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




