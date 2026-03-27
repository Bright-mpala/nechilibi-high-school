from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nechilibi', '0007_add_newsletter_subscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(
                    choices=[('sport', 'Sport'), ('club', 'Club'), ('society', 'Society')],
                    default='sport', max_length=10)),
                ('description', models.TextField(blank=True)),
                ('achievements', models.TextField(blank=True, help_text='Notable achievements, trophies, league titles etc.')),
                ('icon', models.CharField(blank=True, default='fas fa-trophy',
                    help_text='FontAwesome class e.g. fas fa-futbol', max_length=60)),
                ('image', models.ImageField(blank=True, null=True, upload_to='sports/')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Sport / Club',
                'verbose_name_plural': 'Sports & Clubs',
                'ordering': ['type', 'order', 'name'],
            },
        ),
    ]
