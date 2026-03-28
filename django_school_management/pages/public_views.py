from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField, Value
from django_school_management.gallery.models import GalleryCategory, GalleryImage, VideoGallery
from django_school_management.events.models import Event
from django_school_management.downloads.models import DownloadCategory, Download
from django_school_management.institute.models import SchoolSettings, EducationBoard, InstituteProfile
from django_school_management.teachers.models import Teacher, LEADERSHIP_ROLES
from django_school_management.nechilibi.models import Testimonial, SchoolVideo, TermDate, CalendarEvent, ZIMSECResult, FeeStructure, SubjectOffered, NewsletterSubscriber, SportClub
from collections import defaultdict
from django_school_management.notices.models import Notice
from django_school_management.downloads.models import Download
from django_school_management.notices.models import Notice

# Articles app — field names: status, created (TimeStampedModel), featured_image, content, title
try:
    from django_school_management.articles.models import Article
    HAS_ARTICLES = True
except Exception:
    HAS_ARTICLES = False


def home(request):
    settings = SchoolSettings.get()

    # Gallery images for homepage (use gallery app's canonical model)
    carousel_images = GalleryImage.objects.filter(is_featured=True, is_active=True).order_by('order')[:5]
    gallery_images = GalleryImage.objects.filter(is_active=True).order_by('order', '-uploaded_at')[:3]

    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True)

    # School videos (from nechilibi app)
    school_videos = SchoolVideo.objects.filter(is_active=True).order_by('-is_featured', '-uploaded_at')[:6]

    # Recent notices (non-expired)
    today = timezone.now().date()
    recent_notices = Notice.objects.filter(expires_at__gte=today).order_by('-created')[:5]

    context = {
        'settings': settings,
        'school_settings': settings,
        'carousel_images': carousel_images,
        'gallery_images': gallery_images,
        'featured_images': GalleryImage.objects.filter(is_featured=True)[:6],
        'upcoming_events': Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now().date()
        ).order_by('start_date')[:4],
        'latest_news': [],
        'recent_articles': [],
        'videos': [],
        'testimonials': testimonials,
        'school_videos': school_videos,
        'recent_notices': recent_notices,
    }
    # Gallery videos
    try:
        context['videos'] = VideoGallery.objects.filter(is_published=True)[:3]
    except Exception:
        pass
    if HAS_ARTICLES:
        try:
            articles = Article.objects.filter(
                status='published'
            ).order_by('-created')[:3]
            context['latest_news'] = articles
            context['recent_articles'] = articles
        except Exception:
            pass
    # Subject departments for homepage — 4 faculty cards
    _DEPT_META = {
        'science':    {'label': 'Science & Mathematics', 'icon': 'fas fa-flask',      'color': '#1a5276'},
        'arts':       {'label': 'Arts & Humanities',      'icon': 'fas fa-palette',    'color': '#4a0080'},
        'commercial': {'label': 'Commercial & Business',  'icon': 'fas fa-chart-line', 'color': '#7d4e00'},
        'practicals': {'label': 'Practicals & Technical', 'icon': 'fas fa-tools',      'color': '#1a6b2a'},
    }
    _subjects_qs = SubjectOffered.objects.filter(is_active=True).only('name', 'department')
    _dept_groups = defaultdict(list)
    for s in _subjects_qs:
        _dept_groups[s.department].append(s.name)
    homepage_depts = []
    for key in ['science', 'arts', 'commercial', 'practicals']:
        names = _dept_groups.get(key, [])
        meta = _DEPT_META[key]
        homepage_depts.append({
            'key':    key,
            'label':  meta['label'],
            'icon':   meta['icon'],
            'color':  meta['color'],
            'count':  len(names),
            'sample': names[:4],
        })
    context['homepage_depts'] = homepage_depts

    # Leadership teachers for homepage — show 3, headmaster first
    context['leadership_teachers'] = Teacher.objects.filter(
        is_active=True,
        role__in=LEADERSHIP_ROLES
    ).select_related('designation').prefetch_related('subjects').annotate(
        role_order=Case(
            When(role='headmaster', then=Value(0)),
            When(role='deputy', then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('role_order', 'name')[:3]
    return render(request, 'public/home.html', context)


def about(request):
    settings = SchoolSettings.get()
    all_teachers = Teacher.objects.filter(is_active=True).select_related("designation").prefetch_related("subjects").order_by("designation__role", "name")
    institute = InstituteProfile.objects.filter(active=True).first()
    education_boards = EducationBoard.objects.all().order_by('name')
    return render(request, "public/about.html", {
        "settings": settings,
        "school_settings": settings,
        "all_teachers": all_teachers,
        "institute": institute,
        "education_boards": education_boards,
    })


def admissions(request):
    settings = SchoolSettings.get()
    education_boards = EducationBoard.objects.all().order_by('name')
    institute = InstituteProfile.objects.filter(active=True).first()
    return render(request, 'public/admissions.html', {
        'settings': settings,
        'school_settings': settings,
        'education_boards': education_boards,
        'institute': institute,
    })


def gallery(request):
    from django_school_management.gallery.models import GalleryImage as GalleryImg
    categories = GalleryCategory.objects.prefetch_related('images').all()
    uncategorised = GalleryImg.objects.filter(category__isnull=True, is_active=True).order_by('order', '-uploaded_at')
    all_images = GalleryImg.objects.filter(is_active=True).order_by('order', '-uploaded_at')
    videos = VideoGallery.objects.filter(is_published=True).order_by('order')
    return render(request, 'public/gallery.html', {
        'categories': categories,
        'uncategorised': uncategorised,
        'all_images': all_images,
        'videos': videos,
    })


def news_list(request):
    articles = []
    if HAS_ARTICLES:
        try:
            articles = Article.objects.filter(
                status='published'
            ).order_by('-created')
        except Exception:
            pass
    return render(request, 'public/news.html', {'articles': articles})


def downloads_page(request):
    categories = DownloadCategory.objects.prefetch_related('downloads').filter(
        downloads__is_published=True
    ).distinct()
    return render(request, 'public/downloads.html', {'categories': categories})


def events_page(request):
    today = timezone.now().date()
    upcoming = Event.objects.filter(
        is_published=True,
        start_date__gte=today
    ).order_by('start_date')
    past = Event.objects.filter(
        is_published=True,
        start_date__lt=today
    ).order_by('-start_date')[:6]
    return render(request, 'public/events.html', {'upcoming': upcoming, 'past': past})


def contact(request):
    settings = SchoolSettings.get()
    return render(request, 'public/contact.html', {
        'settings': settings,
        'school_settings': settings,
    })


def notices_page(request):
    today = timezone.now().date()
    notices = Notice.objects.filter(expires_at__gte=today).order_by('-created')
    return render(request, 'public/notices.html', {'notices': notices})


def fee_structure(request):
    structures = FeeStructure.objects.filter(is_published=True)
    years = structures.values_list('academic_year', flat=True).order_by('-academic_year')
    selected_year = request.GET.get('year', years[0] if years else None)

    structure = None
    groups = {}
    if selected_year:
        structure = structures.filter(academic_year=selected_year).first()
        if structure:
            for item in structure.items.all():
                groups.setdefault(item.form_group, []).append(item)

    GROUP_ORDER = ['form1_2', 'form3_4', 'form5_6', 'all']
    ordered_groups = {k: groups[k] for k in GROUP_ORDER if k in groups}

    return render(request, 'public/fee_structure.html', {
        'structure': structure,
        'years': years,
        'selected_year': selected_year,
        'groups': ordered_groups,
    })


def sports_cocurriculars(request):
    all_items = SportClub.objects.filter(is_active=True)
    sports  = [x for x in all_items if x.type == 'sport']
    clubs   = [x for x in all_items if x.type == 'club']
    societies = [x for x in all_items if x.type == 'society']
    return render(request, 'public/sports_cocurriculars.html', {
        'sports': sports,
        'clubs': clubs,
        'societies': societies,
        'total': all_items.count(),
    })


def staff_directory(request):
    leadership = Teacher.objects.filter(
        is_active=True, role__in=LEADERSHIP_ROLES
    ).select_related('designation').prefetch_related('subjects').order_by('role', 'name')
    staff = Teacher.objects.filter(
        is_active=True
    ).exclude(role__in=LEADERSHIP_ROLES).select_related('designation').prefetch_related('subjects').order_by('designation__title', 'name')
    return render(request, 'public/staff_directory.html', {
        'leadership': leadership,
        'staff': staff,
        'total': Teacher.objects.filter(is_active=True).count(),
    })


def search(request):
    q = request.GET.get('q', '').strip()
    today = timezone.now().date()
    results_notices   = []
    results_downloads = []
    results_articles  = []
    total = 0

    if q and len(q) >= 2:
        results_notices = list(Notice.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q),
            expires_at__gte=today
        )[:10])
        results_downloads = list(Download.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            is_published=True
        )[:10])
        if HAS_ARTICLES:
            try:
                results_articles = list(Article.objects.filter(
                    Q(title__icontains=q) | Q(content__icontains=q),
                    status='published'
                ).order_by('-created')[:10])
            except Exception:
                pass
        total = len(results_notices) + len(results_downloads) + len(results_articles)

    return render(request, 'public/search.html', {
        'q': q,
        'notices': results_notices,
        'downloads': results_downloads,
        'articles': results_articles,
        'total': total,
    })


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        name  = request.POST.get('name', '').strip()
        next_url = request.POST.get('next', '/')
        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )
            if not created and not obj.is_active:
                obj.is_active = True
                obj.name = name or obj.name
                obj.save()
        return redirect(next_url + '?subscribed=1')
    return redirect('/')


def subjects_offered(request):
    subjects = SubjectOffered.objects.filter(is_active=True)

    # Group by department for display
    departments = {}
    DEPT_ORDER = ['science', 'arts', 'commercial', 'practicals']
    for subj in subjects:
        departments.setdefault(subj.department, []).append(subj)
    ordered_depts = {k: departments[k] for k in DEPT_ORDER if k in departments}

    # Counts for filter tabs
    o_level_count = subjects.filter(level__in=['o_level', 'both']).count()
    a_level_count = subjects.filter(level__in=['a_level', 'both']).count()

    return render(request, 'public/subjects_offered.html', {
        'departments': ordered_depts,
        'all_subjects': subjects,
        'o_level_count': o_level_count,
        'a_level_count': a_level_count,
        'total_count': subjects.count(),
    })


def zimsec_results(request):
    years = ZIMSECResult.objects.filter(is_published=True)\
                .values_list('year', flat=True).distinct().order_by('-year')
    selected_year = request.GET.get('year', years[0] if years else None)

    o_level = None
    a_level = None
    if selected_year:
        o_level = ZIMSECResult.objects.filter(
            year=selected_year, level='o_level', is_published=True
        ).prefetch_related('subjects').first()
        a_level = ZIMSECResult.objects.filter(
            year=selected_year, level='a_level', is_published=True
        ).prefetch_related('subjects').first()

    # All published years for trend chart (ordered oldest→newest)
    trend_data = list(
        ZIMSECResult.objects.filter(is_published=True)
            .order_by('year', 'level')
            .values('year', 'level', 'total_candidates', 'total_passes', 'national_average')
    )

    return render(request, 'public/zimsec_results.html', {
        'years': years,
        'selected_year': selected_year,
        'o_level': o_level,
        'a_level': a_level,
        'trend_data': trend_data,
    })


def academic_calendar(request):
    today = timezone.now().date()
    current_year = str(today.year)

    # Get all years that have term data, sorted descending
    years = TermDate.objects.values_list('academic_year', flat=True).distinct().order_by('-academic_year')
    selected_year = request.GET.get('year', current_year if current_year in list(years) else (years[0] if years else current_year))

    terms = TermDate.objects.filter(academic_year=selected_year).order_by('term')
    events = CalendarEvent.objects.filter(academic_year=selected_year).order_by('date_from')

    # Group events by type for display
    holidays  = events.filter(event_type='holiday')
    exams     = events.filter(event_type='exam')
    sch_events = events.filter(event_type='event')
    other     = events.filter(event_type='other')

    return render(request, 'public/academic_calendar.html', {
        'terms': terms,
        'all_events': events,
        'holidays': holidays,
        'exams': exams,
        'sch_events': sch_events,
        'other': other,
        'years': years,
        'selected_year': selected_year,
        'today': today,
    })
