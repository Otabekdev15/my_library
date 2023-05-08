from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.serializers import BookReviewSerializer
from books.models import BookReview
from rest_framework.response import Response
from rest_framework import generics


# Create your views here.
# class BookReviewDetailAPIView(APIView):
#     def get(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(book_review)
#         return Response(data=serializer.data)


class BookReviewsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')


class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    lookup_field = 'id'
