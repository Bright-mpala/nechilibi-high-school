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
        self._seed_articles()
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
                'address': 'P.O. Box 123, Nechilibi, Matabeleland South, Zimbabwe',
                'phone': '0780808201',
                'email': 'info@nechilibi.ac.zw',
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

    # ------------------------------------------------------------------
    # Articles / News (20 articles using Logo as featured image)
    # ------------------------------------------------------------------

    def _seed_articles(self):
        from django.core.files import File
        from django_school_management.articles.models import Article, Category

        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')

        cat, _ = Category.objects.get_or_create(
            name='School News',
            defaults={'slug': 'school-news'},
        )

        articles_data = [
            ('Nechilibi Students Excel in ZIMSEC 2025 Examinations',
             '<p>We are proud to announce that Nechilibi High School students achieved outstanding results in the 2025 ZIMSEC O-Level and A-Level examinations. The school recorded a 95% pass rate at O-Level, with 60% of students achieving 5 or more subjects. At A-Level, several students earned university entrance passes in Mathematics, Sciences and Commerce. The school congratulates all students and thanks the dedicated teaching staff for their efforts.</p>'),

            ('New Science Laboratory Officially Opens at Nechilibi',
             '<p>Nechilibi High School officially opened its newly renovated Science Laboratory this term. The modern facility is equipped with microscopes, chemistry apparatus and computer-aided learning resources for Biology, Chemistry and Physics. The laboratory will serve Form 3 to Form 6 students and is expected to significantly improve practical science education at the school.</p>'),

            ('Sports Day 2025 Highlights — Yellow House Takes the Trophy',
             '<p>The annual Nechilibi High School Sports Day 2025 was a tremendous success. Students competed in track and field events, team relays and cultural performances. Yellow House emerged as the overall champions, edging out Red House in the final tally. The day was attended by parents, guardians and community members who cheered on the students.</p>'),

            ('Form 1 Intake 2026 — Applications Now Open',
             '<p>Nechilibi High School is now accepting applications for Form 1 intake for the 2026 academic year. Parents and guardians of Grade 7 graduates are invited to collect application forms from the school office. The school offers both day and boarding options. Successful applicants will be notified by 30 November 2025.</p>'),

            ('Prize Giving Day 2025 — Celebrating Academic Excellence',
             '<p>The 2025 Annual Prize Giving Day was a colourful celebration of student achievement at Nechilibi High School. Top students in each form were recognised for academic excellence, leadership and sportsmanship. The Guest of Honour, a distinguished alumnus, delivered an inspiring address encouraging students to work hard and serve their communities.</p>'),

            ('Nechilibi Hosts Matabeleland South Inter-School Debate',
             '<p>Nechilibi High School proudly hosted the Matabeleland South Inter-School Debate Competition this term. Twelve schools from across the region participated. Nechilibi\'s debate team reached the semi-finals, demonstrating excellent oratory and critical thinking skills on topics including climate change and youth entrepreneurship.</p>'),

            ('School Library Receives 500 New Books',
             '<p>Thanks to a generous donation from a local development organisation, Nechilibi High School\'s library has received 500 new books covering Science, Mathematics, Literature, History and career guidance. The new titles are now available to all students. The school encourages students to make regular use of the library to supplement classroom learning.</p>'),

            ('Career Guidance Day Inspires Form 5 and Form 6 Students',
             '<p>Nechilibi High School hosted a Career Guidance Day for Form 5 and Form 6 students. Professionals from medicine, engineering, law, agriculture and education addressed students about career pathways, university requirements and scholarship opportunities available to Zimbabwean students.</p>'),

            ('School Garden Project Wins District Award',
             '<p>The Nechilibi High School Agriculture Department has won the Gwanda District Best School Garden Award for 2025. The school garden, managed by Form 3 and Form 4 Agriculture students, produces vegetables that supplement the school boarding kitchen. The award recognises innovation, sustainability and student engagement in agriculture.</p>'),

            ('Girls Football Team Qualifies for Provincial Championships',
             '<p>The Nechilibi High School Girls Football Team has qualified for the Matabeleland South Provincial Football Championships after winning all their district fixtures. The team will represent the school at the provincial level. The school congratulates the team and calls on the community to support them.</p>'),

            ('End of Term 1 Report — Academic Performance Update',
             '<p>As Term 1 2026 comes to a close, the school is pleased to report strong academic performance across all forms. Teachers have observed improved attendance, class participation and homework submission rates. Parents are reminded to review their children\'s report cards and attend the upcoming Parents and Teachers Meeting.</p>'),

            ('Nechilibi Launches Environmental Club',
             '<p>Nechilibi High School has launched the Nechilibi Environmental Club, open to all students from Form 1 to Form 6. The club will focus on tree planting, waste management, water conservation and environmental awareness campaigns in the school and surrounding community.</p>'),

            ('Music and Drama Festival — Nechilibi Shines on Stage',
             '<p>Students of Nechilibi High School gave a spectacular performance at the Gwanda District Music and Drama Festival. The school\'s choir placed second in the choral category, while the drama group\'s original play earned special recognition for creativity and social message from the adjudicators.</p>'),

            ('School Fees Reminder — Term 2 2026',
             '<p>The school administration reminds all parents and guardians that Term 2 2026 school fees are due by the first week of term. Parents experiencing financial difficulties are encouraged to contact the school bursar to discuss payment arrangements. The school appreciates the continued support of parents.</p>'),

            ('Nechilibi Participates in National Science Fair',
             '<p>Three Nechilibi High School students represented the school at the National Science Fair held in Harare. The students presented projects on solar energy, water purification and drought-resistant crop varieties. Their projects were praised by judges for their relevance to Zimbabwe\'s development challenges.</p>'),

            ('New Computer Laboratory Enhances ICT Education',
             '<p>Nechilibi High School has commissioned a new Computer Laboratory with 30 workstations, providing students with improved access to ICT education. The lab supports the ZIMSEC ICT curriculum and provides students with internet access for research purposes. Form 3 to Form 6 students will have scheduled ICT lessons starting this term.</p>'),

            ('Alumni Association Donates School Bus',
             '<p>The Nechilibi High School Alumni Association has donated a 30-seater school bus to assist with student transportation for sports events, educational tours and inter-school competitions. The school\'s administration expressed deep gratitude to the alumni for their continued investment in the institution.</p>'),

            ('Form 6 Students Visit University of Zimbabwe',
             '<p>Form 6 students at Nechilibi High School recently visited the University of Zimbabwe in Harare as part of a university awareness programme. Students toured faculties including Medicine, Engineering, Law and Education, and received insights about entry requirements and bursary opportunities.</p>'),

            ('Annual General Meeting — Parents Invited',
             '<p>Nechilibi High School cordially invites all parents and guardians to the Annual General Meeting scheduled for the last Saturday of Term 2. The AGM will cover academic performance, financial statements, development projects and plans for the coming year. A School Development Committee election will also be held.</p>'),

            ('Headmaster\'s Message — Beginning of 2026 Academic Year',
             '<p>On behalf of the entire Nechilibi High School family, the Headmaster warmly welcomes all students, parents and staff to the 2026 academic year. This year we will focus on improving examination results, expanding co-curricular activities and enhancing school infrastructure. Let us work together to make 2026 a year of excellence at Nechilibi High School.</p>'),
        ]

        for title, content in articles_data:
            obj, created = Article.objects.update_or_create(
                title=title,
                defaults={
                    'content': content,
                    'status': 'published',
                    'is_featured': False,
                }
            )
            if (created or not obj.featured_image) and os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    obj.featured_image.save('nechilibi_news.jpg', File(f), save=False)
                    obj.save()
            if created:
                obj.categories.set([cat])
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} article: {title[:60]}')
