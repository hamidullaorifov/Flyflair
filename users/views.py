from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import EmailVerificationToken
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password


## extra_tags="danger" -- Use tags for the alert color.


def send_verification_email(request, user):
    def send_email():
        email_subject = "Email Verification"
        email_message = render_to_string('email_verification.html', {"verification_link": verification_link, "user": user})

        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=email_message,
        )

    token_obj, created = EmailVerificationToken.objects.get_or_create(user=user)
    token_obj.generate_token()

    uid = urlsafe_base64_encode(str(user.pk).encode())

    token_url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token_obj.token})
    verification_link = settings.SITE_URL + token_url
    send_email()


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user:
        try:
            token_obj = EmailVerificationToken.objects.get(user=user, token=token)
            if not token_obj.is_token_valid():
                messages.error(request, "Verificaiton Token Expired. Please try again", extra_tags="danger")
                return redirect('register')

            if token_obj.is_verified:
                messages.success(request, "Email already verified", extra_tags="info")
                return redirect('login')

            token_obj.is_verified = True
            token_obj.save()

            user.is_active = True
            user.save()

            messages.success(request, "Your email has been successfully verified!")
            return redirect('login')

        except EmailVerificationToken.DoesNotExist:
            messages.error(request, "Invalid or expired verification link.")
            return redirect('signup')
    else:
        messages.error(request, "User not found.")
        return redirect('signup')


def resend_verification(request):
    email = request.GET.get("email")
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            send_verification_email(request, user)
            messages.info(request, "Verification code resent!", extra_tags="success")
        else:
            messages.info(request, "Account already verified.", extra_tags="info")
    except User.DoesNotExist:
        messages.error(request, "User not found.", extra_tags="danger")
    return redirect("login")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            name = email.split("@")[0].split(".") if "." in email.split("@")[0] else ["Jane", "Doe"]
            first_name = name[0].title()
            last_name = name[1].title()
            username = f"{first_name}_{last_name}"
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count() + 1}"
            user = User.objects.create_user(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            messages.success(request, "Account created successfully! Please verify your email", extra_tags="success")
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}", extra_tags="danger")
            return render(request, 'registration.html', {'form': form})

    return render(request, 'registration.html', {'form': RegisterForm()})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    resend_link = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                if not user.is_active:
                    resend_link = f"/resend-verification/?email={user.email}"
                else:
                    login(request, user)
                    next_url = request.POST.get("next") or request.GET.get("next") or 'home'
                    return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.", extra_tags="danger")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.", extra_tags="danger")

    return render(request, "login.html", {"resend_link": resend_link})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        return redirect("home")




@login_required(login_url="login")
def home_view(request):
    return render(request, "home.html")













