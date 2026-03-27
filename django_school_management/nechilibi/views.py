from django.shortcuts import render
from .models import GalleryImage, Testimonial


def home(request):
    carousel_images = GalleryImage.objects.filter(is_carousel=True, is_active=True).order_by('carousel_order')[:5]
    gallery_images = GalleryImage.objects.filter(is_active=True)[:6]
    upcoming_events = []

    # Try to get articles from the articles app
    recent_articles = []
    try:
        from django_school_management.articles.models import Article
        recent_articles = Article.objects.filter(status='published').order_by('-created_at')[:3]
    except Exception:
        pass

    context = {
        'carousel_images': carousel_images,
        'gallery_images': gallery_images,
        'upcoming_events': upcoming_events,
        'recent_articles': recent_articles,
    }
    return render(request, 'public/home.html', context)
