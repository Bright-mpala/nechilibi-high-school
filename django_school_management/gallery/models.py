from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Gallery Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, related_name='images', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']

    def __str__(self):
        return self.title


class VideoGallery(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text='YouTube video URL (e.g. https://www.youtube.com/watch?v=XXXX)')
    thumbnail = models.ImageField(upload_to='videos/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        import re
        patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'youtu\.be/([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return f'https://www.youtube.com/embed/{match.group(1)}'
        return self.youtube_url
