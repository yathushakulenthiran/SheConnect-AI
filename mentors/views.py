from django.shortcuts import render, get_object_or_404
from .models import Mentor


def mentor_list(request):
    """Public mentor directory"""
    mentors = Mentor.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by availability
    availability = request.GET.get('availability', '')
    if availability:
        mentors = mentors.filter(availability_status=availability)
    
    # Filter by industry
    industry = request.GET.get('industry', '')
    if industry:
        mentors = mentors.filter(industry__icontains=industry)
    
    context = {
        'mentors': mentors,
        'availability_filter': availability,
        'industry_filter': industry,
    }
    return render(request, 'mentors/mentor_list.html', context)


def mentor_detail(request, mentor_id):
    """Individual mentor profile"""
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True)
    
    context = {
        'mentor': mentor,
    }
    return render(request, 'mentors/mentor_detail.html', context)
