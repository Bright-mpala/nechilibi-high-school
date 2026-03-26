# curriculum app removed — this migration is now a no-op

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0015_educationboard'),
    ]

    operations = [
        # curriculum FK removed (curriculum app not used)
    ]
