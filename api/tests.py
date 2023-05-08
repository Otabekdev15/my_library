from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from books.models import Book, BookReview
from users.models import CustomUser


# Create your tests here.
class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='Otabek', first_name='Otabek')
        self.user.set_password('2001')
        self.user.save()
        self.client.login(username='Otabek', password='2001')

    def test_book_review_detail(self):
        permission_classes = [IsAuthenticated]

        book = Book.objects.create(title='Book1', description='Description1', isbn='123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')

        response = self.client.get(reverse('api:reviews-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'good book')
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], '123')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'Otabek')
        self.assertEqual(response.data['user']['username'], 'Otabek')

    def test_delete_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')

        response = self.client.delete(reverse('api:reviews-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')

        response = self.client.patch(reverse('api:reviews-detail', kwargs={'id': br.id}), data={'stars_given': 5})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)

    def test_put_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')

        response = self.client.patch(reverse('api:reviews-detail',
                                             kwargs={'id': br.id}),
                                     data={'stars_given': 5,
                                           'comment': 'nice book',
                                           'user_id': self.user.id,
                                           'book_id': book.id})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)
        self.assertEqual(br.comment, 'nice book')

    def test_book_review_list(self):
        permission_classes = [IsAuthenticated]
        user_two = CustomUser.objects.create(username='Ali', first_name='Ali')
        book = Book.objects.create(title='Book', description='Description1', isbn='123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=4, comment='nice book')

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], br.id)
        self.assertEqual(response.data[0]['stars_given'], br.stars_given)
        self.assertEqual(response.data[0]['comment'], br.comment)

        self.assertEqual(response.data[1]['id'], br_two.id)
        self.assertEqual(response.data[1]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data[1]['comment'], br_two.comment)
