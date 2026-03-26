import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django_school_management.academics.models import AcademicSession, Semester, Department, Subject

# ── Academic session ──────────────────────────────────────────────────────────
session, created = AcademicSession.objects.get_or_create(
    year=2025,
    defaults={'created_by': None}
)
print("Academic session 2025-2026:", "created" if created else "already exists")

# ── Semesters / Terms (numbered 1–3) ─────────────────────────────────────────
for number in [1, 2, 3]:
    Semester.objects.get_or_create(
        number=number,
        defaults={'created_by': None}
    )
print("Terms (semesters) ensured: 1, 2, 3")

# ── Departments (Streams) ─────────────────────────────────────────────────────
dept_data = [
    ('Sciences',     'SCI', 101),
    ('Humanities',   'HUM', 102),
    ('Commercials',  'COM', 103),
    ('Arts',         'ART', 104),
]
for name, short_name, code in dept_data:
    Department.objects.get_or_create(
        name=name,
        defaults={'short_name': short_name, 'code': code, 'created_by': None}
    )
print("Departments created:", Department.objects.count())

# ── ZIMSEC Subjects ───────────────────────────────────────────────────────────
subjects_data = [
    # (name, subject_code, theory_marks, practical_marks)
    ('Mathematics',                   1001, 100, 0),
    ('Additional Mathematics',        1002, 100, 0),
    ('Physics',                       1003,  80, 20),
    ('Chemistry',                     1004,  80, 20),
    ('Biology',                       1005,  80, 20),
    ('Combined Science',              1006,  80, 20),
    ('English Language',              2001, 100, 0),
    ('English Literature',            2002, 100, 0),
    ('Shona',                         2003, 100, 0),
    ('Ndebele',                       2004, 100, 0),
    ('History',                       2005, 100, 0),
    ('Geography',                     2006, 100, 0),
    ('Religious and Moral Education', 2007, 100, 0),
    ('Accounts',                      3001, 100, 0),
    ('Commerce',                      3002, 100, 0),
    ('Economics',                     3003, 100, 0),
    ('Business Studies',              3004, 100, 0),
]
for subj_name, code, theory, practical in subjects_data:
    Subject.objects.get_or_create(
        subject_code=code,
        defaults={
            'name': subj_name,
            'theory_marks': theory,
            'practical_marks': practical,
            'created_by': None,
        }
    )
print("Subjects created:", Subject.objects.count())

# ── Gallery categories ────────────────────────────────────────────────────────
from django_school_management.gallery.models import GalleryCategory

cats = [
    ('School Life', 'school-life', 1),
    ('Sports',      'sports',      2),
    ('Events',      'events',      3),
    ('Facilities',  'facilities',  4),
    ('Graduation',  'graduation',  5),
]
for name, slug, order in cats:
    GalleryCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'order': order})
print("Gallery categories created:", GalleryCategory.objects.count())

# ── Download categories ───────────────────────────────────────────────────────
from django_school_management.downloads.models import DownloadCategory

dl_cats = [
    ('Application Forms', 1),
    ('School Calendar',   2),
    ('Syllabi',           3),
    ('Timetables',        4),
    ('Newsletters',       5),
]
for name, order in dl_cats:
    DownloadCategory.objects.get_or_create(name=name, defaults={'order': order})
print("Download categories created:", DownloadCategory.objects.count())

print("\nSeed complete.")
