import os
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import GalleryImage, SchoolSettings


class Command(BaseCommand):
    help = 'Seed initial gallery images and school settings'

    def handle(self, *args, **kwargs):
        # Create school settings
        if not SchoolSettings.objects.exists():
            SchoolSettings.objects.create(
                school_name='Nechilibi High School',
                tagline='Excellence in Education',
                address='Nechilibi, Matabeleland South, Zimbabwe',
                email='info@nechilibi.ac.zw',
            )
            self.stdout.write(self.style.SUCCESS('Created school settings'))

        # Seed gallery from media/gallery folder
        from django.conf import settings as django_settings
        gallery_dir = os.path.join(django_settings.MEDIA_ROOT, 'gallery')
        if os.path.exists(gallery_dir):
            files = [f for f in os.listdir(gallery_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            files.sort()
            for i, filename in enumerate(files[:10]):  # max 10
                rel_path = f'gallery/{filename}'
                title = filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title()
                obj, created = GalleryImage.objects.get_or_create(
                    image=rel_path,
                    defaults={
                        'title': title,
                        'is_carousel': i < 5,  # first 5 are carousel
                        'carousel_order': i,
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(f'  Added: {filename}')
        self.stdout.write(self.style.SUCCESS('Gallery seeded successfully!'))
