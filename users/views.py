from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm, UserUpdateForm
from django.contrib import messages


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, 'registration/profile.html', {'user': request.user})


class ProfileUpdateView(View, LoginRequiredMixin):
    def get(self, request):
        messages.success(request, "Welcome to personal_edit page")
        user_form = UserUpdateForm(instance=request.user)
        return render(request, 'registration/profile_edit.html', {"form": user_form})

    def post(self, request):
        user_form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "You have successfully updated your profile")
            return redirect('profile')

        return render(request, 'registration/profile_edit.html', {"form": user_form})
