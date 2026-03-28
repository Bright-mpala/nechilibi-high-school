"""
Master seed command — seeds ALL content for Nechilibi High School.
Uses logo.jpg as the placeholder image for everything that needs a photo.

Run:  python manage.py seed_everything
Safe to run multiple times (uses get_or_create / update_or_create).
"""
import os
import io
from datetime import date

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.management import call_command


LOGO_PATH = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')


def logo_file():
    """Return an open file handle to logo.jpg, or None if missing."""
    if os.path.exists(LOGO_PATH):
        return open(LOGO_PATH, 'rb')
    return None


class Command(BaseCommand):
    help = 'Seed ALL Nechilibi High School content (teachers, gallery, sports, news, fees, etc.)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Nechilibi Full Site Seed ===\n'))

        if not os.path.exists(LOGO_PATH):
            self.stdout.write(self.style.WARNING(
                f'  WARNING: logo not found at {LOGO_PATH}. Images will be skipped.'
            ))

        # Run existing seed commands first (they are idempotent)
        self._run_existing_seeds()

        # New seeds
        self._seed_teachers()
        self._seed_gallery_with_logo()
        self._seed_sport_images()
        self._seed_testimonial_photos()

        self.stdout.write(self.style.SUCCESS('\n=== All content seeded successfully! ===\n'))

    # ──────────────────────────────────────────────────────────────
    # Delegate to existing seed commands
    # ──────────────────────────────────────────────────────────────

    def _run_existing_seeds(self):
        existing = [
            ('seed_nechilibi',  'Academic sessions, departments, social links'),
            ('seed_site',       'School settings, hero banners, highlights, notices, events, downloads, articles'),
            ('seed_calendar',   'Academic calendar & term dates'),
            ('seed_results',    'ZIMSEC results'),
            ('seed_fees',       'Fee structure'),
            ('seed_subjects',   'Subjects offered'),
            ('seed_sports',     'Sports, clubs & societies'),
        ]
        for cmd, label in existing:
            self.stdout.write(f'\n--- {label} ---')
            try:
                call_command(cmd, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'  {cmd} OK'))
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f'  {cmd} skipped: {exc}'))

    # ──────────────────────────────────────────────────────────────
    # Teachers
    # ──────────────────────────────────────────────────────────────

    def _seed_teachers(self):
        from django_school_management.teachers.models import Teacher, Designation

        self.stdout.write('\n--- Teachers ---')

        # 1. Create Designation records
        designations_data = [
            ('Headmaster',              'headmaster'),
            ('Deputy Headmaster',       'deputy'),
            ('Head of Sciences',        'senior_teacher'),
            ('Head of Mathematics',     'senior_teacher'),
            ('Head of Languages',       'senior_teacher'),
            ('Head of Humanities',      'senior_teacher'),
            ('Head of Commerce',        'senior_teacher'),
            ('Biology Teacher',         'teacher'),
            ('Chemistry Teacher',       'teacher'),
            ('Physics Teacher',         'teacher'),
            ('Mathematics Teacher',     'teacher'),
            ('English Language Teacher','teacher'),
            ('History Teacher',         'teacher'),
            ('Geography Teacher',       'teacher'),
            ('Accounts Teacher',        'teacher'),
            ('Agriculture Teacher',     'teacher'),
            ('ICT Teacher',             'teacher'),
            ('Physical Education Teacher', 'teacher'),
        ]
        desig_map = {}
        for title, role in designations_data:
            obj, _ = Designation.objects.get_or_create(
                title=title, defaults={'role': role}
            )
            desig_map[title] = obj

        # 2. Teacher data
        # role choices: headmaster | deputy | senior_teacher | teacher
        teachers_data = [
            # (employee_id, name, role, designation_title, bio)
            ('NHS001', 'Mr T. Ndlovu',   'headmaster',     'Headmaster',
             'Mr Ndlovu has served as Headmaster of Nechilibi High School since 2018. '
             'He holds an M.Ed. in Educational Leadership from NUST and is committed to academic excellence and community development.'),

            ('NHS002', 'Mrs R. Mpofu',   'deputy',         'Deputy Headmaster',
             'Mrs Mpofu is the Deputy Headmaster and Head of Academics. '
             'She has 22 years of teaching experience and specialises in English Literature and Language.'),

            ('NHS003', 'Mr S. Dube',     'senior_teacher', 'Head of Sciences',
             'Mr Dube leads the Science Department and teaches Biology and Chemistry at A-Level. '
             'He is the school\'s most decorated teacher with several national science mentorship awards.'),

            ('NHS004', 'Mrs P. Moyo',    'senior_teacher', 'Head of Mathematics',
             'Mrs Moyo has been teaching Mathematics at Nechilibi for 15 years. '
             'She leads the school\'s Mathematics Olympiad programme and has produced multiple national-level competitors.'),

            ('NHS005', 'Mr B. Sibanda',  'senior_teacher', 'Head of Languages',
             'Mr Sibanda oversees the Languages Department, teaching English Language and Ndebele. '
             'He has a passion for literature and runs the school\'s annual creative writing competition.'),

            ('NHS006', 'Mrs F. Ncube',   'senior_teacher', 'Head of Humanities',
             'Mrs Ncube leads the Humanities Department and teaches History and Geography at both O and A-Level. '
             'She is also the patron of the school\'s Debating Club.'),

            ('NHS007', 'Mr C. Tshuma',   'senior_teacher', 'Head of Commerce',
             'Mr Tshuma leads the Commerce Department and teaches Accounts and Business Studies. '
             'He is a qualified CPA and brings real-world business experience to the classroom.'),

            ('NHS008', 'Mr K. Nkosi',    'teacher',        'Biology Teacher',
             'Mr Nkosi teaches Biology at O and A-Level. He holds a BSc in Biological Sciences from the University of Zimbabwe '
             'and is passionate about environmental conservation education.'),

            ('NHS009', 'Mrs G. Mhlanga', 'teacher',        'Chemistry Teacher',
             'Mrs Mhlanga teaches Chemistry and is the school\'s laboratory supervisor. '
             'She ensures that practical lessons are safe, engaging, and aligned with the ZIMSEC curriculum.'),

            ('NHS010', 'Mr A. Dlamini',  'teacher',        'Physics Teacher',
             'Mr Dlamini teaches Physics at O and A-Level and runs the school\'s robotics and electronics after-school club. '
             'He is a graduate of Lupane State University.'),

            ('NHS011', 'Mrs L. Moyo',    'teacher',        'Mathematics Teacher',
             'Mrs L. Moyo teaches Pure Mathematics and Additional Mathematics at O-Level. '
             'She is known for her patient teaching approach and has a 100% pass rate over the last three years.'),

            ('NHS012', 'Mr D. Ndebele',  'teacher',        'English Language Teacher',
             'Mr Ndebele teaches English Language and Literature. He holds a BA Honours in English from NUST '
             'and is the patron of the school\'s Drama Club.'),

            ('NHS013', 'Mrs T. Zulu',    'teacher',        'History Teacher',
             'Mrs Zulu teaches History at O and A-Level. She is a graduate of the University of Zimbabwe '
             'and brings a deep passion for Zimbabwean and African history to her lessons.'),

            ('NHS014', 'Mr P. Sibanda',  'teacher',        'Accounts Teacher',
             'Mr P. Sibanda teaches Principles of Accounts and Commerce at O-Level. '
             'He is an active member of the Zimbabwe Association of Commerce Teachers.'),

            ('NHS015', 'Mr W. Khumalo',  'teacher',        'Agriculture Teacher',
             'Mr Khumalo manages the school farm and teaches Agriculture to Form 3 and Form 4 students. '
             'Under his guidance, the school has won the District Best School Farm Award twice.'),
        ]

        for emp_id, name, role, desig_title, bio in teachers_data:
            obj, created = Teacher.objects.get_or_create(
                employee_id=emp_id,
                defaults={
                    'name': name,
                    'role': role,
                    'designation': desig_map[desig_title],
                    'bio': bio,
                    'is_active': True,
                    'created_by': None,
                }
            )
            # Attach logo as photo if no photo yet
            if not obj.photo:
                f = logo_file()
                if f:
                    with f:
                        obj.photo.save('teacher_photo.jpg', File(f), save=True)
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} teacher: {name}')

    # ──────────────────────────────────────────────────────────────
    # Gallery — seed with logo where no real images exist
    # ──────────────────────────────────────────────────────────────

    def _seed_gallery_with_logo(self):
        from django_school_management.gallery.models import GalleryCategory, GalleryImage

        self.stdout.write('\n--- Gallery Images ---')

        categories_data = [
            ('school-life',        'School Life',           0),
            ('sports-culture',     'Sports & Culture',      1),
            ('infrastructure',     'Infrastructure',        2),
            ('events-ceremonies',  'Events & Ceremonies',   3),
        ]
        cats = {}
        for slug, name, order in categories_data:
            cat, _ = GalleryCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'order': order}
            )
            cats[slug] = cat

        # Images to create using logo (skipped if a real image already exists for that title)
        images_data = [
            ('School Assembly',              'school-life',       True,  0),
            ('Students in Class',            'school-life',       True,  1),
            ('Break Time at School',         'school-life',       False, 2),
            ('Morning Parade',               'school-life',       False, 3),
            ('Football Practice',            'sports-culture',    True,  4),
            ('Netball Match',                'sports-culture',    True,  5),
            ('Athletics Day',                'sports-culture',    False, 6),
            ('School Building Front',        'infrastructure',    True,  7),
            ('School Classroom Block',       'infrastructure',    True,  8),
            ('School Library',               'infrastructure',    False, 9),
            ('Science Laboratory',           'infrastructure',    False, 10),
            ('Prize Giving Ceremony',        'events-ceremonies', True,  11),
            ('Annual Sports Day',            'events-ceremonies', True,  12),
            ('Graduation Day',               'events-ceremonies', False, 13),
            ('Cultural Day Celebration',     'events-ceremonies', False, 14),
        ]

        for title, cat_slug, featured, order in images_data:
            # Skip if an image with this exact title already exists
            if GalleryImage.objects.filter(title=title).exists():
                self.stdout.write(f'  Skipping (exists): {title}')
                continue

            f = logo_file()
            if not f:
                self.stdout.write(self.style.WARNING(f'  No logo found — skipping: {title}'))
                continue

            with f:
                img = GalleryImage(
                    title=title,
                    category=cats.get(cat_slug),
                    is_featured=featured,
                    order=order,
                    is_active=True,
                )
                img.image.save('gallery_photo.jpg', File(f), save=True)
            self.stdout.write(f'  Created gallery image: {title}')

    # ──────────────────────────────────────────────────────────────
    # Sports — attach logo image to any club without an image
    # ──────────────────────────────────────────────────────────────

    def _seed_sport_images(self):
        from django_school_management.nechilibi.models import SportClub

        self.stdout.write('\n--- Sport/Club Images ---')
        try:
            for club in SportClub.objects.filter(image=''):
                f = logo_file()
                if f:
                    with f:
                        club.image.save('sport_logo.jpg', File(f), save=True)
                    self.stdout.write(f'  Added image to: {club.name}')
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f'  Skipped sport images: {exc}'))

    # ──────────────────────────────────────────────────────────────
    # Testimonials — attach logo photo to any without a photo
    # ──────────────────────────────────────────────────────────────

    def _seed_testimonial_photos(self):
        from django_school_management.nechilibi.models import Testimonial

        self.stdout.write('\n--- Testimonial Photos ---')
        try:
            for t in Testimonial.objects.filter(photo=''):
                f = logo_file()
                if f:
                    with f:
                        t.photo.save('testimonial_photo.jpg', File(f), save=True)
                    self.stdout.write(f'  Added photo to: {t.name}')
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f'  Skipped testimonial photos: {exc}'))
