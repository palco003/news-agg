from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import FeedForm
from .models import Article, Feed
import feedparser
import datetime

# Create your views here.


def articles_list(request):
    articles = Article.objects.all()
    return render(request, 'news/articles_list.html', {'articles': articles})


def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})


def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)

            feedData = feedparser.parse(feed.url)

            # set some fields
            feed.title = feedData.feed.title
            feed.save()

            for entry in feedData.entries:
                article = Article()
                article.title = entry.title
                article.url = entry.link
                article.description = entry.description
                # publication_date
                d = datetime.datetime(*(entry.published_parsed[:6]))
                date_string = d.strftime('%Y-%m-%d %H:%M:%S')

                article.publication_date = date_string
                article.feed = feed
                article.save()

            return redirect(reverse('feeds_list'))
    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})
