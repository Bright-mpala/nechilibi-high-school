from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nechilibi', '0006_add_subject_offered'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Newsletter Subscriber',
                'verbose_name_plural': 'Newsletter Subscribers',
                'ordering': ['-subscribed_at'],
            },
        ),
    ]
