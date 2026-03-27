"""
Seeds sample ZIMSEC results for Nechilibi High School.
Run:  python manage.py seed_results
Safe to re-run — uses update_or_create throughout.
"""
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import ZIMSECResult, SubjectResult

DATA = {
    # year: { level: { overall, subjects } }
    '2023': {
        'o_level': {
            'candidates': 87, 'passes': 75, 'distinctions': 18, 'national_average': 62.4,
            'notes': 'Best O-Level performance in the school\'s history at that time.',
            'subjects': [
                ('English Language',       87, 80, 12),
                ('Mathematics',            87, 71, 14),
                ('Combined Science',       87, 74, 10),
                ('History',                60, 55,  8),
                ('Geography',              72, 65,  9),
                ('Shona / Ndebele',        87, 82, 15),
                ('Commerce',               45, 39,  5),
                ('Accounts',               40, 32,  4),
                ('Agriculture',            55, 50,  7),
                ('Physical Education',     30, 29,  6),
            ],
        },
        'a_level': {
            'candidates': 34, 'passes': 29, 'distinctions': 8, 'national_average': 54.1,
            'notes': '',
            'subjects': [
                ('Mathematics',            20, 17, 5),
                ('Physics',                18, 15, 4),
                ('Chemistry',              16, 13, 3),
                ('Biology',                14, 12, 2),
                ('History',                10,  9, 1),
                ('Geography',              12, 10, 2),
                ('Accounts',               14, 11, 1),
            ],
        },
    },
    '2024': {
        'o_level': {
            'candidates': 92, 'passes': 83, 'distinctions': 22, 'national_average': 63.8,
            'notes': '',
            'subjects': [
                ('English Language',       92, 86, 14),
                ('Mathematics',            92, 78, 18),
                ('Combined Science',       92, 80, 12),
                ('History',                65, 60,  9),
                ('Geography',              78, 71, 11),
                ('Shona / Ndebele',        92, 88, 17),
                ('Commerce',               48, 42,  6),
                ('Accounts',               44, 37,  5),
                ('Agriculture',            60, 56,  8),
                ('Physical Education',     35, 34,  7),
            ],
        },
        'a_level': {
            'candidates': 38, 'passes': 34, 'distinctions': 10, 'national_average': 55.3,
            'notes': '',
            'subjects': [
                ('Mathematics',            22, 19, 6),
                ('Physics',                20, 17, 5),
                ('Chemistry',              18, 15, 3),
                ('Biology',                16, 14, 3),
                ('History',                12, 11, 1),
                ('Geography',              14, 12, 2),
                ('Accounts',               16, 13, 2),
            ],
        },
    },
    '2025': {
        'o_level': {
            'candidates': 98, 'passes': 91, 'distinctions': 27, 'national_average': 64.5,
            'notes': 'School pass rate of 92.9% — 28.4 percentage points above the national average.',
            'subjects': [
                ('English Language',       98, 93, 16),
                ('Mathematics',            98, 85, 21),
                ('Combined Science',       98, 88, 14),
                ('History',                70, 65, 11),
                ('Geography',              82, 77, 13),
                ('Shona / Ndebele',        98, 95, 20),
                ('Commerce',               52, 47,  7),
                ('Accounts',               48, 41,  6),
                ('Agriculture',            65, 61,  9),
                ('Physical Education',     40, 39,  8),
            ],
        },
        'a_level': {
            'candidates': 42, 'passes': 38, 'distinctions': 13, 'national_average': 56.2,
            'notes': 'Three students achieved straight A grades across all subjects.',
            'subjects': [
                ('Mathematics',            24, 21, 7),
                ('Physics',                22, 19, 6),
                ('Chemistry',              20, 17, 4),
                ('Biology',                18, 16, 4),
                ('History',                14, 13, 2),
                ('Geography',              16, 14, 3),
                ('Accounts',               18, 15, 3),
            ],
        },
    },
}


class Command(BaseCommand):
    help = 'Seed ZIMSEC results (2023–2025) for Nechilibi High School'

    def handle(self, *args, **options):
        total_results = 0
        total_subjects = 0

        for year, levels in DATA.items():
            for level_key, data in levels.items():
                result, _ = ZIMSECResult.objects.update_or_create(
                    year=year,
                    level=level_key,
                    defaults={
                        'total_candidates': data['candidates'],
                        'total_passes':     data['passes'],
                        'distinctions':     data['distinctions'],
                        'national_average': data['national_average'],
                        'notes':            data['notes'],
                        'is_published':     True,
                    }
                )
                total_results += 1

                for subj_name, cands, passes, dists in data['subjects']:
                    SubjectResult.objects.update_or_create(
                        exam=result,
                        subject=subj_name,
                        defaults={
                            'candidates':   cands,
                            'passes':       passes,
                            'distinctions': dists,
                        }
                    )
                    total_subjects += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {total_results} exam results and {total_subjects} subject entries.'
        ))
