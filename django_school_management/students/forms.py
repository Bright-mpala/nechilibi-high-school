import re
from datetime import date

from django import forms
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)

from django_school_management.institute.models import EducationBoard
from django_school_management.institute.education_boards import (
    APPLYING_FOR_FORM_MIN,
    APPLYING_FOR_FORM_MAX,
)
from .models import AdmissionStudent, CounselingComment, Student

MAX_UPLOAD_SIZE_MB = 5


class StudentForm(forms.ModelForm):
    """Admission form for Zimbabwe high school students (Form 1–6)."""

    class Meta:
        model = AdmissionStudent
        fields = [
            'name',
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'gender',
            'city',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'tribal_status',
            'department_choice',
            'applying_for_class',
            'board',
            'ssc_roll',
            'ssc_registration',
            'gpa',
            'exam_name',
            'passing_year',
            'group',
            'photo',
            'marksheet_image',
            'admission_policy_agreement',
            'admit_to_semester',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
            'gpa': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop('institute', None)
        super().__init__(*args, **kwargs)

        if 'gender' in self.fields:
            self.fields['gender'].required = True

        # Show Form 1-6 selection, remove polytechnic-only field
        self.fields.pop('admit_to_semester', None)
        if 'applying_for_class' in self.fields:
            self.fields['applying_for_class'].required = False
            self.fields['applying_for_class'].label = 'Applying for Form'
            self.fields['applying_for_class'].widget = forms.Select(
                choices=[('', '---------')] + [
                    (i, 'Form %s' % i) for i in range(APPLYING_FOR_FORM_MIN, APPLYING_FOR_FORM_MAX + 1)
                ]
            )

        if self.institute:
            self.fields['department_choice'].queryset = (
                self.fields['department_choice'].queryset.filter(institute=self.institute)
            )
            self.fields['department_choice'].label = (
                self.institute.department_label or 'Department'
            )
            # Academic fields optional for school
            for f in ('exam_name', 'passing_year', 'group', 'board',
                      'ssc_roll', 'ssc_registration', 'gpa', 'marksheet_image'):
                if f in self.fields:
                    self.fields[f].required = False

            # Show ZIMSEC/CIE boards if available
            boards_qs = EducationBoard.get_boards_for_country(self.institute.country)
            if boards_qs.exists() and 'board' in self.fields:
                self.fields['board'].widget = forms.Select(
                    choices=[('', '---------')] + [(b.name, b.name) for b in boards_qs]
                )
                self.fields['board'].label = 'Examination Council'

            # Rename SSC labels to Zimbabwe equivalents
            if 'ssc_roll' in self.fields:
                self.fields['ssc_roll'].label = 'ZIMSEC Roll No.'
            if 'ssc_registration' in self.fields:
                self.fields['ssc_registration'].label = 'ZIMSEC Registration No.'
            if 'gpa' in self.fields:
                self.fields['gpa'].label = 'Previous Result (%)'

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 100):
            raise forms.ValidationError("Result must be between 0 and 100.")
        return gpa

    def clean_mobile_number(self):
        value = self.cleaned_data.get('mobile_number', '')
        if value and not re.match(r'^\+?[\d\s\-]{7,15}$', value):
            raise forms.ValidationError("Enter a valid phone number.")
        return value

    def clean_guardian_mobile_number(self):
        value = self.cleaned_data.get('guardian_mobile_number', '')
        if value and not re.match(r'^\+?[\d\s\-]{7,15}$', value):
            raise forms.ValidationError("Enter a valid phone number.")
        return value

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob >= date.today():
            raise forms.ValidationError("Date of birth must be in the past.")
        return dob

    def _check_file_size(self, field_name):
        f = self.cleaned_data.get(field_name)
        if f and hasattr(f, 'size') and f.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"File must be under {MAX_UPLOAD_SIZE_MB} MB.")
        return f

    def clean_photo(self):
        return self._check_file_size('photo')

    def clean_marksheet_image(self):
        return self._check_file_size('marksheet_image')

    def clean_applying_for_class(self):
        val = self.cleaned_data.get('applying_for_class')
        if val is not None and val != '':
            try:
                n = int(val)
                if APPLYING_FOR_FORM_MIN <= n <= APPLYING_FOR_FORM_MAX:
                    return n
            except (TypeError, ValueError):
                pass
        return None


class AdmissionForm(forms.ModelForm):
    """Admit form: set chosen department."""

    class Meta:
        model = AdmissionStudent
        fields = ['choosen_department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.department_choice_id:
            institute = getattr(self.instance.department_choice, 'institute', None)
            if institute:
                self.fields['choosen_department'].queryset = (
                    self.fields['choosen_department'].queryset.filter(institute=institute)
                )


class StudentRegistrantUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'name',
            'photo',
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'gender',
            'current_address',
            'permanent_address',
            'mobile_number',
            'email',
            'choosen_department',
            'admitted',
            'paid',
            'rejected',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        show_choosen_department = kwargs.pop('show_choosen_department', True)
        super().__init__(*args, **kwargs)
        if not show_choosen_department and 'choosen_department' in self.fields:
            self.fields.pop('choosen_department')


class CounselingDataForm(forms.ModelForm):
    class Meta:
        model = CounselingComment
        fields = ['comment']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'roll',
            'registration_number',
            'semester',
            'guardian_mobile',
            'is_alumni', 'is_dropped'
        )
