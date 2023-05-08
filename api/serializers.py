from rest_framework import serializers
from books.models import Book, BookReview
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','id', 'first_name', 'last_name', 'email')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookSerializer()

    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'book', 'user')
