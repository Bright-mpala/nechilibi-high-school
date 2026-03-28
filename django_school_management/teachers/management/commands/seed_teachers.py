"""
Seed teachers and designations for Nechilibi High School.
Safe to run multiple times (uses get_or_create).
Writes all errors to stderr so they appear in Railway deploy logs.
"""
import os
import sys
import traceback

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from django_school_management.teachers.models import Teacher, Designation

LOGO_PATH = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')


def logo_file():
    if os.path.exists(LOGO_PATH):
        return open(LOGO_PATH, 'rb')
    return None


DESIGNATIONS = [
    ('Headmaster',                 'headmaster'),
    ('Deputy Headmaster',          'deputy'),
    ('Head of Sciences',           'senior_teacher'),
    ('Head of Mathematics',        'senior_teacher'),
    ('Head of Languages',          'senior_teacher'),
    ('Head of Humanities',         'senior_teacher'),
    ('Head of Commerce',           'senior_teacher'),
    ('Biology Teacher',            'teacher'),
    ('Chemistry Teacher',          'teacher'),
    ('Physics Teacher',            'teacher'),
    ('Mathematics Teacher',        'teacher'),
    ('English Language Teacher',   'teacher'),
    ('History Teacher',            'teacher'),
    ('Geography Teacher',          'teacher'),
    ('Accounts Teacher',           'teacher'),
    ('Agriculture Teacher',        'teacher'),
    ('ICT Teacher',                'teacher'),
    ('Physical Education Teacher', 'teacher'),
]

TEACHERS = [
    ('NHS001', 'Mr T. Ndlovu',   'headmaster',     'Headmaster',
     'Mr Ndlovu has served as Headmaster of Nechilibi High School since 2018. '
     'He holds an M.Ed. in Educational Leadership from NUST and is committed to academic excellence.'),

    ('NHS002', 'Mrs R. Mpofu',   'deputy',         'Deputy Headmaster',
     'Mrs Mpofu is the Deputy Headmaster and Head of Academics. '
     'She has 22 years of teaching experience and specialises in English Literature.'),

    ('NHS003', 'Mr S. Dube',     'senior_teacher', 'Head of Sciences',
     'Mr Dube leads the Science Department and teaches Biology and Chemistry at A-Level. '
     'He is the school\'s most decorated teacher with several national science mentorship awards.'),

    ('NHS004', 'Mrs P. Moyo',    'senior_teacher', 'Head of Mathematics',
     'Mrs Moyo has been teaching Mathematics at Nechilibi for 15 years. '
     'She leads the school\'s Mathematics Olympiad programme.'),

    ('NHS005', 'Mr B. Sibanda',  'senior_teacher', 'Head of Languages',
     'Mr Sibanda oversees the Languages Department, teaching English Language and Ndebele. '
     'He runs the school\'s annual creative writing competition.'),

    ('NHS006', 'Mrs F. Ncube',   'senior_teacher', 'Head of Humanities',
     'Mrs Ncube leads the Humanities Department and teaches History and Geography. '
     'She is also the patron of the school\'s Debating Club.'),

    ('NHS007', 'Mr C. Tshuma',   'senior_teacher', 'Head of Commerce',
     'Mr Tshuma leads the Commerce Department and teaches Accounts and Business Studies. '
     'He is a qualified CPA and brings real-world business experience to the classroom.'),

    ('NHS008', 'Mr K. Nkosi',    'teacher',        'Biology Teacher',
     'Mr Nkosi teaches Biology at O and A-Level. He holds a BSc in Biological Sciences '
     'and is passionate about environmental conservation education.'),

    ('NHS009', 'Mrs G. Mhlanga', 'teacher',        'Chemistry Teacher',
     'Mrs Mhlanga teaches Chemistry and is the school\'s laboratory supervisor. '
     'She ensures that practical lessons are safe and aligned with the ZIMSEC curriculum.'),

    ('NHS010', 'Mr A. Dlamini',  'teacher',        'Physics Teacher',
     'Mr Dlamini teaches Physics at O and A-Level and runs the robotics after-school club. '
     'He is a graduate of Lupane State University.'),

    ('NHS011', 'Mrs L. Moyo',    'teacher',        'Mathematics Teacher',
     'Mrs L. Moyo teaches Pure Mathematics and Additional Mathematics at O-Level. '
     'She is known for her patient teaching approach and a 100% pass rate over three years.'),

    ('NHS012', 'Mr D. Ndebele',  'teacher',        'English Language Teacher',
     'Mr Ndebele teaches English Language and Literature. He holds a BA Honours in English '
     'and is the patron of the school\'s Drama Club.'),

    ('NHS013', 'Mrs T. Zulu',    'teacher',        'History Teacher',
     'Mrs Zulu teaches History at O and A-Level and brings a deep passion for African history.'),

    ('NHS014', 'Mr P. Sibanda',  'teacher',        'Accounts Teacher',
     'Mr P. Sibanda teaches Principles of Accounts and Commerce at O-Level. '
     'He is an active member of the Zimbabwe Association of Commerce Teachers.'),

    ('NHS015', 'Mr W. Khumalo',  'teacher',        'Agriculture Teacher',
     'Mr Khumalo manages the school farm and teaches Agriculture to Form 3 and Form 4 students. '
     'Under his guidance the school has won the District Best School Farm Award twice.'),
]


class Command(BaseCommand):
    help = 'Seed teacher and designation records for Nechilibi High School'

    def handle(self, *args, **options):
        self.stdout.write('--- Seeding Designations ---')
        desig_map = {}
        for title, role in DESIGNATIONS:
            try:
                obj, created = Designation.objects.get_or_create(
                    title=title, defaults={'role': role}
                )
                desig_map[title] = obj
                self.stdout.write(f'  {"Created" if created else "OK"}: {title}')
            except Exception:
                self.stderr.write(f'  ERROR creating designation "{title}":')
                self.stderr.write(traceback.format_exc())
                raise

        self.stdout.write('--- Seeding Teachers ---')
        logo = os.path.exists(LOGO_PATH)
        self.stdout.write(f'  Logo path: {LOGO_PATH}  exists={logo}')

        for emp_id, name, role, desig_title, bio in TEACHERS:
            try:
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
                self.stdout.write(f'  {"Created" if created else "OK"}: {name}')

                if not obj.photo and logo:
                    try:
                        with open(LOGO_PATH, 'rb') as f:
                            obj.photo.save('teacher_photo.jpg', File(f), save=True)
                        self.stdout.write(f'    Photo saved for {name}')
                    except Exception:
                        self.stderr.write(f'    WARNING: could not save photo for {name}:')
                        self.stderr.write(traceback.format_exc())
            except Exception:
                self.stderr.write(f'  ERROR creating teacher "{name}":')
                self.stderr.write(traceback.format_exc())
                raise

        total = Teacher.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'Teachers seeded OK. Total active teachers: {total}'))
