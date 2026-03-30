from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Visitor

def index(request):
    return redirect('visitor_form')

def visitor_form(request):
    if request.method == "POST":
        visitor = Visitor.objects.create(
            full_name=request.POST.get('full_name'),
            document_type=request.POST.get('document_type'),
            document_number=request.POST.get('document_number'),
            organization=request.POST.get('organization'),
            escort_id=request.POST.get('escort')
        )
        
        visitor.valid_until = visitor.created_at + timedelta(hours=8)
        visitor.save()
        
        return redirect('request_success')
    
    escorts = Visitor.objects.filter(status='approved')
    return render(request, 'core/visitor_form.html', {'escorts': escorts})

def dashboard(request):
    visitors = Visitor.objects.all().order_by('-created_at')
    return render(request, 'core/dashboard.html', {'visitors': visitors})

def dashboard_partial(request):
    tab = request.GET.get('tab', 'active')
    visitors = Visitor.objects.all().order_by('-created_at')
    
    if tab == 'archive':
        template_name = 'core/dashboard_partial_archive.html'
    else:
        template_name = 'core/dashboard_partial_active.html'
    
    return render(request, template_name, {'visitors': visitors})

def approve_visitor(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    
    if visitor.status == 'pending':
        visitor.status = 'approved'
        visitor.arrival_time = timezone.now()
        visitor.save()
    
    return redirect('dashboard')

def mark_departed(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if visitor.status == 'approved':
        visitor.status = 'departed'
        visitor.departure_time = timezone.now()
        visitor.save()
    return redirect('dashboard')

def request_success(request):
    return render(request, 'core/success.html')
