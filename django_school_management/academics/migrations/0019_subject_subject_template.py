# curriculum app removed — this migration is now a no-op

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0018_department_institute'),
    ]

    operations = [
        # subject_template FK removed (curriculum app not used)
    ]
