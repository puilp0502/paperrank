from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render

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
    last_year_dict = {}
    for i, publisher in enumerate(last_year):
        publisher['ranking'] = i + 1
        last_year_dict[publisher['publisher__name']] = publisher
    for publisher in this_year:
        try:
            last_year_publisher = last_year_dict[publisher['publisher__name']]
            publisher['delta'] = last_year_publisher['ranking'] - publisher['ranking']
        except KeyError:
            publisher['delta'] = 0

    print(this_year)
    print(last_year)

    return render(request, 'ranking/rank.html', {'publishers': this_year})
