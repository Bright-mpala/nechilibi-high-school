"""
Seed subjects offered at Nechilibi High School.
Safe to run multiple times — skips if subjects already exist.
"""
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import SubjectOffered

SUBJECTS = [
    # ── Languages ────────────────────────────────────────────────
    dict(name='English Language',      level='o_level', department='languages', icon='fas fa-pen-nib',    description='Core communication skills, comprehension, and composition.', order=1),
    dict(name='English Literature',    level='a_level', department='languages', icon='fas fa-book',       description='In-depth study of prose, poetry, and drama texts.', order=2),
    dict(name='Ndebele Language',      level='both',    department='languages', icon='fas fa-comments',   description='Reading, writing, and oral communication in isiNdebele.', order=3),
    dict(name='Shona Language',        level='o_level', department='languages', icon='fas fa-comments',   description='Reading, writing, and oral communication in ChiShona.', order=4),

    # ── Mathematics ──────────────────────────────────────────────
    dict(name='Mathematics',           level='o_level', department='mathematics', icon='fas fa-calculator', description='Number, algebra, geometry, statistics, and problem solving.', order=1),
    dict(name='Additional Mathematics',level='o_level', department='mathematics', icon='fas fa-superscript', description='Extended topics for high-achieving O-Level mathematics students.', order=2),
    dict(name='Pure Mathematics',      level='a_level', department='mathematics', icon='fas fa-infinity',   description='Calculus, algebra, trigonometry, and proof at A-Level.', order=3),
    dict(name='Statistics',            level='a_level', department='mathematics', icon='fas fa-chart-bar',  description='Probability, statistical inference, and data analysis.', order=4),

    # ── Sciences ─────────────────────────────────────────────────
    dict(name='Combined Science',      level='o_level', department='sciences', icon='fas fa-atom',         description='Foundations of biology, chemistry, and physics.', order=1),
    dict(name='Biology',               level='both',    department='sciences', icon='fas fa-dna',           description='Life processes, ecology, genetics, and human biology.', order=2),
    dict(name='Chemistry',             level='both',    department='sciences', icon='fas fa-flask',         description='Atomic structure, reactions, organic chemistry, and analysis.', order=3),
    dict(name='Physics',               level='both',    department='sciences', icon='fas fa-bolt',          description='Mechanics, waves, electricity, magnetism, and modern physics.', order=4),
    dict(name='Agriculture',           level='both',    department='sciences', icon='fas fa-seedling',      description='Crop production, animal husbandry, and agri-business.', order=5),

    # ── Humanities ───────────────────────────────────────────────
    dict(name='History',               level='both',    department='humanities', icon='fas fa-landmark',    description='Zimbabwean, African, and world history from 1890 to present.', order=1),
    dict(name='Geography',             level='both',    department='humanities', icon='fas fa-globe-africa', description='Physical and human geography with fieldwork components.', order=2),
    dict(name='Religious Studies',     level='both',    department='humanities', icon='fas fa-pray',         description='Comparative religion, ethics, and moral reasoning.', order=3),
    dict(name='Divinity',              level='a_level', department='humanities', icon='fas fa-bible',        description='Biblical studies and Christian theology at A-Level.', order=4),

    # ── Commercial & Business ────────────────────────────────────
    dict(name='Commerce',              level='o_level', department='commercial', icon='fas fa-store',        description='Business environment, trade, banking, and commerce principles.', order=1),
    dict(name='Accounts',              level='o_level', department='commercial', icon='fas fa-file-invoice-dollar', description='Book-keeping, final accounts, and basic accounting principles.', order=2),
    dict(name='Accounting',            level='a_level', department='commercial', icon='fas fa-file-invoice-dollar', description='Financial and management accounting at A-Level.', order=3),
    dict(name='Business Studies',      level='a_level', department='commercial', icon='fas fa-briefcase',    description='Business operations, marketing, HR, and strategy.', order=4),
    dict(name='Economics',             level='a_level', department='commercial', icon='fas fa-chart-line',   description='Micro and macroeconomics, development, and policy.', order=5),

    # ── Technical & Practical ────────────────────────────────────
    dict(name='Computer Science',      level='both',    department='technical', icon='fas fa-laptop-code',   description='Programming, networking, databases, and digital literacy.', order=1),
    dict(name='Home Economics',        level='o_level', department='technical', icon='fas fa-utensils',      description='Food science, nutrition, textiles, and household management.', order=2),
    dict(name='Technical Graphics',    level='o_level', department='technical', icon='fas fa-drafting-compass', description='Technical drawing, orthographic projection, and design.', order=3),
    dict(name='Wood Technology',       level='o_level', department='technical', icon='fas fa-hammer',        description='Woodcraft, joinery, and construction technology.', order=4),

    # ── Arts & Creative ──────────────────────────────────────────
    dict(name='Art & Design',          level='both',    department='arts', icon='fas fa-palette',            description='Drawing, painting, sculpture, and design principles.', order=1),
    dict(name='Music',                 level='o_level', department='arts', icon='fas fa-music',              description='Music theory, performance, and Zimbabwean musical heritage.', order=2),
    dict(name='Physical Education',    level='o_level', department='arts', icon='fas fa-running',            description='Sport, fitness, and health education.', order=3),
]


class Command(BaseCommand):
    help = 'Seed subjects offered at Nechilibi High School'

    def handle(self, *args, **options):
        if SubjectOffered.objects.exists():
            self.stdout.write(self.style.WARNING('Subjects already seeded — skipping.'))
            return

        for data in SUBJECTS:
            SubjectOffered.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(SUBJECTS)} subjects.'))
