from rest_framework import viewsets, permissions
from .serializers import BookSerializer
from .models import Book
from .permissions import IsLibrarian


class BookViewSet(viewsets.ModelViewSet):
    """This viewset provides create, retrieve, update and delete apis for books"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [
        IsLibrarian
    ]