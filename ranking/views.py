from django.db.models import Sum, Q
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView

from .models import Paper


def annotate_ranking(queryset):
    for i, publisher in enumerate(queryset):
        publisher['ranking'] = i + 1
    return queryset


def paper_rank(request):
    try:
        year = int(request.GET['year'])
    except (KeyError, ValueError):
        year = timezone.now().year

    this_year = Paper.objects.filter(year=year) \
        .values('publisher', 'publisher__name').annotate(score_sum=Sum('score')) \
        .order_by('-score_sum', 'publisher__name')
    last_year = Paper.objects.filter(year=year-1) \
        .values('publisher', 'publisher__name').annotate(score_sum=Sum('score')) \
        .order_by('-score_sum', 'publisher__name')

    this_year = annotate_ranking(this_year)
    last_year = annotate_ranking(last_year)
    last_year_dict = {}
    for publisher in last_year:
        last_year_dict[publisher['publisher__name']] = publisher

    for publisher in this_year:
        try:
            last_year_publisher = last_year_dict[publisher['publisher__name']]
            publisher['delta'] = last_year_publisher['ranking'] - publisher['ranking']
            publisher['delta_abs'] = abs(publisher['delta'])
        except KeyError:
            publisher['delta'] = 0

    return render(request, 'ranking/rank.html',
                  {'publishers': this_year, 'year': year})


class PaperListView(ListView):
    model = Paper

    template_name = 'ranking/paper_list.html'
    context_object_name = 'papers'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query is not None:
            return Paper.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(abstract__contains=query) |
                Q(publisher__name__icontains=query)).order_by('-id')
        else:
            return Paper.objects.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['query'] = self.request.GET.get('query')
        return context