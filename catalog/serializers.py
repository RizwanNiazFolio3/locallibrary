from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from catalog.models import Author, BookInstance, Book
from django.contrib.auth.models import User, Group
from .models import Book, Genre, Language


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """This class converts model"""

    class Meta:
        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for the Register view'''
    class Meta:
        model = User
        fields = ('id','username','password')
        #Specifying that the password field should only be write_only
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data: dict) -> User:
        #Creating a new user once it is validated
        user = User.objects.create_user(validated_data['username'], password = validated_data['password'])
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    '''The serializer for the user class, the returned json will only contain the id and username of the new created user'''
    class Meta:
        model = User
        fields = ['id','username','groups']

class RegisterLibrarianSerializer(RegisterSerializer):
    '''The serializer to register other librarians'''
    #We must override the create method of the parent class so that it now allows us to the user being created to the librarian group
    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(validated_data['username'], password = validated_data['password'])
        librarian_group = Group.objects.get(name="Librarians")
        librarian_group.user_set.add(user)
        return user

class HomePageSerializer(serializers.Serializer):
    num_books = serializers.IntegerField()
    num_instances = serializers.IntegerField()
    num_instances_available = serializers.IntegerField()
    num_fantasy_genres = serializers.IntegerField()
    num_lotr_books = serializers.IntegerField()
    num_authors = serializers.IntegerField()

class BookInstanceSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    borrower = serializers.StringRelatedField()
    class Meta:
        model = BookInstance
        fields = ['id','book','due_back','borrower']
    
