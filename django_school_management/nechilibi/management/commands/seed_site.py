"""
Management command to seed Nechilibi High School site content with real images.
Run: python manage.py seed_site
Safe to run multiple times (uses update_or_create / get_or_create).
Does NOT create any user accounts.
"""
import os
import io
from datetime import date

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed Nechilibi High School site with realistic content and images'

    def handle(self, *args, **options):
        self._seed_school_settings()
        self._seed_hero_banners()
        self._seed_highlights()
        self._seed_gallery()
        self._seed_testimonials()
        self._seed_notices()
        self._seed_events()
        self._seed_downloads()
        self.stdout.write(self.style.SUCCESS('\nAll content seeded successfully!'))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _media_path(self, rel):
        """Absolute path to a file in MEDIA_ROOT."""
        return os.path.join(settings.MEDIA_ROOT, rel)

    def _static_path(self, rel):
        """Absolute path to a file in the project static dir."""
        base = os.path.dirname(settings.MEDIA_ROOT)  # project root
        return os.path.join(base, 'static', rel)

    def _open_image(self, abs_path):
        """Return an open File handle if the path exists, else None."""
        if os.path.exists(abs_path):
            return open(abs_path, 'rb')
        return None

    # ------------------------------------------------------------------
    # School Settings
    # ------------------------------------------------------------------

    def _seed_school_settings(self):
        from django_school_management.nechilibi.models import SchoolSettings

        logo_path = os.path.join(settings.MEDIA_ROOT, 'school', 'Logo.jpg')
        static_logo = self._static_path('img/school/Logo.jpg')

        obj, created = SchoolSettings.objects.update_or_create(
            pk=1,
            defaults={
                'school_name': 'Nechilibi High School',
                'tagline': 'Shaping Tomorrow\'s Leaders',
                'address': 'Nechilibi, Gwanda District, Matabeleland South, Zimbabwe',
                'phone': '+263 XX XXX XXXX',
                'email': 'nechilibi.highschool@gmail.com',
                'hero_text': 'Welcome to Nechilibi High School',
                'hero_subtext': (
                    'Nechilibi High School is a premier secondary school in Matabeleland South, '
                    'Zimbabwe, offering Form 1 to Form 6 education under ZIMSEC and Cambridge '
                    'curricula. We are committed to academic excellence, holistic development, '
                    'and producing future leaders of Zimbabwe.'
                ),
                'facebook_url': 'https://www.facebook.com/nechilibihighschool',
                'whatsapp_number': '+263771234567',
            }
        )

        # Attach logo image if not already set
        if not obj.logo:
            src = logo_path if os.path.exists(logo_path) else static_logo
            if os.path.exists(src):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'school'), exist_ok=True)
                with open(src, 'rb') as f:
                    obj.logo.save('Logo.jpg', File(f), save=True)

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  {action} school settings.')

    # ------------------------------------------------------------------
    # Hero Banners (pages app)
    # ------------------------------------------------------------------

    def _seed_hero_banners(self):
        from django_school_management.pages.models import HeroBanner

        slides = [
            {
                'order': 1,
                'title': 'Welcome to Nechilibi High School',
                'subtitle': 'Shaping Tomorrow\'s Leaders Since 1985',
                'cta_text': 'Learn More',
                'cta_url': '/about/',
                'img_static': 'img/hero/1.jpg',
                'img_media': 'gallery/school_1.jpg',
            },
            {
                'order': 2,
                'title': 'Academic Excellence',
                'subtitle': 'ZIMSEC and Cambridge Curricula — Preparing Students for the World',
                'cta_text': 'Our Programmes',
                'cta_url': '/academics/',
                'img_static': 'img/hero/2.jpg',
                'img_media': 'gallery/school_2.jpg',
            },
            {
                'order': 3,
                'title': 'A Nurturing Environment',
                'subtitle': 'Holistic Education: Mind, Body and Spirit',
                'cta_text': 'Gallery',
                'cta_url': '/gallery/',
                'img_static': 'img/hero/3.jpg',
                'img_media': 'gallery/school_3.jpg',
            },
            {
                'order': 4,
                'title': 'Proud Heritage, Bright Future',
                'subtitle': 'Serving the Gwanda District and Matabeleland South since 1985',
                'cta_text': 'Our History',
                'cta_url': '/about/',
                'img_static': 'img/hero/4.jpg',
                'img_media': 'gallery/school_4.jpg',
            },
            {
                'order': 5,
                'title': 'Sports, Arts & Culture',
                'subtitle': 'Beyond the Classroom — Building Well-Rounded Individuals',
                'cta_text': 'Events',
                'cta_url': '/events/',
                'img_static': 'img/hero/5.jpg',
                'img_media': 'gallery/school_5.jpg',
            },
        ]

        for slide in slides:
            obj, created = HeroBanner.objects.update_or_create(
                order=slide['order'],
                defaults={
                    'title': slide['title'],
                    'subtitle': slide['subtitle'],
                    'cta_text': slide['cta_text'],
                    'cta_url': slide['cta_url'],
                    'is_active': True,
                }
            )

            if not obj.image:
                # Try static hero first, then media gallery fallback
                static_abs = self._static_path(slide['img_static'])
                media_abs = self._media_path(slide['img_media'])
                src = None
                if os.path.exists(static_abs):
                    src = static_abs
                elif os.path.exists(media_abs):
                    src = media_abs

                if src:
                    fname = os.path.basename(src)
                    with open(src, 'rb') as f:
                        obj.image.save(fname, File(f), save=True)

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} hero slide {slide["order"]}: {slide["title"]}')

    # ------------------------------------------------------------------
    # School Highlights (pages app)
    # ------------------------------------------------------------------

    def _seed_highlights(self):
        from django_school_management.pages.models import SchoolHighlight

        highlights = [
            ('fas fa-user-graduate', '500+', 'Students Enrolled', 0),
            ('fas fa-chalkboard-teacher', '40+', 'Qualified Teachers', 1),
            ('fas fa-trophy', '95%', 'ZIMSEC Pass Rate', 2),
            ('fas fa-calendar-alt', '1985', 'Year Established', 3),
        ]
        for icon, value, label, order in highlights:
            _, created = SchoolHighlight.objects.update_or_create(
                label=label,
                defaults={'icon_class': icon, 'value': value, 'order': order}
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} highlight: {value} {label}')

    # ------------------------------------------------------------------
    # Gallery (gallery app)
    # ------------------------------------------------------------------

    def _seed_gallery(self):
        from django_school_management.gallery.models import GalleryCategory, GalleryImage

        categories_data = [
            ('school-life', 'School Life', 0),
            ('sports-culture', 'Sports & Culture', 1),
            ('infrastructure', 'Infrastructure', 2),
            ('events-ceremonies', 'Events & Ceremonies', 3),
        ]
        cats = {}
        for slug, name, order in categories_data:
            cat, created = GalleryCategory.objects.update_or_create(
                slug=slug,
                defaults={'name': name, 'order': order}
            )
            cats[slug] = cat
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} gallery category: {name}')

        # Images to seed: (filename_in_media_gallery, title, category_slug, is_featured, order)
        gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery')
        images_data = [
            ('IMG_0001.jpg',        'School Assembly Grounds',      'school-life',       True,  0),
            ('IMG_0010.jpg',        'Students at School',           'school-life',       True,  1),
            ('IMG_0031.jpg',        'School Grounds',               'infrastructure',    True,  2),
            ('IMG_0035.jpg',        'School Building',              'infrastructure',    True,  3),
            ('IMG_0106.jpg',        'School Activities',            'school-life',       False, 4),
            ('IMG_0134.jpg',        'School Events',                'events-ceremonies', True,  5),
            ('IMG_0137.jpg',        'Sports & Recreation',          'sports-culture',    True,  6),
            ('IMG_0143.jpg',        'Cultural Activities',          'sports-culture',    False, 7),
            ('IMG_0149.jpg',        'Prize Giving Ceremony',        'events-ceremonies', False, 8),
            ('school_1.jpg',        'Nechilibi School Front',       'infrastructure',    False, 9),
            ('school_2.jpg',        'School Campus',                'infrastructure',    False, 10),
            ('school_3.jpg',        'School Life Moments',          'school-life',       False, 11),
            ('school_4.jpg',        'School Uniform — Maroon',      'school-life',       False, 12),
            ('school_5.jpg',        'School Activities',            'events-ceremonies', False, 13),
            ('IMG_0010 (1).jpg',    'Students Learning',            'school-life',       False, 14),
            ('IMG_0031 (1).jpg',    'Campus View',                  'infrastructure',    False, 15),
            ('IMG_0035 (1).jpg',    'School Facilities',            'infrastructure',    False, 16),
        ]

        for filename, title, cat_slug, featured, order in images_data:
            abs_path = os.path.join(gallery_dir, filename)
            if not os.path.exists(abs_path):
                self.stdout.write(self.style.WARNING(f'  Skipping (not found): {filename}'))
                continue

            rel_path = f'gallery/{filename}'
            # Check if already seeded by image path
            existing = GalleryImage.objects.filter(image=rel_path).first()
            if existing:
                existing.title = title
                existing.category = cats.get(cat_slug)
                existing.is_featured = featured
                existing.order = order
                existing.is_active = True
                existing.save(update_fields=['title', 'category', 'is_featured', 'order', 'is_active'])
                self.stdout.write(f'  Updated gallery image: {title}')
            else:
                img_obj = GalleryImage(
                    title=title,
                    category=cats.get(cat_slug),
                    is_featured=featured,
                    order=order,
                    is_active=True,
                )
                with open(abs_path, 'rb') as f:
                    img_obj.image.save(filename, File(f), save=True)
                self.stdout.write(f'  Created gallery image: {title}')

    # ------------------------------------------------------------------
    # Testimonials (nechilibi app)
    # ------------------------------------------------------------------

    def _seed_testimonials(self):
        from django_school_management.nechilibi.models import Testimonial

        testimonials = [
            {
                'name': 'Mrs Sibanda',
                'role': 'Parent',
                'message': (
                    'Nechilibi High gave my child the foundation to excel at university. '
                    'The teachers are dedicated and the environment is nurturing.'
                ),
            },
            {
                'name': 'Takudzwa Moyo',
                'role': 'Alumni 2018',
                'message': (
                    'I am proud to be a Nechilibi alumnus. The school shaped my character '
                    'and prepared me for the world.'
                ),
            },
            {
                'name': 'Mr Ncube',
                'role': 'Parent',
                'message': (
                    'The ZIMSEC results here speak for themselves. A school that truly '
                    'cares about every student.'
                ),
            },
            {
                'name': 'Thandiwe Dube',
                'role': 'Alumni 2020',
                'message': (
                    'Form 6 at Nechilibi was challenging but rewarding. I passed my '
                    'A-Levels with flying colours thanks to my teachers.'
                ),
            },
        ]

        for data in testimonials:
            obj, created = Testimonial.objects.update_or_create(
                name=data['name'],
                defaults={
                    'role': data['role'],
                    'message': data['message'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} testimonial: {data["name"]}')

    # ------------------------------------------------------------------
    # Notices
    # ------------------------------------------------------------------

    def _seed_notices(self):
        from django_school_management.notices.models import Notice

        notices = [
            {
                'title': '2025 Form 1 Intake Now Open',
                'content': (
                    'Applications for Form 1 intake 2026 are now open. '
                    'Visit the school office for admission requirements and application forms. '
                    'Deadline: 31 January 2026.'
                ),
                'expires_at': date(2026, 1, 31),
            },
            {
                'title': 'Term 2 2025 Timetable Released',
                'content': (
                    'The Term 2 2025 timetable has been finalised and is now available. '
                    'Students and parents may collect printed copies from the school office '
                    'or download from the school website.'
                ),
                'expires_at': date(2026, 6, 30),
            },
            {
                'title': 'Annual Prize Giving Day — 28 March 2026',
                'content': (
                    'The Annual Prize Giving Day ceremony will be held on 28 March 2026. '
                    'All parents, guardians and community members are invited to attend '
                    'and celebrate the achievements of our students.'
                ),
                'expires_at': date(2026, 3, 31),
            },
            {
                'title': 'ZIMSEC November 2025 Results Available',
                'content': (
                    'ZIMSEC November 2025 Ordinary Level and Advanced Level results are now '
                    'available. Students may collect their statements from the school office '
                    'or check on the ZIMSEC online portal.'
                ),
                'expires_at': date(2026, 6, 30),
            },
        ]

        for data in notices:
            obj, created = Notice.objects.update_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'expires_at': data['expires_at'],
                    'notice_type': 'n',
                    'uploaded_by': None,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} notice: {data["title"]}')

    # ------------------------------------------------------------------
    # Events (pages app)
    # ------------------------------------------------------------------

    def _seed_events(self):
        from django.utils.text import slugify
        from django_school_management.events.models import Event

        events = [
            {
                'title': 'Prize Giving Day 2026',
                'slug': 'prize-giving-day-2026',
                'description': (
                    'The annual Prize Giving Day ceremony celebrates the academic, sporting and '
                    'cultural achievements of Nechilibi High School students. All parents and '
                    'guardians are warmly invited to attend.'
                ),
                'start_date': date(2026, 3, 28),
                'location': 'Nechilibi High School Main Hall',
            },
            {
                'title': 'Form 1 Orientation Day',
                'slug': 'form-1-orientation-day-2026',
                'description': (
                    'Orientation day for all new Form 1 students joining Nechilibi High School '
                    'in 2026. Students and parents are expected to attend for school tour, '
                    'uniform collection and timetable distribution.'
                ),
                'start_date': date(2026, 1, 15),
                'location': 'Nechilibi High School',
            },
            {
                'title': 'Sports Day 2026',
                'slug': 'sports-day-2026',
                'description': (
                    'The annual inter-house Sports Day featuring track and field events, '
                    'team sports and cultural performances. Students compete for the coveted '
                    'Nechilibi Sports Champion trophy.'
                ),
                'start_date': date(2026, 4, 10),
                'location': 'Nechilibi High School Sports Grounds',
            },
            {
                'title': 'Parents & Teachers Meeting',
                'slug': 'parents-teachers-meeting-2026',
                'description': (
                    'A formal meeting between parents/guardians and class teachers to discuss '
                    'student progress, Term 1 results and the academic roadmap for 2026. '
                    'Attendance by all parents is strongly encouraged.'
                ),
                'start_date': date(2026, 2, 14),
                'location': 'Nechilibi High School',
            },
        ]

        for data in events:
            obj, created = Event.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'start_date': data['start_date'],
                    'location': data['location'],
                    'is_published': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} event: {data["title"]}')

    # ------------------------------------------------------------------
    # Downloads (pages app — no required file field, uses is_published)
    # ------------------------------------------------------------------

    def _seed_downloads(self):
        from django_school_management.pages.models import Download

        downloads = [
            {
                'title': 'School Fee Structure 2026',
                'category': 'other',
                'description': (
                    'Official Nechilibi High School fee structure for 2026, including tuition, '
                    'boarding, examination and development levies. Contact the bursar for '
                    'payment plan options.'
                ),
            },
            {
                'title': '2026 Academic Calendar',
                'category': 'timetable',
                'description': (
                    'Full academic calendar for 2026 showing term dates, public holidays, '
                    'examination periods and school events for Form 1 to Form 6 students.'
                ),
            },
            {
                'title': 'Admission Requirements — Form 1',
                'category': 'forms',
                'description': (
                    'Admission requirements and application form for Form 1 entry 2026. '
                    'Includes required documents: Grade 7 results, birth certificate and '
                    'transfer letter for transferring students.'
                ),
            },
            {
                'title': 'School Rules and Regulations',
                'category': 'policies',
                'description': (
                    'Nechilibi High School code of conduct and rules booklet covering '
                    'discipline, uniform, attendance and general student behaviour expectations.'
                ),
            },
        ]

        for data in downloads:
            # Create a minimal placeholder file in memory so the FileField is satisfied
            placeholder_content = (
                f"[{data['title']}]\n"
                f"This document will be uploaded by the school administration.\n"
                f"Contact: nechilibi.highschool@gmail.com\n"
            ).encode('utf-8')

            obj, created = Download.objects.update_or_create(
                title=data['title'],
                defaults={
                    'category': data['category'],
                    'description': data['description'],
                    'is_published': True,
                }
            )

            # Only attach placeholder file if no file is set yet
            if created or not obj.file:
                safe_name = data['title'].replace(' ', '_').replace('—', '-') + '.txt'
                obj.file.save(safe_name, File(io.BytesIO(placeholder_content)), save=True)

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} download: {data["title"]}')
