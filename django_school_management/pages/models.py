from django.db import models
from django.conf import settings


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photos.count()


class GalleryPhoto(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.album.title} — {self.caption or self.pk}"


class VideoGallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_url = models.URLField(help_text='YouTube video URL (e.g. https://www.youtube.com/watch?v=...)')
    thumbnail = models.ImageField(upload_to='gallery/video_thumbs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Convert watch URL to embed URL."""
        url = self.youtube_url
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Download(models.Model):
    CATEGORY_CHOICES = [
        ('forms', 'Application Forms'),
        ('timetable', 'Timetables'),
        ('results', 'Results'),
        ('policies', 'Policies'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    file = models.FileField(upload_to='downloads/')
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('linkedin', 'LinkedIn'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_platform_display()

    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'


class HeroBanner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='hero/')
    cta_text = models.CharField('Button text', max_length=100, blank=True)
    cta_url = models.CharField('Button URL', max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Banner Slide'
        verbose_name_plural = 'Hero Banner Slides'

    def __str__(self):
        return self.title


class SchoolHighlight(models.Model):
    icon_class = models.CharField(
        max_length=100, default='fas fa-star',
        help_text='FontAwesome icon class, e.g. fas fa-graduation-cap'
    )
    value = models.CharField(max_length=50, help_text='e.g. 1200 or 98%')
    label = models.CharField(max_length=100, help_text='e.g. Students Enrolled')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'School Highlight / Stat'
        verbose_name_plural = 'School Highlights / Stats'

    def __str__(self):
        return f"{self.value} {self.label}"
