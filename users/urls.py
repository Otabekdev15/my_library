from django.urls import path
from users .views import SignUpView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', ProfileUpdateView.as_view(), name='profile_edit')

]