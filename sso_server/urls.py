from django.contrib import admin
from django.urls import path, include

import sso_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('userinfo/', sso_app.views.userinfo, name='user_info'),
    path('accounts/', include('sso_app.urls')),
    path('home/', sso_app.views.home_view, name='custom_home'),
    path('', include('oidc_provider.urls', namespace='oidc_provider')),
    # path('api/userinfo/', sso_app.views.userinfo, name='api-userinfo'),

]
