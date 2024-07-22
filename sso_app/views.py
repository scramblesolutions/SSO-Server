from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from oidc_provider.lib.claims import StandardScopeClaims
from oidc_provider.lib.utils.common import cors_allow_any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from .serializers import UserSerializer
from .utils import CustomScopeClaims

from django.views.decorators.http import require_http_methods

from oidc_provider.lib.utils.oauth2 import protected_resource_view

from sso_app.forms import LoginForm, RegisterForm, UserForm, ProfileForm

User = get_user_model()


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# @csrf_exempt
# @login_required
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


# @require_http_methods(['GET'])
# @protected_resource_view(['info_profile'])
# def userinfo(request):
#     user = get_user_model().objects.get(id=2)  # request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)
#     # return JsonResponse({})

@require_http_methods(['GET', 'POST', 'OPTIONS'])
@protected_resource_view(['openid'])
def userinfo(request, *args, **kwargs):
    """
    Create a dictionary with all the requested claims about the End-User.
    See: http://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse

    Return a dictionary.
    """

    def set_headers(response):
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        cors_allow_any(request, response)
        return response

    if request.method == 'OPTIONS':
        return set_headers(HttpResponse())

    token = kwargs['token']

    dic = {
        'sub': token.id_token.get('sub'),
    }

    standard_claims = StandardScopeClaims(token)
    dic.update(standard_claims.create_response_dic())

    if settings.OIDC_EXTRA_SCOPE_CLAIMS:
        extra_claims = settings.get('OIDC_EXTRA_SCOPE_CLAIMS', import_str=True)(token)
        dic.update(extra_claims.create_response_dic())

    success_response = JsonResponse(dic, status=200)
    set_headers(success_response)

    return success_response


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
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('custom_home')


def home_view(request):
    return render(request, 'home.html')
