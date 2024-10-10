
from django.contrib import admin
from django.urls import path, include
from twitter import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twitter.urls'))
]
