from django.db.models import Sum, Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Paper


def annotate_ranking(queryset):
    for i, publisher in enumerate(queryset):
        publisher['ranking'] = i + 1
    return queryset


def main_page(request):
    recent_paper = Paper.objects.order_by('-registered', '-pk')[:10]
    return render(request, 'ranking/main.html',
                  {'recent_paper': recent_paper})


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
    paginate_by = 10

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


class PaperDetailView(DetailView):
    model = Paper
    template_name = 'ranking/paper_detail.html'
    context_object_name = 'paper'

    def __init__(self):
        super().__init__()
        self.redirect = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        url_slug = self.kwargs.get(self.slug_url_kwarg)
        obj_slug = getattr(obj, self.get_slug_field())
        if url_slug != obj_slug:
            self.redirect = reverse('ranking:paper',
                                    kwargs={'pk': obj.pk, 'slug': obj_slug})
        return obj

    def render_to_response(self, context, **response_kwargs):
        if self.redirect:
            return redirect(self.redirect)
        return super().render_to_response(context, **response_kwargs)
