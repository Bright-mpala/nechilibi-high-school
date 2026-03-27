from django.shortcuts import render
from django.utils import timezone
from django_school_management.gallery.models import GalleryCategory, GalleryImage
from django_school_management.events.models import Event
from django_school_management.downloads.models import DownloadCategory, Download
from django_school_management.institute.models import SchoolSettings
from django_school_management.teachers.models import Teacher, LEADERSHIP_ROLES

# Articles app — field names: status, created (TimeStampedModel), featured_image, content, title
try:
    from django_school_management.articles.models import Article
    HAS_ARTICLES = True
except Exception:
    HAS_ARTICLES = False


def home(request):
    settings = SchoolSettings.get()

    # Nechilibi-specific gallery/carousel images
    carousel_images = []
    gallery_images = []
    try:
        from django_school_management.nechilibi.models import GalleryImage as NechilibiGalleryImage
        carousel_images = NechilibiGalleryImage.objects.filter(is_carousel=True, is_active=True).order_by('carousel_order')[:5]
        gallery_images = NechilibiGalleryImage.objects.filter(is_active=True)[:6]
    except Exception:
        pass

    context = {
        'settings': settings,
        'carousel_images': carousel_images,
        'gallery_images': gallery_images,
        'featured_images': GalleryImage.objects.filter(is_featured=True)[:6],
        'upcoming_events': Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now().date()
        ).order_by('start_date')[:4],
        'latest_news': [],
        'recent_articles': [],
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
            articles = Article.objects.filter(
                status='published'
            ).order_by('-created')[:3]
            context['latest_news'] = articles
            context['recent_articles'] = articles
        except Exception:
            pass
    # Leadership teachers for homepage (Headmaster, Deputy, Senior Teacher)
    context['leadership_teachers'] = Teacher.objects.filter(
        is_active=True,
        role__in=LEADERSHIP_ROLES
    ).select_related('designation').prefetch_related('subjects').order_by('designation__role', 'name')
    return render(request, 'public/home.html', context)


def about(request):
    settings = SchoolSettings.get()
    all_teachers = Teacher.objects.filter(is_active=True).select_related("designation").prefetch_related("subjects").order_by("designation__role", "name")
    return render(request, "public/about.html", {"settings": settings, "all_teachers": all_teachers})


def admissions(request):
    return render(request, 'public/admissions.html')


def gallery(request):
    from django_school_management.gallery.models import GalleryImage as GalleryImg
    categories = GalleryCategory.objects.prefetch_related('images').all()
    uncategorised = GalleryImg.objects.filter(category__isnull=True).order_by('order', '-uploaded_at')
    all_images = GalleryImg.objects.all().order_by('order', '-uploaded_at')
    return render(request, 'public/gallery.html', {
        'categories': categories,
        'uncategorised': uncategorised,
        'all_images': all_images,
    })


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
