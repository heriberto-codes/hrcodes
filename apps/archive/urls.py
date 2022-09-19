from django.urls import path
from .views import ArchivePageView


urlpatterns = [
    path('', ArchivePageView.as_view(), name='archive')
]
  