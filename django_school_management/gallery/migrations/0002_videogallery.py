from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('youtube_url', models.URLField(help_text='YouTube video URL')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='videos/')),
                ('description', models.TextField(blank=True)),
                ('is_published', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
