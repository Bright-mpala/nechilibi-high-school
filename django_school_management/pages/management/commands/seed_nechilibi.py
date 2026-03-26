"""
Management command to seed initial Nechilibi High School data.
Run once after first migration:  python manage.py seed_nechilibi
"""
from django.core.management.base import BaseCommand

from django_school_management.pages.models import (
    SocialMediaLink, SchoolHighlight, HeroBanner,
)
from django_school_management.academics.models import (
    AcademicSession, Semester, Department,
)


class Command(BaseCommand):
    help = 'Seed initial data for Nechilibi High School'

    def handle(self, *args, **options):
        self._seed_social_links()
        self._seed_highlights()
        self._seed_academic_data()
        self.stdout.write(self.style.SUCCESS('Nechilibi data seeded successfully.'))

    def _seed_social_links(self):
        links = [
            ('facebook', 'https://www.facebook.com/nechilibihighschool'),
            ('twitter', 'https://twitter.com/nechilibihs'),
            ('youtube', 'https://www.youtube.com/@nechilibihighschool'),
            ('whatsapp', 'https://wa.me/263771234567'),
        ]
        for platform, url in links:
            SocialMediaLink.objects.get_or_create(
                platform=platform, defaults={'url': url, 'is_active': True}
            )
        self.stdout.write('  Social media links seeded.')

    def _seed_highlights(self):
        highlights = [
            ('fas fa-user-graduate', '1200+', 'Students Enrolled', 0),
            ('fas fa-chalkboard-teacher', '80+', 'Qualified Teachers', 1),
            ('fas fa-trophy', '98%', 'ZIMSEC Pass Rate', 2),
            ('fas fa-calendar-alt', '1962', 'Year Established', 3),
        ]
        for icon, value, label, order in highlights:
            SchoolHighlight.objects.get_or_create(
                label=label,
                defaults={'icon_class': icon, 'value': value, 'order': order}
            )
        self.stdout.write('  School highlights seeded.')

    def _seed_academic_data(self):
        # Academic session
        session, _ = AcademicSession.objects.get_or_create(year=2025)

        # Forms (1-6) stored as Semesters
        for form_number in range(1, 7):
            Semester.objects.get_or_create(number=form_number)

        # Default departments
        for dept_name, short, code in [
            ('Sciences', 'SCI', 1),
            ('Humanities & Arts', 'HUM', 2),
            ('Commercial', 'COM', 3),
        ]:
            Department.objects.get_or_create(
                name=dept_name,
                defaults={'short_name': short, 'code': code}
            )
        self.stdout.write('  Academic data seeded (session, forms, departments).')
