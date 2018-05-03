from django.urls import path

from .views import paper_rank


urlpatterns = [
    path('rank/', paper_rank),
]
