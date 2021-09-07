from rest_framework import serializers
from catalog.models import Author
from .models import Book
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """This class converts model"""

    class Meta:
        model = Book
        fields = '__all__'


