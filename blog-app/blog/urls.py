from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls')),  # This includes all diary URLs
    path('api/',include('diary.api_urls')),
]