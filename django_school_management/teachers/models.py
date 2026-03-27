from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from utilities.compat import ExportModelOperationsMixin
from taggit.managers import TaggableManager


class Designation(ExportModelOperationsMixin('designation'), TimeStampedModel):
    ROLE_HEADMASTER = 'headmaster'
    ROLE_DEPUTY = 'deputy'
    ROLE_SENIOR = 'senior_teacher'
    ROLE_TEACHER = 'teacher'
    ROLE_OTHER = 'other'

    ROLE_CHOICES = [
        (ROLE_HEADMASTER, 'Headmaster'),
        (ROLE_DEPUTY, 'Deputy Headmaster'),
        (ROLE_SENIOR, 'Senior Teacher'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_OTHER, 'Other'),
    ]

    title = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TEACHER,
        help_text='Controls display prominence on the website.',
    )
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['role', 'title']

    def __str__(self):
        return str(self.title)

    @property
    def is_leadership(self):
        return self.role in (self.ROLE_HEADMASTER, self.ROLE_DEPUTY, self.ROLE_SENIOR)


ROLE_HEADMASTER = 'headmaster'
ROLE_DEPUTY = 'deputy'
ROLE_SENIOR = 'senior_teacher'
ROLE_TEACHER = 'teacher'

ROLE_CHOICES = [
    (ROLE_HEADMASTER, 'Headmaster'),
    (ROLE_DEPUTY, 'Deputy Headmaster'),
    (ROLE_SENIOR, 'Senior Teacher'),
    (ROLE_TEACHER, 'Ordinary Teacher'),
]

LEADERSHIP_ROLES = {ROLE_HEADMASTER, ROLE_DEPUTY, ROLE_SENIOR}


class Teacher(ExportModelOperationsMixin('teacher'), TimeStampedModel):
    employee_id = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='teachers', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TEACHER,
        verbose_name='Position',
        help_text='Select the teacher\'s position at the school.',
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.CASCADE,
        related_name='resources',
        help_text='Job title/department label (e.g. "Head of Science")',
    )
    subjects = models.ManyToManyField(
        'academics.Subject',
        blank=True,
        related_name='assigned_teachers',
        help_text='Subjects this teacher teaches.',
    )
    bio = models.TextField(
        blank=True, null=True,
        help_text='Short biography shown on the website.',
    )
    expertise = TaggableManager(blank=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    # Social media
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(
        max_length=20, blank=True, null=True,
        help_text='WhatsApp number with country code e.g. +2637...',
    )
    joining_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to hide this teacher from the website.',
    )
    institute = models.ForeignKey(
        'institute.InstituteProfile',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='teachers',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['role', 'name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.get_role_display())

    @property
    def is_leadership(self):
        return self.role in LEADERSHIP_ROLES

    @property
    def subject_list(self):
        return ', '.join(self.subjects.values_list('name', flat=True))
