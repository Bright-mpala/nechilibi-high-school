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


class TermDate(models.Model):
    TERM_CHOICES = [(1, 'Term 1'), (2, 'Term 2'), (3, 'Term 3')]

    academic_year = models.CharField(max_length=9, help_text='e.g. 2026')
    term = models.IntegerField(choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False, help_text='Mark the running term')
    notes = models.TextField(blank=True, help_text='Optional note e.g. "Includes Prize Giving Day"')

    class Meta:
        ordering = ['academic_year', 'term']
        unique_together = ['academic_year', 'term']
        verbose_name = 'Term Date'
        verbose_name_plural = 'Term Dates'

    def __str__(self):
        return f'{self.academic_year} – Term {self.term}'

    @property
    def duration_weeks(self):
        return round((self.end_date - self.start_date).days / 7)


class CalendarEvent(models.Model):
    TYPE_CHOICES = [
        ('holiday', 'School Holiday'),
        ('exam',    'Examinations'),
        ('event',   'School Event'),
        ('other',   'Other'),
    ]
    title        = models.CharField(max_length=200)
    event_type   = models.CharField(max_length=20, choices=TYPE_CHOICES, default='event')
    date_from    = models.DateField()
    date_to      = models.DateField(blank=True, null=True, help_text='Leave blank for single-day entry')
    academic_year = models.CharField(max_length=9, help_text='e.g. 2026')
    notes        = models.TextField(blank=True)

    class Meta:
        ordering = ['date_from']
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    def __str__(self):
        return f'{self.title} ({self.date_from})'

    @property
    def is_multiday(self):
        return bool(self.date_to and self.date_to != self.date_from)
