from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


# Create your tests here.
class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("list"))

        self.assertContains(response, " No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description='des1', isbn='111')
        book2 = Book.objects.create(title="Book2", description='des2', isbn='222')
        book3 = Book.objects.create(title="Book3", description='des3', isbn='333')

        response = self.client.get(reverse('list') + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
            self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description='des1', isbn='111')

        response = self.client.get(reverse('detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_book(self):
        book1 = Book.objects.create(title="God", description='des1', isbn='111')
        book2 = Book.objects.create(title="Tom", description='des2', isbn='222')
        book3 = Book.objects.create(title="Deal", description='des3', isbn='333')

        response = self.client.get(reverse('list') + "?q=God")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('list') + "?q=Tom")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('list') + "?q=Deal")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

    def test_add_review(self):
        book = Book.objects.create(title="God", description='des1', isbn='111')

        user = CustomUser.objects.create(username="Otabek",
                                         first_name="Otabek",
                                         last_name="Mikhliev",
                                         email="otabekmikhliev15@gmail.com")
        user.set_password("2001")
        user.save()
        self.client.login(username="Otabek", password="2001")

        self.client.post(reverse('reviews', kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": 'nice book'
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)




