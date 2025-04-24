from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Facility URLs
    path('facilities/', views.facility_list, name='facility_list'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility_detail'),
    path('facilities/create/', views.facility_create, name='facility_create'),
    path('facilities/<int:pk>/update/', views.facility_update, name='facility_update'),
    
    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('bookings/<int:pk>/approve/', views.booking_approve, name='booking_approve'),
    
    # Equipment URLs
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/update/', views.equipment_update, name='equipment_update'),
    
    # Maintenance URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/report/', views.maintenance_report, name='maintenance_report'),
    path('maintenance/<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    
    # API URLs
    path('api/check-availability/', views.check_availability, name='check_availability'),
]
