from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Facility, Equipment, Booking, MaintenanceRecord, UsageLog, UserProfile
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,
    FacilityForm, EquipmentForm, BookingForm, BookingApprovalForm,
    MaintenanceRecordForm, MaintenanceUpdateForm
)

# Helper functions
def is_staff_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.profile.role in ['staff', 'admin'] or user.is_superuser

def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.profile.role == 'admin' or user.is_superuser

# View functions
def home(request):
    facilities = Facility.objects.filter(status='available')[:4]
    return render(request, 'home.html', {'facilities': facilities})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set default role to student
            profile = user.profile
            profile.role = 'student'
            profile.save()

            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})

# Facility views
def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'facility/facility_list.html', {'facilities': facilities})

def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    equipment = facility.equipment.all()

    # Get available time slots for the next 7 days
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    bookings = facility.bookings.filter(
        start_time__date__gte=today,
        start_time__date__lte=next_week,
        status__in=['approved', 'pending']
    ).order_by('start_time')

    return render(request, 'facility/facility_detail.html', {
        'facility': facility,
        'equipment': equipment,
        'bookings': bookings
    })

@login_required
def facility_create(request):
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to create facilities')
        return redirect('facility_list')

    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facility created successfully!')
            return redirect('facility_list')
    else:
        form = FacilityForm()

    return render(request, 'facility/facility_form.html', {'form': form, 'title': 'Create Facility'})

@login_required
def facility_update(request, pk):
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to update facilities')
        return redirect('facility_list')

    facility = get_object_or_404(Facility, pk=pk)

    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facility updated successfully!')
            return redirect('facility_detail', pk=facility.pk)
    else:
        form = FacilityForm(instance=facility)

    return render(request, 'facility/facility_form.html', {'form': form, 'title': 'Update Facility'})

# Booking views
@login_required
def booking_list(request):
    if is_staff_or_admin(request.user):
        # Staff and admin can see all bookings
        bookings = Booking.objects.all().order_by('-created_at')
    else:
        # Regular users can only see their own bookings
        bookings = request.user.bookings.all().order_by('-created_at')

    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Check if user has permission to view this booking
    if not (booking.user == request.user or is_staff_or_admin(request.user)):
        messages.error(request, 'You do not have permission to view this booking')
        return redirect('booking_list')

    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('booking_list')
    else:
        # Pre-select facility if provided in URL
        facility_id = request.GET.get('facility')
        if facility_id:
            form = BookingForm(initial={'facility': facility_id})
        else:
            form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form, 'title': 'Create Booking'})

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Check if user has permission to cancel this booking
    if not (booking.user == request.user or is_staff_or_admin(request.user)):
        messages.error(request, 'You do not have permission to cancel this booking')
        return redirect('booking_list')

    # Check if booking can be cancelled
    if booking.status not in ['pending', 'approved']:
        messages.error(request, 'This booking cannot be cancelled')
        return redirect('booking_detail', pk=booking.pk)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('booking_list')

    return render(request, 'booking/booking_cancel.html', {'booking': booking})

@login_required
def booking_approve(request, pk):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to approve bookings')
        return redirect('booking_list')

    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        form = BookingApprovalForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking status updated successfully!')
            return redirect('booking_detail', pk=booking.pk)
    else:
        form = BookingApprovalForm(instance=booking)

    return render(request, 'booking/booking_approve.html', {'form': form, 'booking': booking})

# Equipment views
@login_required
def equipment_list(request):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to view equipment')
        return redirect('home')

    equipment = Equipment.objects.all()
    return render(request, 'equipment/equipment_list.html', {'equipment': equipment})

@login_required
def equipment_detail(request, pk):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to view equipment details')
        return redirect('home')

    equipment = get_object_or_404(Equipment, pk=pk)
    maintenance_records = equipment.maintenance_records.all().order_by('-reported_at')

    return render(request, 'equipment/equipment_detail.html', {
        'equipment': equipment,
        'maintenance_records': maintenance_records
    })

@login_required
def equipment_create(request):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to create equipment')
        return redirect('equipment_list')

    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment created successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentForm()

    return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'Add Equipment'})

@login_required
def equipment_update(request, pk):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to update equipment')
        return redirect('equipment_list')

    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'Update Equipment'})

# Maintenance views
@login_required
def maintenance_report(request):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Maintenance issue reported successfully!')
            return redirect('maintenance_list')
    else:
        # Pre-select facility or equipment if provided in URL
        facility_id = request.GET.get('facility')
        equipment_id = request.GET.get('equipment')
        initial = {}
        if facility_id:
            initial['facility'] = facility_id
        if equipment_id:
            initial['equipment'] = equipment_id
        form = MaintenanceRecordForm(initial=initial)

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'title': 'Report Maintenance Issue'})

@login_required
def maintenance_list(request):
    if is_staff_or_admin(request.user):
        # Staff and admin can see all maintenance records
        records = MaintenanceRecord.objects.all().order_by('-reported_at')
    else:
        # Regular users can only see their own reports
        records = request.user.reported_issues.all().order_by('-reported_at')

    return render(request, 'maintenance/maintenance_list.html', {'records': records})

@login_required
def maintenance_detail(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)

    # Check if user has permission to view this record
    if not (record.reported_by == request.user or is_staff_or_admin(request.user)):
        messages.error(request, 'You do not have permission to view this maintenance record')
        return redirect('maintenance_list')

    return render(request, 'maintenance/maintenance_detail.html', {'record': record})

@login_required
def maintenance_update(request, pk):
    if not is_staff_or_admin(request.user):
        messages.error(request, 'You do not have permission to update maintenance records')
        return redirect('maintenance_list')

    record = get_object_or_404(MaintenanceRecord, pk=pk)

    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=record)
        if form.is_valid():
            maintenance = form.save(commit=False)
            if maintenance.status == 'resolved' and not maintenance.resolved_at:
                maintenance.resolved_at = timezone.now()
            maintenance.save()
            messages.success(request, 'Maintenance record updated successfully!')
            return redirect('maintenance_detail', pk=record.pk)
    else:
        form = MaintenanceUpdateForm(instance=record)

    return render(request, 'maintenance/maintenance_update.html', {'form': form, 'record': record})

# Dashboard views
@login_required
def dashboard(request):
    if is_admin(request.user):
        return admin_dashboard(request)
    elif is_staff_or_admin(request.user):
        return staff_dashboard(request)
    else:
        return user_dashboard(request)

@login_required
def user_dashboard(request):
    # Get user's upcoming bookings
    upcoming_bookings = request.user.bookings.filter(
        start_time__gte=timezone.now(),
        status__in=['approved', 'pending']
    ).order_by('start_time')[:5]

    # Get user's recent maintenance reports
    maintenance_reports = request.user.reported_issues.all().order_by('-reported_at')[:5]

    return render(request, 'dashboard/user_dashboard.html', {
        'upcoming_bookings': upcoming_bookings,
        'maintenance_reports': maintenance_reports
    })

@login_required
def staff_dashboard(request):
    if not is_staff_or_admin(request.user):
        return redirect('dashboard')

    # Get pending bookings
    pending_bookings = Booking.objects.filter(status='pending').order_by('start_time')

    # Get active maintenance issues
    active_issues = MaintenanceRecord.objects.filter(
        status__in=['reported', 'in_progress']
    ).order_by('-reported_at')

    # Get today's bookings
    today = timezone.now().date()
    today_bookings = Booking.objects.filter(
        start_time__date=today,
        status='approved'
    ).order_by('start_time')

    return render(request, 'dashboard/staff_dashboard.html', {
        'pending_bookings': pending_bookings,
        'active_issues': active_issues,
        'today_bookings': today_bookings
    })

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('dashboard')

    # Get counts for dashboard stats
    total_facilities = Facility.objects.count()
    total_equipment = Equipment.objects.count()
    total_users = UserProfile.objects.count()
    total_bookings = Booking.objects.count()

    # Get facilities under maintenance
    maintenance_facilities = Facility.objects.filter(status='maintenance')

    # Get recent bookings
    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]

    # Get maintenance issues by status
    maintenance_by_status = MaintenanceRecord.objects.values('status').annotate(count=Count('status'))

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_facilities': total_facilities,
        'total_equipment': total_equipment,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'maintenance_facilities': maintenance_facilities,
        'recent_bookings': recent_bookings,
        'maintenance_by_status': maintenance_by_status
    })

# API views
def check_availability(request):
    if request.method == 'POST':
        facility_id = request.POST.get('facility_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        booking_id = request.POST.get('booking_id')  # For excluding current booking when editing

        if not all([facility_id, start_time, end_time]):
            return JsonResponse({'available': False, 'message': 'Missing required parameters'})

        # Check for overlapping bookings
        overlapping_query = Booking.objects.filter(
            facility_id=facility_id,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['approved', 'pending']
        )

        # Exclude current booking if editing
        if booking_id:
            overlapping_query = overlapping_query.exclude(pk=booking_id)

        is_available = not overlapping_query.exists()

        return JsonResponse({
            'available': is_available,
            'message': 'Time slot is available' if is_available else 'Time slot is already booked'
        })

    return JsonResponse({'available': False, 'message': 'Invalid request method'})