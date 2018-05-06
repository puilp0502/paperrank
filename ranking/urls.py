from django.urls import path

from .views import paper_rank


app_name = 'ranking'
urlpatterns = [
    path('rank/', paper_rank, name='rank'),
]
