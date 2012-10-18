from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article
from .forms import SearchForm
#import forms   # forms.Search

#from django.views.generic.dates
from django.views.generic import dates



####################
## NewsStory views
####################

from .models import Story
from markdown import markdown

# or store on view func?
#_markdown = markdown.Markdown()
#_markdown.convert(text1)
#_markdown.reset().convert(text1)


def story_list (request):
    data = Story.objects.all().filter(published=True).order_by('date')
    for item in data:
        item.text = markdown (item.text, safe_mode='escape')
    return render (request, 'news/story_list.html', { 'list': data })


def story_detail (request, story_id):
    #data = get_object_or_404 (Story, pk=story_id, published=True)
    item = get_object_or_404 (Story, pk=story_id)
    item.text = markdown (item.text, safe_mode='escape')
    return render (request, 'news/story_detail.html', {
        'object': item,
#        'object': get_object_or_404 (Story, pk=story_id, published=True)
    })




####################
## NewsLink views

class ArchiveView (dates.ArchiveIndexView):
    model = Article
    date_field = 'date'
    paginate_by = 25
    #context_object_name = 'list'    # object_list
    #date_list_period = 'year'
    #allow_future = False
    # get_dated_queryset(**lookup)
    # get_date_list(queryset, date_type=None, ordering='ASC')
    # @todo get from cache (same query as sub-menu does. cache queryset?)
#    def get_date_list(queryset, date_type=None, ordering='ASC'):
#        return [datetime(2002,1,1), datetime(2004,1,1), datetime(2006,1,1)]
archive = ArchiveView.as_view()

# ArchiveYearView
# @todo show months in revered order?
class YearView (dates.YearArchiveView):
    model = Article
    date_field = 'date'
    make_object_list = True     # False => only generate month list
archive_year = YearView.as_view()

# ArchiveMonthView
class MonthView (dates.MonthArchiveView):
    model = Article
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
archive_month = MonthView.as_view()



# @note can use ArchiveIndexView as base for this view
def list (request):
    # Search
    query = request.GET.get ('query')
    if query:
        form = SearchForm (request.GET)
        qs = Article.objects.filter(
                Q(title__icontains=query)   |
                Q(summary__icontains=query) |
                Q(body__icontains=query)
        )
    else:
        form = SearchForm()
        qs = Article.objects.all()

    qs = qs.order_by('-date')

    # Pagination
    pagesize = 25
    paginator = Paginator (qs, pagesize)
    try:
        articles = paginator.page (request.GET.get('page'))
    except:
        articles = paginator.page (1)
    # @todo helper?
    # @todo hi+low, and put on paginator instance
    low = (articles.number-1) * pagesize + 1
    high = low + pagesize
    count = paginator.count
    if high > count: high = count

    return render (request, 'news/list.html', {
        'list': articles, 'low': low, 'high': high,
        'form': form, 'query': query,
        # if query: search = '&search=%s' % urlencode(query)
        # better to pass in session?
    })



def detail (request, news_id):
    return render (request, 'news/detail.html', {
        'item': get_object_or_404 (Article, pk=news_id)
        # @todo same name as DetailView uses. (object?)
    })
