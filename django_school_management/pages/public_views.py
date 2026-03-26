from django.shortcuts import render
from django.utils import timezone
from django_school_management.gallery.models import GalleryCategory, GalleryImage
from django_school_management.events.models import Event
from django_school_management.downloads.models import DownloadCategory, Download
from django_school_management.institute.models import SchoolSettings

# Articles app — field names: status, created (TimeStampedModel), featured_image, content, title
try:
    from django_school_management.articles.models import Article
    HAS_ARTICLES = True
except Exception:
    HAS_ARTICLES = False


def home(request):
    settings = SchoolSettings.get()
    context = {
        'settings': settings,
        'featured_images': GalleryImage.objects.filter(is_featured=True)[:6],
        'upcoming_events': Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now().date()
        ).order_by('start_date')[:4],
        'latest_news': [],
        'videos': [],
    }
    # add videos
    try:
        from django_school_management.gallery.models import VideoGallery
        context['videos'] = VideoGallery.objects.filter(is_published=True)[:3]
    except Exception:
        pass
    if HAS_ARTICLES:
        try:
            context['latest_news'] = Article.objects.filter(
                status='published'
            ).order_by('-created')[:3]
        except Exception:
            pass
    return render(request, 'public/home.html', context)


def about(request):
    settings = SchoolSettings.get()
    return render(request, 'public/about.html', {'settings': settings})


def admissions(request):
    return render(request, 'public/admissions.html')


def gallery(request):
    categories = GalleryCategory.objects.prefetch_related('images').all()
    return render(request, 'public/gallery.html', {'categories': categories})


def news_list(request):
    articles = []
    if HAS_ARTICLES:
        try:
            articles = Article.objects.filter(
                status='published'
            ).order_by('-created')
        except Exception:
            pass
    return render(request, 'public/news.html', {'articles': articles})


def downloads_page(request):
    categories = DownloadCategory.objects.prefetch_related('downloads').filter(
        downloads__is_published=True
    ).distinct()
    return render(request, 'public/downloads.html', {'categories': categories})


def events_page(request):
    today = timezone.now().date()
    upcoming = Event.objects.filter(
        is_published=True,
        start_date__gte=today
    ).order_by('start_date')
    past = Event.objects.filter(
        is_published=True,
        start_date__lt=today
    ).order_by('-start_date')[:6]
    return render(request, 'public/events.html', {'upcoming': upcoming, 'past': past})


def contact(request):
    settings = SchoolSettings.get()
    return render(request, 'public/contact.html', {'settings': settings})
