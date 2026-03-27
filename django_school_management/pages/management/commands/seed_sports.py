"""
Seed sports teams, clubs, and societies for Nechilibi High School.
Safe to run multiple times — skips if data already exists.
"""
from django.core.management.base import BaseCommand
from django_school_management.nechilibi.models import SportClub

SPORTS_DATA = [
    # ── Sports ────────────────────────────────────────────────────
    dict(type='sport', name='Football (Boys)',    icon='fas fa-futbol',       order=1,
         description='Our boys football team competes in the Matabeleland South Schools League, fielding teams at both junior and senior levels.',
         achievements='Matabeleland South Regional Runners-Up 2023\nDistrict Champions 2022\nRegional Quarter-Finals 2024'),

    dict(type='sport', name='Netball (Girls)',    icon='fas fa-circle',       order=2,
         description='The girls netball team is one of the school\'s strongest performing sides, competing at provincial level.',
         achievements='Provincial Champions 2023\nNational Schools Tournament Participants 2023\nDistrict Champions 2022 & 2024'),

    dict(type='sport', name='Athletics',          icon='fas fa-running',      order=3,
         description='Track and field events including sprints, middle distance, long jump, and relay. Students represent the school at district and provincial meets.',
         achievements='District Athletics Gala — Multiple Gold Medals 2023 & 2024\nProvincial Representative Athletes'),

    dict(type='sport', name='Basketball',         icon='fas fa-basketball-ball', order=4,
         description='Mixed basketball programme open to Form 3–6 students. Training sessions held three times a week on the school court.',
         achievements='District Basketball Tournament Semi-Finalists 2024'),

    dict(type='sport', name='Volleyball',         icon='fas fa-volleyball-ball', order=5,
         description='Both boys and girls volleyball teams compete in inter-school competitions across the district.',
         achievements='District Volleyball League Runners-Up 2023'),

    dict(type='sport', name='Cricket',            icon='fas fa-baseball-ball', order=6,
         description='Cricket is offered during the summer term for students in all forms. The school fields a competitive side in district fixtures.',
         achievements='District Cricket League Participants 2022–2024'),

    dict(type='sport', name='Chess',              icon='fas fa-chess',        order=7,
         description='Competitive chess played at inter-school and district level. Open to all students with regular after-school coaching sessions.',
         achievements='District Chess Olympiad — Top 3 Finishes (2022, 2023, 2024)'),

    # ── Clubs ─────────────────────────────────────────────────────
    dict(type='club', name='Debating Club',        icon='fas fa-comments',    order=1,
         description='Students develop public speaking, critical thinking, and argumentation skills through weekly debates and inter-school competitions.',
         achievements='Matabeleland South Schools Debating Champions 2023\nNational Debating Finals Participants 2024'),

    dict(type='club', name='Science Club',         icon='fas fa-flask',       order=2,
         description='Hands-on experiments, science fairs, and guest lectures. Open to all science students with a curiosity beyond the classroom.',
         achievements='Zimbabwe National Science Fair — Regional Representatives 2023'),

    dict(type='club', name='Environmental Club',   icon='fas fa-leaf',        order=3,
         description='Tree planting, conservation projects, and environmental awareness campaigns within the school and local community.',
         achievements='School Garden Initiative\nRegional Environmental Awareness Award 2022'),

    dict(type='club', name='Drama Club',           icon='fas fa-theater-masks', order=4,
         description='Annual school play, cultural performances, and participation in inter-school drama festivals. All forms welcome.',
         achievements='Annual School Drama Festival — Best Performance 2023'),

    dict(type='club', name='Computer Club',        icon='fas fa-laptop-code',  order=5,
         description='Programming, graphic design, and IT projects beyond the curriculum. Students build websites, apps, and multimedia content.',
         achievements='District ICT Competition Finalists 2024'),

    dict(type='club', name='Agriculture Club',     icon='fas fa-seedling',    order=6,
         description='Practical farming, crop management, and agri-business projects on the school farm. Closely linked to the Agriculture curriculum.',
         achievements='Best School Farm Award — District 2022'),

    # ── Societies ─────────────────────────────────────────────────
    dict(type='society', name='Student Council',   icon='fas fa-users-cog',   order=1,
         description='The elected student representative body that voices student concerns, organises school events, and liaises with school management.',
         achievements='Spearheaded the School Beautification Project 2023\nAnnual Charity Drive organisers'),

    dict(type='society', name='Christian Union',   icon='fas fa-cross',       order=2,
         description='Weekly devotional meetings, prayer, and community outreach. Open to all students regardless of denomination.',
         achievements='Annual Carol Service organisers\nCommunity Outreach Programme'),

    dict(type='society', name='Young Entrepreneurs Society', icon='fas fa-chart-line', order=3,
         description='Business simulations, entrepreneurship workshops, and business plan competitions to prepare students for the real world.',
         achievements='Business Plan Competition Winners — District 2024'),

    dict(type='society', name='Prefect Body',      icon='fas fa-shield-alt',  order=4,
         description='Senior students elected to leadership roles supporting school discipline, mentoring younger students, and representing the school at official events.',
         achievements='Annual Prefects\' Leadership Camp\nStudent Mentorship Programme'),
]


class Command(BaseCommand):
    help = 'Seed sports teams, clubs, and societies for Nechilibi High School'

    def handle(self, *args, **options):
        if SportClub.objects.exists():
            self.stdout.write(self.style.WARNING('Sports & clubs already seeded — skipping.'))
            return

        for data in SPORTS_DATA:
            SportClub.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(SPORTS_DATA)} sports/clubs/societies.'))
