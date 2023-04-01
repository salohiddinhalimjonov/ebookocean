from django.shortcuts import render, redirect
from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.utils.http import urlencode
from django.contrib import messages
from random import randint
from .forms import CustomUserForm, VerificationForm, LoginForm, EmailForm, ForgotPasswordForm
from .models import UserModel


def register_view(request):
    if request.method != 'POST':
        form = CustomUserForm()
    else:
        form = CustomUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = UserModel.objects.create_user(email, password, is_active=False)
            login(request, user, backend='src.user.backends.EmailBackend')
            send_email(request, email)
            redirect_url = reverse('verify')
            parameters = urlencode({'email': email})
            return redirect(f'{redirect_url}?{parameters}')
    context = {'form': form}

    return render(request, 'user/signup.html', context)


def verify_view(request):
    if request.method != 'POST':
        form = VerificationForm()
        email = request.GET.get('email')
    else:
        form = VerificationForm(request.POST)
        if form.is_valid():
            email = request.GET.get('email')
            if not email:
                return redirect('sign_up')
            code = form.cleaned_data.get('code')
            correct_code = cache.get(email)
            if correct_code:
                if correct_code == code:
                    user = get_object_or_404(UserModel, email=email)
                    user.is_active = True
                    user.save(update_fields=['is_active'])
                    return redirect('home')
                else:
                    messages.error(request, 'Incorrect Code!')
                    return render(request, 'user/verify.html', {'form': VerificationForm(request.GET)})
            else:
                messages.error(request, 'Code Expired!')
                return render(request, 'user/verify.html', {'form': VerificationForm(request.GET)})
    if not email:
        return redirect('sign_up')
    context = {'form': form, 'email': email}
    return render(request, 'user/verify.html', context)


def send_email(request, email, timeout=120):
    code = randint(100000, 999999)
    cache.set(email, str(code), timeout=timeout)
    try:
        send_mail('EbookOcean', f'Your verification Code: {code}', settings.EMAIL_HOST_USER, [email])
    except Exception as e:
        messages.error(request, f'{e.message}')
        return redirect('sign_up')


def resend_code_view(request):
    email = request.GET.get('email')
    if not email:
        return redirect('sign_up')
    redirect_url = reverse('verify')
    parameters = urlencode({'email': email})
    result = cache.get(email)
    if result:
        messages.error(request, "Please, try after the code expires!")
        return redirect(f'{redirect_url}?{parameters}')
    else:
        send_email(request, email)
        return redirect(f'{redirect_url}?{parameters}')


def sign_in_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user, backend='src.user.backends.EmailBackend')
                    return redirect('home')
                else:
                    redirect_url = reverse('verify')
                    parameters = urlencode({'email': user.email})
                    send_email(request, request.user.email)
                    messages.error(request, 'Please, activate your account!')
                    return redirect(f'{redirect_url}?{parameters}')
            else:
                messages.error(request, 'Email or password is not correct!')
                return redirect('sign_in')


    else:
        form = LoginForm()
    return render(request, 'user/signin.html', {'form': form})


def email_forgot_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if UserModel.objects.filter(email=email).exists():
                redirect_url = reverse('forgot_password')
                parameters = urlencode({'email': email})
                send_email(request, email, 180)
                return redirect(f'{redirect_url}?{parameters}')
            else:
                messages.error(request, 'User with the email does not exist!')
                return render(request, 'user/email_forgot.html', {'form': EmailForm(request.GET)})

    else:
        form = EmailForm()
    return render(request, 'user/email_forgot.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.GET.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, 'The two password fields did not match!')
                return render(request, 'user/forgot_password.html', {'form': ForgotPasswordForm(request.GET)})
            code = form.cleaned_data.get('code')
            correct_code = cache.get(email)
            if correct_code:
                if correct_code == code:
                    user = get_object_or_404(UserModel, email=email)
                    user.set_password(password1)
                    user.save(update_fields=['password'])
                    return redirect('home')
                else:
                    messages.error(request, 'Incorrect Code!')
                    return render(request, 'user/forgot_password.html', {'form': ForgotPasswordForm(request.GET)})
            else:
                messages.error(request, 'Code Expired!')
                return render(request, 'user/forgot_password.html', {'form': ForgotPasswordForm(request.GET)})

    else:
        form = ForgotPasswordForm()
    context = {'form': form}
    return render(request, 'user/forgot_password.html', context)


class DeleteProfileView(View):
    def get(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(guid=self.kwargs.get("guid"))
        except UserModel.DoesNotExist:
            return redirect('home')
        return render(request, 'user/delete_profile.html', {'object': user.email})

    def post(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(guid=self.kwargs.get("guid"))
        except UserModel.DoesNotExist:
            return redirect('home')
        if user:
            user.delete()
            return redirect('home')
        return render(request, 'user/delete_profile.html', {'user': user.email})


class UserDetailView(DetailView):
    # specify the model to use
    model = UserModel

    def get_object(self, queryset=None):
        return UserModel.objects.get(guid=self.kwargs.get("guid"))


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = UserModel

    fields = [
        "first_name",
        "last_name",
        "birthday",
        "country",
    ]

    def get_object(self, queryset=None):
        return UserModel.objects.get(guid=self.kwargs.get("guid"))

    def get_success_url(self):
        return reverse('profile', kwargs={
            'guid': self.object.guid,
        })
