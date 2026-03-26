from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel
from utilities.compat import ExportModelOperationsMixin

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import model_help_texts


# Nechilibi High School — Zimbabwe secondary school only
INSTITUTE_TYPE_SCHOOL = 'school'

INSTITUTE_TYPE_CHOICES = [
    (INSTITUTE_TYPE_SCHOOL, 'High School'),
]

INSTITUTE_TYPE_ONBOARDING_ORDER = [
    INSTITUTE_TYPE_SCHOOL,
]


class EducationBoard(ExportModelOperationsMixin('education_board'), models.Model):
	"""Examination councils (e.g. ZIMSEC for Zimbabwe)."""
	country = CountryField(db_index=True)
	name = models.CharField(max_length=120)
	code = models.CharField(max_length=30, blank=True, help_text='Short code for display')

	class Meta:
		ordering = ['country', 'name']
		unique_together = [('country', 'name')]

	def __str__(self):
		return self.name

	@classmethod
	def get_boards_for_country(cls, country_code):
		"""Return examination boards/councils for a country."""
		if country_code is None:
			return cls.objects.none()
		code = getattr(country_code, 'code', country_code) or str(country_code) if country_code else None
		if not code:
			return cls.objects.none()
		return cls.objects.filter(country=code)


class InstituteProfile(ExportModelOperationsMixin('institute_profile'), models.Model):
	name = models.CharField(max_length=255)
	date_of_estashment = models.DateField(blank=True, null=True)
	country = CountryField(blank=True, null=True)
	logo = models.ImageField(upload_to='institute/')
	logo_small = models.ImageField(upload_to='institute/', blank=True, null=True)
	site_favicon = models.ImageField(upload_to='institute', blank=True, null=True)
	site_header = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SITEHEADER,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SITEHEADER_DEFAULT
	)
	site_title = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SITETITLE,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SITETITLE_DEFAULT
	)
	super_admin_index_title = models.CharField(
		help_text=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE,
		max_length=100,
		default=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE_DEFAULT
	)
	motto = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	active = models.BooleanField(default=False, unique=True)
	onboarding_completed = models.BooleanField(default=False)
	institute_type = models.CharField(
		max_length=20,
		choices=INSTITUTE_TYPE_CHOICES,
		default=INSTITUTE_TYPE_SCHOOL,
		blank=True,
		null=True,
	)
	current_session = models.ForeignKey(
		'academics.AcademicSession',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='institutes_using_as_current',
		help_text='Current active academic session.',
	)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True
	)

	def __str__(self):
		return self.name

	@property
	def onboarding_step(self):
		if self.onboarding_completed:
			return None
		from django_school_management.academics.models import Department
		if not Department.objects.filter(institute=self).exists():
			return 2
		return 3

	def get_absolute_url(self):
		return reverse('institute:institute_detail', args=[self.pk])

	@property
	def is_polytechnic(self):
		return False

	@property
	def is_school_or_madrasah(self):
		return True

	@property
	def department_label_plural(self):
		return 'Departments'

	@property
	def department_label(self):
		return 'Department'

	@property
	def semester_label(self):
		return 'Form'

	@property
	def semester_label_plural(self):
		return 'Forms'


class SchoolSettings(models.Model):
    """Singleton model for school-wide settings editable from admin."""
    school_name = models.CharField(max_length=200, default='Nechilibi High School')
    tagline = models.CharField(max_length=300, blank=True, default='Excellence in Education')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, default='info@nechilibi.ac.zw')
    address = models.TextField(blank=True, default='P.O. Box 123, Nechilibi, Matabeleland South, Zimbabwe')
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    hero_heading = models.CharField(max_length=200, blank=True, default="Shaping Tomorrow's Leaders Today")
    hero_subheading = models.TextField(blank=True, default='Nechilibi High School provides quality secondary education from Form 1 to Form 6.')
    about_text = models.TextField(blank=True)
    total_students = models.PositiveIntegerField(default=500)
    total_teachers = models.PositiveIntegerField(default=40)
    logo = models.ImageField(upload_to='school/', blank=True, null=True)
    hero_background = models.ImageField(upload_to='school/', blank=True, null=True)

    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        # Singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class City(ExportModelOperationsMixin('city'), TimeStampedModel):
	name = models.CharField(max_length=150)
	country = CountryField()
	code = models.CharField(
		max_length=10,
		help_text='Province/district code',
	)

	class Meta:
		verbose_name_plural = 'cities'
		ordering = ['name']
		unique_together = ['country', 'code']

	def __str__(self):
		return self.name


class BaseWidget(TimeStampedModel):
	WIDGET_TYPE_CHOICES = (
		('text', 'Text Content'),
		('list', 'List Items'),
	)
	widget_type = models.CharField(
		max_length=10,
		choices=WIDGET_TYPE_CHOICES,
		default=WIDGET_TYPE_CHOICES[0][0]
	)
	widget_title = models.CharField(max_length=50)
	widget_number = models.PositiveSmallIntegerField(unique=True)

	class Meta:
		abstract = True


class TextWidget(ExportModelOperationsMixin('text_widget'), BaseWidget):
	content = RichTextUploadingField(config_name='default')

	def __str__(self):
		return self.widget_title


class ListWidget(ExportModelOperationsMixin('list_widget'), BaseWidget):
	pass

	def __str__(self):
		return self.widget_title


class WidgetListItem(ExportModelOperationsMixin('widget_list_item'), TimeStampedModel):
	widget = models.ForeignKey(
		ListWidget,
		on_delete=models.CASCADE
	)
	text = models.CharField(max_length=150)
	link = models.URLField(
		max_length=255,
		blank=True, null=True
	)

	def __str__(self):
		return self.text

	def __html__(self):
		return mark_safe(
			'<a href="{0}">{1}</>'.format(self.link, self.text)
		)
