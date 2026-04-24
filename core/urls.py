from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_choice, name='main_choice'),
    path('responsible-login/', views.responsible_login, name='responsible_login'),
    path('responsible-kpp-choice/', views.responsible_kpp_choice, name='responsible_kpp_choice'),
    path('responsible-form/', views.visitor_form_responsible, name='visitor_form_responsible'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/partial/', views.dashboard_partial, name='dashboard_partial'),
    path('approve/<int:pk>/', views.approve_visitor, name='approve_visitor'),
    path('departed/<int:pk>/', views.mark_departed, name='mark_departed'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('admin-access/', views.admin_access, name='admin_access'),
    path('admin-add-responsible/', views.admin_add_responsible, name='admin_add_responsible'),
    path('admin-edit-responsible/<int:user_id>/', views.admin_edit_responsible, name='admin_edit_responsible'),
    path('admin-delete-responsible/<int:user_id>/', views.admin_delete_responsible, name='admin_delete_responsible'),
    path('success/', views.request_success, name='request_success'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-access/', views.admin_access, name='admin_access'),
]