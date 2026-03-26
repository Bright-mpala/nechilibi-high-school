from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0016_instituteprofile_curriculum'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(default='Nechilibi High School', max_length=200)),
                ('tagline', models.CharField(blank=True, default='Excellence in Education', max_length=300)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, default='info@nechilibi.ac.zw', max_length=254)),
                ('address', models.TextField(blank=True, default='P.O. Box 123, Nechilibi, Matabeleland South, Zimbabwe')),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=30)),
                ('hero_heading', models.CharField(blank=True, default="Shaping Tomorrow's Leaders Today", max_length=200)),
                ('hero_subheading', models.TextField(blank=True, default='Nechilibi High School provides quality secondary education from Form 1 to Form 6.')),
                ('about_text', models.TextField(blank=True)),
                ('total_students', models.PositiveIntegerField(default=500)),
                ('total_teachers', models.PositiveIntegerField(default=40)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='school/')),
                ('hero_background', models.ImageField(blank=True, null=True, upload_to='school/')),
            ],
            options={
                'verbose_name': 'School Settings',
                'verbose_name_plural': 'School Settings',
            },
        ),
    ]
