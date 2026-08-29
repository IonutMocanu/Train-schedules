from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', include('UsersBackend.urls')),
    path('login/', include('UsersBackend.urls')),
    path('search/', include('SearchBackend.urls')),
]