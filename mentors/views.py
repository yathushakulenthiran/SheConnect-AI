from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Mentor
from django.core.paginator import Paginator
from mentees.models import ConnectionRequest


def mentor_list(request):
    """Public mentor directory with advanced filtering"""
    mentors_qs = Mentor.objects.filter(is_active=True, is_verified=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        mentors_qs = mentors_qs.filter(
            Q(name__icontains=search_query) |
            Q(expertise__icontains=search_query) |
            Q(industry__icontains=search_query) |
            Q(short_bio__icontains=search_query)
        )
    
    # Filter by availability
    availability = request.GET.get('availability', '')
    if availability:
        mentors_qs = mentors_qs.filter(availability_status=availability)
    
    # Filter by industry
    industry = request.GET.get('industry', '')
    if industry:
        mentors_qs = mentors_qs.filter(industry__icontains=industry)
    
    # Filter by business stage expertise
    business_stage = request.GET.get('business_stage', '')
    if business_stage:
        mentors_qs = mentors_qs.filter(business_stage_expertise=business_stage)

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(mentors_qs, 9)
    mentors = paginator.get_page(page_number)
    
    # Get unique industries for filter dropdown
    industries = Mentor.objects.filter(is_active=True).values_list('industry', flat=True).distinct()
    
    context = {
        'mentors': mentors,
        'paginator': paginator,
        'search_query': search_query,
        'availability_filter': availability,
        'industry_filter': industry,
        'business_stage_filter': business_stage,
        'industries': industries,
        'availability_choices': Mentor._meta.get_field('availability_status').choices,
        'business_stage_choices': Mentor._meta.get_field('business_stage_expertise').choices,
    }
    return render(request, 'mentors/mentor_list.html', context)


def mentor_detail(request, mentor_id):
    """Individual mentor profile"""
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True)
    
    # Check connection status for authenticated mentees
    connection_status = None
    if request.user.is_authenticated:
        try:
            mentee = request.user.mentee_profile
            connection = ConnectionRequest.objects.filter(
                mentee=mentee,
                mentor=mentor
            ).first()
            if connection:
                connection_status = connection.status
        except:
            pass
    
    context = {
        'mentor': mentor,
        'connection_status': connection_status,
    }
    return render(request, 'mentors/mentor_detail.html', context)
