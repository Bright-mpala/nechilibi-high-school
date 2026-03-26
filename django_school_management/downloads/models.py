from django.db import models

class DownloadCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Download Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Download(models.Model):
    category = models.ForeignKey(DownloadCategory, on_delete=models.CASCADE, related_name='downloads')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='downloads/')
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
