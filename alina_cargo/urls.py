from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('packages/', include('packages.urls')),
]
urlpatterns+=staticfiles_urlpatterns()
