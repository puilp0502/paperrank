from django.urls import path

from .views import paper_rank, PaperListView, PaperDetailView

app_name = 'ranking'
urlpatterns = [
    path('rank/', paper_rank, name='rank'),
    path('papers/', PaperListView.as_view(), name='papers'),
    path('paper/<int:pk>/<slug:slug>/', PaperDetailView.as_view(), name='paper')
]
