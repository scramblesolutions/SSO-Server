from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import sso_app.views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('sso_app.urls')),
    path('', sso_app.views.home_view, name='custom_home'),
    path('', include('oidc_provider.urls', namespace='oidc_provider')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
