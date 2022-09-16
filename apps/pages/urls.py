from django.urls import path
from .views import HomePageView, ArchivePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('pages', ArchivePageView.as_view(), name='archive')
]
