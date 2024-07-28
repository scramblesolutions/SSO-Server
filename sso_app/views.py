from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.permissions import BasePermission
import base64

from sso_app.forms import LoginForm, RegisterForm, UserForm, ProfileForm

User = get_user_model()


def userinfoview(request):
    user = request.user
    profile = user.profile  # Assuming the Profile model is linked to the User model via a OneToOneField

    user_info = {
        "sub": str(user.id),
        "given_name": user.first_name,
        "family_name": user.last_name,
        "nickname": user.username,
        "email": user.email,
        "profile_image": profile.profile_image.url if profile.profile_image else '',
        "bio": profile.bio
    }

    return JsonResponse(user_info)


class HasScope(BasePermission):
    def has_permission(self, request, view):
        required_scope = 'info_profile'  # Define the required scope
        if not request.auth:
            return False

        # Assuming `request.auth` is the OIDC token with scope information
        token = request.auth
        scopes = token.get('scope', '').split()
        return required_scope in scopes


def image_to_base64(image_field):
    """
    Convert an image field to a base64 string.
    """
    if not image_field:
        return None

    # Read the image file
    image_data = image_field.read()

    # Encode the image to base64
    base64_encoded_image = base64.b64encode(image_data).decode('utf-8')

    return base64_encoded_image


def userinfo(claims, user):
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['picture'] = image_to_base64(user.profile.profile_image)
    claims['profile'] = user.profile.bio

    return claims


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next_url = request.POST.get('next')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('custom_home')  # Replace 'home' with your redirect target
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        next_url = request.GET.get('next')
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'next': next_url
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('custom_login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('custom_home')


def home_view(request):
    return render(request, 'home.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
