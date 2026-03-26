from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='DownloadCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name_plural': 'Download Categories', 'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downloads', to='downloads.downloadcategory')),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='downloads/')),
                ('description', models.TextField(blank=True)),
                ('is_published', models.BooleanField(default=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-uploaded_at']},
        ),
    ]
