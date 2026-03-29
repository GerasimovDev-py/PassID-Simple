from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Visitor

def index(request):
    return redirect('visitor_form')

def visitor_form(request):
    if request.method == "POST":
        Visitor.objects.create(
            full_name=request.POST.get('full_name'),
            passport=request.POST.get('passport'),
            phone=request.POST.get('phone'),
            organization=request.POST.get('organization'),
            escort_id=request.POST.get('escort') or None
        )   
        return redirect('request_success')
    
    escorts = Visitor.objects.filter(status='approved')
    return render(request, 'core/visitor_form.html', {'escorts': escorts})

def dashboard(request):
    visitors = Visitor.objects.all().order_by('-created_at')
    return render(request, 'core/dashboard.html', {'visitors': visitors})

def dashboard_partial(request):
    visitors = Visitor.objects.all().order_by('-created_at')
    return render(request, 'core/dashboard_partial.html', {'visitors': visitors})

def approve_visitor(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    visitor.status = 'approved'
    visitor.save()
    return redirect('dashboard')

def request_success(request):
    return render(request, 'core/success.html')
