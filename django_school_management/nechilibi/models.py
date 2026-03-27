from django.db import models


class SchoolSettings(models.Model):
    school_name = models.CharField(max_length=200, default='Nechilibi High School')
    tagline = models.CharField(max_length=300, blank=True, default='Excellence in Education')
    address = models.TextField(blank=True, default='Nechilibi, Matabeleland South, Zimbabwe')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, default='info@nechilibi.ac.zw')
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='school/', blank=True, null=True)
    hero_text = models.CharField(max_length=500, blank=True, default='Welcome to Nechilibi High School')
    hero_subtext = models.TextField(blank=True, default='Providing quality education in Zimbabwe since our founding.')

    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'

    def __str__(self):
        return self.school_name


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('sports', 'Sports'),
        ('academics', 'Academics'),
        ('events', 'Events'),
        ('facilities', 'Facilities'),
    ]
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    description = models.TextField(blank=True)
    is_carousel = models.BooleanField(default=False, help_text='Show on homepage carousel')
    carousel_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['carousel_order', '-uploaded_at']

    def __str__(self):
        return self.title


class SchoolVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(blank=True, help_text='YouTube embed URL')
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbs/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SchoolEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title


class Download(models.Model):
    CATEGORY_CHOICES = [
        ('forms', 'Application Forms'),
        ('timetable', 'Timetables'),
        ('results', 'Results'),
        ('handbook', 'Student Handbook'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='downloads/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Student')
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
