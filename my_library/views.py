from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import BookReview


def reviews_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 7)
    paginator = Paginator(book_reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)

    return render(request, "reviews.html", {"page_obj": page_object})
