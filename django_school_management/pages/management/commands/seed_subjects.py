"""
Seed subjects offered at Nechilibi High School.
Organised into four faculties: Science, Arts, Commercial, Practicals.
Safe to re-run — clears and recreates all subjects each time.
"""
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import SubjectOffered

SUBJECTS = [
    # ══════════════════════════════════════════════════════
    # SCIENCE & MATHEMATICS
    # ══════════════════════════════════════════════════════
    dict(name='Mathematics',
         level='o_level', department='science',
         icon='fas fa-calculator',
         description='Number, algebra, geometry, statistics and problem solving for Form 1–4.',
         order=1),
    dict(name='Additional Mathematics',
         level='o_level', department='science',
         icon='fas fa-superscript',
         description='Extended O-Level mathematics for high-achieving students.',
         order=2),
    dict(name='Pure Mathematics',
         level='a_level', department='science',
         icon='fas fa-infinity',
         description='Calculus, algebra, trigonometry and proof at A-Level.',
         order=3),
    dict(name='Statistics',
         level='a_level', department='science',
         icon='fas fa-chart-bar',
         description='Probability, statistical inference and data analysis at A-Level.',
         order=4),
    dict(name='Combined Science',
         level='o_level', department='science',
         icon='fas fa-atom',
         description='Foundations of Biology, Chemistry and Physics for Form 1–4.',
         order=5),
    dict(name='Biology',
         level='both', department='science',
         icon='fas fa-dna',
         description='Life processes, ecology, genetics and human biology — O-Level & A-Level.',
         order=6),
    dict(name='Chemistry',
         level='both', department='science',
         icon='fas fa-flask',
         description='Atomic structure, reactions, organic chemistry and analysis — O-Level & A-Level.',
         order=7),
    dict(name='Physics',
         level='both', department='science',
         icon='fas fa-bolt',
         description='Mechanics, waves, electricity, magnetism and modern physics — O-Level & A-Level.',
         order=8),
    dict(name='Computer Science',
         level='both', department='science',
         icon='fas fa-laptop-code',
         description='Programming, networking, databases and digital literacy — O-Level & A-Level.',
         order=9),

    # ══════════════════════════════════════════════════════
    # ARTS & HUMANITIES
    # ══════════════════════════════════════════════════════
    dict(name='English Language',
         level='o_level', department='arts',
         icon='fas fa-pen-nib',
         description='Core communication skills, comprehension and composition.',
         order=1),
    dict(name='English Literature',
         level='a_level', department='arts',
         icon='fas fa-book-open',
         description='In-depth study of prose, poetry and drama texts at A-Level.',
         order=2),
    dict(name='Ndebele Language',
         level='both', department='arts',
         icon='fas fa-comments',
         description='Reading, writing and oral communication in isiNdebele — O-Level & A-Level.',
         order=3),
    dict(name='Shona Language',
         level='o_level', department='arts',
         icon='fas fa-comments',
         description='Reading, writing and oral communication in ChiShona.',
         order=4),
    dict(name='History',
         level='both', department='arts',
         icon='fas fa-landmark',
         description='Zimbabwean, African and world history from 1890 to the present.',
         order=5),
    dict(name='Geography',
         level='both', department='arts',
         icon='fas fa-globe-africa',
         description='Physical and human geography with fieldwork components.',
         order=6),
    dict(name='Religious Studies',
         level='both', department='arts',
         icon='fas fa-pray',
         description='Comparative religion, ethics and moral reasoning.',
         order=7),
    dict(name='Divinity',
         level='a_level', department='arts',
         icon='fas fa-bible',
         description='Biblical studies and Christian theology at A-Level.',
         order=8),
    dict(name='Art & Design',
         level='both', department='arts',
         icon='fas fa-palette',
         description='Drawing, painting, sculpture and design principles.',
         order=9),
    dict(name='Music',
         level='o_level', department='arts',
         icon='fas fa-music',
         description='Music theory, performance and Zimbabwean musical heritage.',
         order=10),

    # ══════════════════════════════════════════════════════
    # COMMERCIAL & BUSINESS
    # ══════════════════════════════════════════════════════
    dict(name='Commerce',
         level='o_level', department='commercial',
         icon='fas fa-store',
         description='Business environment, trade, banking and commerce principles at O-Level.',
         order=1),
    dict(name='Accounts',
         level='o_level', department='commercial',
         icon='fas fa-file-invoice-dollar',
         description='Book-keeping, final accounts and basic accounting principles at O-Level.',
         order=2),
    dict(name='Accounting',
         level='a_level', department='commercial',
         icon='fas fa-file-invoice-dollar',
         description='Financial and management accounting at A-Level.',
         order=3),
    dict(name='Business Studies',
         level='a_level', department='commercial',
         icon='fas fa-briefcase',
         description='Business operations, marketing, HR and strategy at A-Level.',
         order=4),
    dict(name='Economics',
         level='a_level', department='commercial',
         icon='fas fa-chart-line',
         description='Micro and macroeconomics, development and policy at A-Level.',
         order=5),

    # ══════════════════════════════════════════════════════
    # PRACTICALS & TECHNICAL
    # ══════════════════════════════════════════════════════
    dict(name='Agriculture',
         level='both', department='practicals',
         icon='fas fa-seedling',
         description='Crop production, animal husbandry and agri-business with practical fieldwork.',
         order=1),
    dict(name='Home Economics',
         level='o_level', department='practicals',
         icon='fas fa-utensils',
         description='Food science, nutrition, textiles and household management.',
         order=2),
    dict(name='Technical Graphics',
         level='o_level', department='practicals',
         icon='fas fa-drafting-compass',
         description='Technical drawing, orthographic projection and design.',
         order=3),
    dict(name='Wood Technology',
         level='o_level', department='practicals',
         icon='fas fa-hammer',
         description='Woodcraft, joinery and construction technology.',
         order=4),
    dict(name='Fashion & Fabrics',
         level='o_level', department='practicals',
         icon='fas fa-cut',
         description='Garment construction, textile science and fashion design.',
         order=5),
    dict(name='Physical Education',
         level='o_level', department='practicals',
         icon='fas fa-running',
         description='Sport, fitness and health education.',
         order=6),
]


class Command(BaseCommand):
    help = 'Seed subjects offered at Nechilibi High School (clears existing and recreates)'

    def handle(self, *args, **options):
        deleted, _ = SubjectOffered.objects.all().delete()
        if deleted:
            self.stdout.write(f'  Cleared {deleted} existing subjects.')

        for data in SUBJECTS:
            SubjectOffered.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(
            f'Subjects seeded OK. Total: {len(SUBJECTS)} '
            f'({sum(1 for s in SUBJECTS if s["department"] == "science")} Science, '
            f'{sum(1 for s in SUBJECTS if s["department"] == "arts")} Arts, '
            f'{sum(1 for s in SUBJECTS if s["department"] == "commercial")} Commercial, '
            f'{sum(1 for s in SUBJECTS if s["department"] == "practicals")} Practicals)'
        ))
