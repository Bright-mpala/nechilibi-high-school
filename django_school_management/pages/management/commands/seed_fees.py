"""
Seed realistic 2026 USD fee data for Nechilibi High School.
Safe to run multiple times — skips if the year already exists.
"""
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import FeeStructure, FeeItem


FEE_DATA = {
    'academic_year': '2026',
    'currency': 'USD',
    'effective_from': '2026-01-20',
    'notes': (
        'All fees are payable in USD or ZiG equivalent at the prevailing RBZ rate on the date of payment. '
        'ZIMSEC examination fees are collected in Term 2 only and are subject to change by ZIMSEC. '
        'Boarding fees cover accommodation, meals, and basic toiletries. '
        'For payment plans contact the school bursar.'
    ),
    'items': [
        # ── Form 1 & 2 ──────────────────────────────────────────
        dict(form_group='form1_2', category='tuition',     description='Tuition Fee',               amount='120.00', frequency='per_term', order=1),
        dict(form_group='form1_2', category='boarding',    description='Boarding Fee',               amount='180.00', frequency='per_term', order=2),
        dict(form_group='form1_2', category='development', description='Development Levy',            amount='30.00',  frequency='per_term', order=3),
        dict(form_group='form1_2', category='sports',      description='Sports & Activities Levy',   amount='15.00',  frequency='per_term', order=4),
        dict(form_group='form1_2', category='library',     description='Library & Resources Levy',   amount='10.00',  frequency='per_term', order=5),
        dict(form_group='form1_2', category='other',       description='School Diary & Stationery',  amount='8.00',   frequency='once_off', order=6, notes='New intake only'),

        # ── Form 3 & 4 ──────────────────────────────────────────
        dict(form_group='form3_4', category='tuition',     description='Tuition Fee',               amount='130.00', frequency='per_term', order=1),
        dict(form_group='form3_4', category='boarding',    description='Boarding Fee',               amount='180.00', frequency='per_term', order=2),
        dict(form_group='form3_4', category='development', description='Development Levy',            amount='30.00',  frequency='per_term', order=3),
        dict(form_group='form3_4', category='sports',      description='Sports & Activities Levy',   amount='15.00',  frequency='per_term', order=4),
        dict(form_group='form3_4', category='library',     description='Library & Resources Levy',   amount='10.00',  frequency='per_term', order=5),
        dict(form_group='form3_4', category='zimsec',      description='ZIMSEC Exam Registration',   amount='45.00',  frequency='once_off', order=6, notes='Form 4 only — Term 2 collection'),

        # ── Form 5 & 6 (A-Level) ────────────────────────────────
        dict(form_group='form5_6', category='tuition',     description='Tuition Fee',               amount='150.00', frequency='per_term', order=1),
        dict(form_group='form5_6', category='boarding',    description='Boarding Fee',               amount='180.00', frequency='per_term', order=2),
        dict(form_group='form5_6', category='development', description='Development Levy',            amount='30.00',  frequency='per_term', order=3),
        dict(form_group='form5_6', category='sports',      description='Sports & Activities Levy',   amount='15.00',  frequency='per_term', order=4),
        dict(form_group='form5_6', category='library',     description='Library & Resources Levy',   amount='12.00',  frequency='per_term', order=5),
        dict(form_group='form5_6', category='zimsec',      description='ZIMSEC A-Level Registration', amount='55.00', frequency='once_off', order=6, notes='Form 6 only — Term 2 collection'),

        # ── All Forms ────────────────────────────────────────────
        dict(form_group='all',     category='other',       description='Computer Lab Levy',          amount='10.00',  frequency='per_term', order=1),
        dict(form_group='all',     category='other',       description='School Identity Card',       amount='5.00',   frequency='once_off', order=2, notes='Replacement: $3'),
    ],
}


class Command(BaseCommand):
    help = 'Seed 2026 fee structure for Nechilibi High School'

    def handle(self, *args, **options):
        year = FEE_DATA['academic_year']

        if FeeStructure.objects.filter(academic_year=year).exists():
            self.stdout.write(self.style.WARNING(f'Fee structure for {year} already exists — skipping.'))
            return

        structure = FeeStructure.objects.create(
            academic_year=year,
            currency=FEE_DATA['currency'],
            effective_from=FEE_DATA['effective_from'],
            is_published=True,
            notes=FEE_DATA['notes'],
        )

        for item_data in FEE_DATA['items']:
            FeeItem.objects.create(
                structure=structure,
                form_group=item_data['form_group'],
                category=item_data['category'],
                description=item_data['description'],
                amount=item_data['amount'],
                frequency=item_data['frequency'],
                order=item_data.get('order', 0),
                notes=item_data.get('notes', ''),
            )

        self.stdout.write(self.style.SUCCESS(
            f'Created {year} fee structure with {len(FEE_DATA["items"])} items.'
        ))
