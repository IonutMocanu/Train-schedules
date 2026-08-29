from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    # path('search_results/', include('SchedulesBackend.urls')),
]