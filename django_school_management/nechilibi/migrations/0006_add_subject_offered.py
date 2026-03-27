from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nechilibi', '0005_add_fee_structure'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectOffered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.CharField(
                    choices=[('o_level', 'O-Level (Form 1–4)'), ('a_level', 'A-Level (Form 5–6)'), ('both', 'O-Level & A-Level')],
                    default='o_level', max_length=10)),
                ('department', models.CharField(
                    choices=[('languages', 'Languages'), ('sciences', 'Sciences'), ('mathematics', 'Mathematics'),
                             ('humanities', 'Humanities'), ('commercial', 'Commercial & Business'),
                             ('technical', 'Technical & Practical'), ('arts', 'Arts & Creative'), ('other', 'Other')],
                    default='other', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Brief description shown on the page')),
                ('icon', models.CharField(blank=True, default='fas fa-book', help_text='FontAwesome class e.g. fas fa-flask', max_length=60)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Subject Offered',
                'verbose_name_plural': 'Subjects Offered',
                'ordering': ['department', 'order', 'name'],
            },
        ),
    ]
