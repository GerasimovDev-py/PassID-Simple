from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-pass/', views.visitor_form, name='visitor_form'),
    path('success/', views.request_success, name='request_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/partial/', views.dashboard_partial, name='dashboard_partial'),
    path('approve/<int:pk>/', views.approve_visitor, name='approve'),
    path('departed/<int:pk>/', views.mark_departed, name='mark_departed'),
]