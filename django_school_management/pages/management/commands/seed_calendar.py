"""
Seeds 2026 academic calendar data (term dates + key events).
Run:  python manage.py seed_calendar
Safe to re-run — uses get_or_create throughout.
"""
from datetime import date
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import TermDate, CalendarEvent


YEAR = '2026'

TERMS = [
    # term, start, end, is_current, notes
    (1, date(2026, 1, 20), date(2026, 4,  3), False, 'Includes AGM for parents (last Saturday of Term 1)'),
    (2, date(2026, 5,  5), date(2026, 8,  7), True,  'Mid-year exams in June/July'),
    (3, date(2026, 9,  8), date(2026, 12, 4), False, 'ZIMSEC O-Level & A-Level November exams. Prize Giving Day — end of term.'),
]

EVENTS = [
    # title, event_type, date_from, date_to, notes
    # Examinations
    ('Mid-Year Internal Exams (O-Level)',  'exam', date(2026, 6, 22), date(2026, 7, 3),  'Forms 3 & 4'),
    ('Mid-Year Internal Exams (A-Level)',  'exam', date(2026, 6, 22), date(2026, 7, 3),  'Forms 5 & 6'),
    ('ZIMSEC O-Level November Session',   'exam', date(2026, 11, 2), date(2026, 11, 27), 'National ZIMSEC examinations — Form 4'),
    ('ZIMSEC A-Level November Session',   'exam', date(2026, 11, 2), date(2026, 11, 27), 'National ZIMSEC examinations — Form 6'),
    ('End-of-Year Internal Exams',        'exam', date(2026, 11, 9), date(2026, 11, 20), 'Forms 1, 2, 3 & 5'),

    # School holidays
    ('Good Friday',                 'holiday', date(2026, 4, 3),  None,              'Public holiday'),
    ('Easter Monday',               'holiday', date(2026, 4, 6),  None,              'Public holiday'),
    ('Independence Day',            'holiday', date(2026, 4, 18), None,              'Zimbabwe Independence — school closed'),
    ("Workers' Day",                'holiday', date(2026, 5, 1),  None,              'Public holiday'),
    ('Africa Day',                  'holiday', date(2026, 5, 25), None,              'Public holiday'),
    ("Heroes' Day",                 'holiday', date(2026, 8, 10), None,              'Public holiday'),
    ('Defence Forces Day',          'holiday', date(2026, 8, 11), None,              'Public holiday'),
    ('Unity Day',                   'holiday', date(2026, 12, 22), None,             'Public holiday'),
    ('Christmas Day',               'holiday', date(2026, 12, 25), None,             'Public holiday'),
    ('Boxing Day',                  'holiday', date(2026, 12, 26), None,             'Public holiday'),

    # Key school events
    ('Annual General Meeting (AGM)', 'event', date(2026, 3, 28), None,              'Parents and guardians are invited — venue: school hall'),
    ('Sports Day',                   'event', date(2026, 3, 7),  None,              'Inter-house athletics competition'),
    ('Prize Giving Day',             'event', date(2026, 11, 28), None,             'Annual academic prize giving ceremony'),
    ('Career Guidance Day',          'event', date(2026, 8, 1),  None,              'Form 4 & 6 students — invited speakers from various professions'),
    ('School Cultural Day',          'event', date(2026, 6, 5),  None,              'Music, drama and art showcase'),
    ('Parents & Teachers Meeting',   'event', date(2026, 7, 18), None,              'Term 2 academic progress — all forms'),
    ('Form 1 Orientation Day',       'event', date(2026, 1, 19), None,              'New Form 1 students and parents'),
]


class Command(BaseCommand):
    help = 'Seed 2026 academic calendar — term dates and key events'

    def handle(self, *args, **options):
        created_terms = 0
        for term_num, start, end, current, notes in TERMS:
            _, created = TermDate.objects.update_or_create(
                academic_year=YEAR,
                term=term_num,
                defaults={
                    'start_date': start,
                    'end_date': end,
                    'is_current': current,
                    'notes': notes,
                }
            )
            if created:
                created_terms += 1

        created_events = 0
        for title, etype, dfrom, dto, notes in EVENTS:
            _, created = CalendarEvent.objects.update_or_create(
                academic_year=YEAR,
                title=title,
                defaults={
                    'event_type': etype,
                    'date_from': dfrom,
                    'date_to': dto,
                    'notes': notes,
                }
            )
            if created:
                created_events += 1

        self.stdout.write(self.style.SUCCESS(
            f'Calendar seeded: {created_terms} new terms, {created_events} new events for {YEAR}.'
        ))
