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


class ZIMSECResult(models.Model):
    LEVEL_CHOICES = [
        ('o_level', 'O-Level'),
        ('a_level', 'A-Level'),
    ]
    year             = models.CharField(max_length=4, help_text='e.g. 2025')
    level            = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    total_candidates = models.PositiveIntegerField(default=0)
    total_passes     = models.PositiveIntegerField(default=0)
    distinctions     = models.PositiveIntegerField(default=0, help_text='Number of A/A* grades')
    national_average = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                           help_text='National pass rate % for comparison')
    notes            = models.TextField(blank=True)
    is_published     = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', 'level']
        unique_together = ['year', 'level']
        verbose_name = 'ZIMSEC Result'
        verbose_name_plural = 'ZIMSEC Results'

    def __str__(self):
        return f'{self.year} {self.get_level_display()}'

    @property
    def pass_rate(self):
        if self.total_candidates:
            return round((self.total_passes / self.total_candidates) * 100, 1)
        return 0

    @property
    def distinction_rate(self):
        if self.total_candidates:
            return round((self.distinctions / self.total_candidates) * 100, 1)
        return 0

    @property
    def above_national(self):
        if self.national_average:
            return self.pass_rate > float(self.national_average)
        return None


class SubjectResult(models.Model):
    exam          = models.ForeignKey(ZIMSECResult, on_delete=models.CASCADE, related_name='subjects')
    subject       = models.CharField(max_length=100)
    candidates    = models.PositiveIntegerField(default=0)
    passes        = models.PositiveIntegerField(default=0)
    distinctions  = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['subject']
        verbose_name = 'Subject Result'
        verbose_name_plural = 'Subject Results'

    def __str__(self):
        return f'{self.exam} — {self.subject}'

    @property
    def pass_rate(self):
        if self.candidates:
            return round((self.passes / self.candidates) * 100, 1)
        return 0
