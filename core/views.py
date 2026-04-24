from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Visitor, Profile
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


def main_choice(request):
    """Главная страница с двумя кнопками"""
    return render(request, 'core/main_choice.html')

@staff_member_required
def admin_access(request):
    """Админ панель - управление ответственными"""
    responsibles = Profile.objects.filter(is_responsible=True).select_related('user')
    return render(request, 'core/admin_access.html', {'responsibles': responsibles})


@staff_member_required
def admin_add_responsible(request):
    """Добавление нового ответственного"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Пользователь с логином "{username}" уже существует!')
            return redirect('admin_access')
        
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        Profile.objects.create(
            user=user,
            is_responsible=True,
            responsible_full_name=full_name,
            responsible_phone=phone,
            kpp=None
        )
        
        messages.success(request, f'Ответственный "{full_name}" успешно добавлен!')
        return redirect('admin_access')
    
    return render(request, 'core/admin_add_responsible.html')


@staff_member_required
def admin_edit_responsible(request, user_id):
    """Редактирование ответственного"""
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        if not profile.is_responsible:
            messages.error(request, 'Этот пользователь не является ответственным')
            return redirect('admin_access')
    except:
        messages.error(request, 'Пользователь не найден')
        return redirect('admin_access')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, f'Пользователь с логином "{username}" уже существует!')
            return redirect('admin_edit_responsible', user_id=user_id)
        
        user.username = username
        if password:
            user.set_password(password)
        user.save()
        
        profile.responsible_full_name = full_name
        profile.responsible_phone = phone
        profile.save()
        
        messages.success(request, f'Данные ответственного "{full_name}" обновлены!')
        return redirect('admin_access')
    
    return render(request, 'core/admin_edit_responsible.html', {
        'user': user,
        'profile': profile
    })


@staff_member_required
def admin_delete_responsible(request, user_id):
    """Удаление ответственного"""
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        if profile.is_responsible:
            full_name = profile.responsible_full_name
            user.delete()
            messages.success(request, f'Ответственный "{full_name}" удалён!')
        else:
            messages.error(request, 'Этот пользователь не является ответственным')
    except:
        messages.error(request, 'Пользователь не найден')
    
    return redirect('admin_access')

def admin_logout(request):
    """Выход из админ-панели"""
    logout(request)
    request.session.flush()
    return redirect('main_choice')

def responsible_login(request):
    """Логин для ответственного"""
    if request.user.is_authenticated:
        return redirect('responsible_kpp_choice')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = user.profile
                if profile.is_responsible:
                    login(request, user)
                    return redirect('responsible_kpp_choice')
                else:
                    messages.error(request, 'Этот пользователь не зарегистрирован как ответственный')
            except:
                messages.error(request, 'Профиль не найден')
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'core/responsible_login.html')


def responsible_kpp_choice(request):
    """Выбор КПП для ответственного (после логина)"""
    if not request.user.is_authenticated:
        return redirect('responsible_login')
    
    try:
        profile = request.user.profile
        if not profile.is_responsible:
            messages.error(request, 'Доступ только для ответственных лиц')
            return redirect('main_choice')
    except:
        messages.error(request, 'Профиль не найден')
        return redirect('main_choice')
    
    kpp = request.GET.get('kpp')
    if kpp in ['kpp1', 'kpp2']:
        return redirect(f"{reverse('visitor_form_responsible')}?kpp={kpp}")
    
    return render(request, 'core/kpp_choice_responsible.html')

def visitor_form_responsible(request):
    """Форма оформления пропуска для ответственного"""
    if not request.user.is_authenticated:
        return redirect('responsible_login')
    
    try:
        profile = request.user.profile
        if not profile.is_responsible:
            messages.error(request, 'Доступ только для ответственных лиц')
            return redirect('main_choice')
    except:
        messages.error(request, 'Профиль не найден')
        return redirect('main_choice')

    kpp = request.GET.get('kpp')
    
    if not kpp:
        return redirect('responsible_kpp_choice')

    if request.method == "POST":
        try:
            valid_date_str = request.POST.get('valid_date')
            valid_date = datetime.strptime(valid_date_str, "%d.%m.%Y")
            valid_until = datetime(valid_date.year, valid_date.month, valid_date.day, 23, 59, 59)
        except ValueError:
            messages.error(request, "Неверный формат даты")
            return redirect(request.get_full_path())

        visitor = Visitor.objects.create(
            full_name=request.POST.get('full_name'),
            document_type='car_plate',
            document_number=request.POST.get('document_number'),
            escort_name=profile.responsible_full_name,
            escort_phone=profile.responsible_phone,
            valid_until=valid_until,
            kpp=kpp,
            comment=request.POST.get('comment')
        )
        visitor.save()
        
        logout(request)
        request.session.flush()
        
        return redirect('main_choice')
    
    return render(request, 'core/visitor_form_responsible.html', {
        'kpp': kpp,
        'responsible_name': profile.responsible_full_name,
        'responsible_phone': profile.responsible_phone
    })

def staff_login(request):
    """Логин для сотрудника охраны"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.flush()

            if username == 'KPP-1':
                request.session['kpp_access'] = 'kpp1'
                request.session['kpp_name'] = 'КПП-1'
            elif username == 'KPP-2':
                request.session['kpp_access'] = 'kpp2'
                request.session['kpp_name'] = 'КПП-2'
            else:
                request.session['kpp_access'] = 'kpp1'
                request.session['kpp_name'] = 'КПП-1'

            request.session.save()
            
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'core/staff_login.html')

def dashboard(request):
    """Панель охраны"""
    kpp = request.session.get('kpp_access')
    if not kpp:
        messages.error(request, 'Для доступа к панели необходимо войти')
        return redirect('staff_login')

    kpp_name = request.session.get('kpp_name', 'КПП')
    visitors = Visitor.objects.filter(kpp=kpp).order_by('-created_at')

    return render(request, 'core/dashboard.html', {
        'visitors': visitors,
        'kpp_name': kpp_name
    })

def dashboard_partial(request):
    """Частичное обновление панели"""
    kpp = request.session.get('kpp_access')
    if not kpp:
        return render(request, 'core/dashboard_partial_active.html', {'visitors': []})

    tab = request.GET.get('tab', 'active')
    visitors = Visitor.objects.filter(kpp=kpp).order_by('-created_at')

    if tab == 'archive':
        filtered = [v for v in visitors if v.status == 'departed']
        return render(request, 'core/dashboard_partial_archive.html', {'visitors': filtered})
    else:
        filtered = [v for v in visitors if v.status != 'departed']
        return render(request, 'core/dashboard_partial_active.html', {'visitors': filtered})


def approve_visitor(request, pk):
    """Подтвердить вход"""
    kpp = request.session.get('kpp_access')
    if not kpp:
        messages.error(request, 'Для доступа к панели необходимо войти')
        return redirect('staff_login')

    visitor = get_object_or_404(Visitor, pk=pk, kpp=kpp)
    if visitor.status == 'pending':
        visitor.status = 'approved'
        visitor.arrival_time = timezone.now()
        visitor.save()
    return redirect('dashboard')


def mark_departed(request, pk):
    """Отметить как ушедшего"""
    kpp = request.session.get('kpp_access')
    if not kpp:
        messages.error(request, 'Для доступа к панели необходимо войти')
        return redirect('staff_login')

    visitor = get_object_or_404(Visitor, pk=pk, kpp=kpp)
    if visitor.status == 'approved':
        visitor.status = 'departed'
        visitor.departure_time = timezone.now()
        visitor.save()
    return redirect('dashboard')

def admin_login(request):
    """Логин для администратора"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_access')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            logout(request)
            login(request, user)
            return redirect('admin_access')
        else:
            messages.error(request, 'Неверный логин или пароль, или у вас нет прав администратора')

    return render(request, 'core/admin_login.html')

def staff_logout(request):
    """Выход для охраны"""
    logout(request)
    request.session.flush()
    return redirect('main_choice')


def request_success(request):
    """Страница успеха"""
    return render(request, 'core/success.html')