from django import forms

from django_school_management.institute.models import (
    InstituteProfile,
    INSTITUTE_TYPE_CHOICES,
)
from django_school_management.academics.models import Department, AcademicSession


FC = {'class': 'form-control'}


class OnboardingStep1Form(forms.ModelForm):
    """Institute profile basics."""

    class Meta:
        model = InstituteProfile
        fields = [
            'name', 'country', 'logo', 'motto', 'description',
            'date_of_estashment', 'institute_type',
        ]
        widgets = {
            'name': forms.TextInput(attrs={**FC, 'placeholder': 'School name'}),
            'date_of_estashment': forms.DateInput(attrs={**FC, 'type': 'date'}),
            'motto': forms.Textarea(attrs={**FC, 'rows': 2, 'placeholder': 'School motto'}),
            'description': forms.Textarea(attrs={**FC, 'rows': 3, 'placeholder': 'Brief description'}),
            'institute_type': forms.Select(attrs={**FC}),
        }
        labels = {
            'date_of_estashment': 'Date of Establishment',
            'institute_type': 'Type of institution',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institute_type'].choices = [('', '---------')] + list(INSTITUTE_TYPE_CHOICES)
        if 'country' in self.fields:
            self.fields['country'].widget.attrs.update(FC)


class OnboardingDepartmentForm(forms.Form):
    """Plain form for adding new departments during onboarding."""

    name = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={**FC, 'placeholder': 'e.g. Sciences'}),
    )
    short_name = forms.CharField(
        max_length=5, required=False,
        widget=forms.TextInput(attrs={**FC, 'placeholder': 'e.g. SCI'}),
    )
    code = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={**FC, 'placeholder': 'e.g. 101'}),
    )


OnboardingDepartmentFormSet = forms.formset_factory(
    OnboardingDepartmentForm,
    extra=1,
    max_num=20,
)


class OnboardingAcademicSessionForm(forms.ModelForm):
    """Academic session for onboarding."""

    class Meta:
        model = AcademicSession
        fields = ['year']
        widgets = {
            'year': forms.NumberInput(attrs={**FC, 'placeholder': 'e.g. 2026'}),
        }
