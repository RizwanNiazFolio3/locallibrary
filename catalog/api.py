from catalog.models import Author
from rest_framework import viewsets, permissions
from .serializers import AuthorSerializer
from .permissions import IsLibrarian #importing our custom permission

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    #Adding our own custom permission to the viewset
    permission_classes = [
        IsLibrarian
    ]
    serializer_class = AuthorSerializer

