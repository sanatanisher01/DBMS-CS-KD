import os
import django
import datetime
from django.utils import timezone

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsphere.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from facility.models import Facility, Equipment, Booking, MaintenanceRecord, UserProfile

def create_users():
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        is_staff=True,
        is_superuser=True
    )
    admin_profile = UserProfile.objects.get(user=admin_user)
    admin_profile.role = 'admin'
    admin_profile.phone = '123-456-7890'
    admin_profile.save()

    # Create staff user
    staff_user = User.objects.create_user(
        username='staff',
        email='staff@example.com',
        password='staff123',
        first_name='Staff',
        last_name='User'
    )
    staff_profile = UserProfile.objects.get(user=staff_user)
    staff_profile.role = 'staff'
    staff_profile.phone = '123-456-7891'
    staff_profile.save()

    # Create faculty user
    faculty_user = User.objects.create_user(
        username='faculty',
        email='faculty@example.com',
        password='faculty123',
        first_name='Faculty',
        last_name='User'
    )
    faculty_profile = UserProfile.objects.get(user=faculty_user)
    faculty_profile.role = 'faculty'
    faculty_profile.phone = '123-456-7892'
    faculty_profile.save()

    # Create student user
    student_user = User.objects.create_user(
        username='student',
        email='student@example.com',
        password='student123',
        first_name='Student',
        last_name='User'
    )
    student_profile = UserProfile.objects.get(user=student_user)
    student_profile.role = 'student'
    student_profile.phone = '123-456-7893'
    student_profile.save()

    return {
        'admin': admin_user,
        'staff': staff_user,
        'faculty': faculty_user,
        'student': student_user
    }

def create_facilities():
    # Create facilities
    basketball_court = Facility.objects.create(
        name='Main Basketball Court',
        type='court',
        location='Sports Complex, Building A',
        capacity=30,
        description='Full-size basketball court with digital scoreboard and spectator seating.',
        status='available'
    )

    tennis_court = Facility.objects.create(
        name='Tennis Courts',
        type='court',
        location='Sports Complex, Outdoor Area',
        capacity=8,
        description='Two professional-grade tennis courts with lighting for evening play.',
        status='available'
    )

    swimming_pool = Facility.objects.create(
        name='Olympic Swimming Pool',
        type='pool',
        location='Aquatic Center, Building B',
        capacity=50,
        description='Olympic-size swimming pool with 8 lanes and diving platforms.',
        status='available'
    )

    gym = Facility.objects.create(
        name='Fitness Center',
        type='gym',
        location='Sports Complex, Building A, 2nd Floor',
        capacity=100,
        description='Modern fitness center with cardio equipment, weight machines, and free weights.',
        status='available'
    )

    football_field = Facility.objects.create(
        name='Football Field',
        type='field',
        location='Sports Complex, Outdoor Area',
        capacity=200,
        description='Full-size football field with artificial turf and floodlights.',
        status='maintenance'
    )

    return {
        'basketball_court': basketball_court,
        'tennis_court': tennis_court,
        'swimming_pool': swimming_pool,
        'gym': gym,
        'football_field': football_field
    }

def create_equipment(facilities):
    # Create equipment for basketball court
    basketball_equipment = [
        Equipment(
            facility=facilities['basketball_court'],
            name='Basketballs',
            type='sports',
            status='available',
            purchase_date=datetime.date(2022, 1, 15),
            notes='Set of 10 basketballs'
        ),
        Equipment(
            facility=facilities['basketball_court'],
            name='Digital Scoreboard',
            type='electronic',
            status='available',
            purchase_date=datetime.date(2021, 11, 10),
            last_maintenance_date=datetime.date(2023, 2, 20)
        ),
        Equipment(
            facility=facilities['basketball_court'],
            name='Portable Hoops',
            type='movable',
            status='available',
            purchase_date=datetime.date(2022, 3, 5)
        )
    ]

    # Create equipment for tennis court
    tennis_equipment = [
        Equipment(
            facility=facilities['tennis_court'],
            name='Tennis Rackets',
            type='sports',
            status='available',
            purchase_date=datetime.date(2022, 2, 10),
            notes='Set of 8 rackets'
        ),
        Equipment(
            facility=facilities['tennis_court'],
            name='Tennis Balls',
            type='sports',
            status='available',
            purchase_date=datetime.date(2023, 1, 5),
            notes='24 cans of tennis balls'
        ),
        Equipment(
            facility=facilities['tennis_court'],
            name='Ball Machine',
            type='electronic',
            status='maintenance',
            purchase_date=datetime.date(2021, 6, 15),
            last_maintenance_date=datetime.date(2023, 3, 10)
        )
    ]

    # Create equipment for swimming pool
    swimming_equipment = [
        Equipment(
            facility=facilities['swimming_pool'],
            name='Lane Dividers',
            type='movable',
            status='available',
            purchase_date=datetime.date(2021, 8, 20)
        ),
        Equipment(
            facility=facilities['swimming_pool'],
            name='Kickboards',
            type='sports',
            status='available',
            purchase_date=datetime.date(2022, 4, 12),
            notes='Set of 20 kickboards'
        ),
        Equipment(
            facility=facilities['swimming_pool'],
            name='Timing System',
            type='electronic',
            status='available',
            purchase_date=datetime.date(2021, 5, 8),
            last_maintenance_date=datetime.date(2023, 1, 15)
        )
    ]

    # Create equipment for gym
    gym_equipment = [
        Equipment(
            facility=facilities['gym'],
            name='Treadmills',
            type='electronic',
            status='available',
            purchase_date=datetime.date(2022, 2, 18),
            last_maintenance_date=datetime.date(2023, 2, 10),
            notes='10 treadmills'
        ),
        Equipment(
            facility=facilities['gym'],
            name='Weight Machines',
            type='fixed',
            status='available',
            purchase_date=datetime.date(2021, 9, 5),
            last_maintenance_date=datetime.date(2023, 1, 20),
            notes='15 different weight machines'
        ),
        Equipment(
            facility=facilities['gym'],
            name='Free Weights',
            type='movable',
            status='available',
            purchase_date=datetime.date(2022, 3, 15),
            notes='Complete set of dumbbells and barbells'
        ),
        Equipment(
            facility=facilities['gym'],
            name='Exercise Bikes',
            type='electronic',
            status='maintenance',
            purchase_date=datetime.date(2021, 11, 8),
            last_maintenance_date=datetime.date(2023, 3, 5),
            notes='5 exercise bikes'
        )
    ]

    # Create equipment for football field
    football_equipment = [
        Equipment(
            facility=facilities['football_field'],
            name='Footballs',
            type='sports',
            status='available',
            purchase_date=datetime.date(2022, 5, 10),
            notes='Set of 15 footballs'
        ),
        Equipment(
            facility=facilities['football_field'],
            name='Goal Posts',
            type='fixed',
            status='available',
            purchase_date=datetime.date(2021, 7, 20),
            last_maintenance_date=datetime.date(2023, 2, 25)
        ),
        Equipment(
            facility=facilities['football_field'],
            name='Training Cones',
            type='movable',
            status='available',
            purchase_date=datetime.date(2022, 6, 5),
            notes='Set of 50 cones'
        )
    ]

    # Save all equipment
    all_equipment = basketball_equipment + tennis_equipment + swimming_equipment + gym_equipment + football_equipment
    for equipment in all_equipment:
        equipment.save()

    return all_equipment

def create_bookings(users, facilities):
    # Current time
    now = timezone.now()

    # Create bookings
    bookings = []

    # Approved bookings
    booking1 = Booking(
        user=users['student'],
        facility=facilities['basketball_court'],
        start_time=now + datetime.timedelta(days=1, hours=10),
        end_time=now + datetime.timedelta(days=1, hours=12),
        status='approved',
        purpose='Basketball practice',
        participants=10
    )
    bookings.append(booking1)

    booking2 = Booking(
        user=users['faculty'],
        facility=facilities['tennis_court'],
        start_time=now + datetime.timedelta(days=2, hours=14),
        end_time=now + datetime.timedelta(days=2, hours=16),
        status='approved',
        purpose='Tennis match',
        participants=4
    )
    bookings.append(booking2)

    booking3 = Booking(
        user=users['student'],
        facility=facilities['swimming_pool'],
        start_time=now + datetime.timedelta(days=3, hours=9),
        end_time=now + datetime.timedelta(days=3, hours=10),
        status='approved',
        purpose='Swimming practice',
        participants=1
    )
    bookings.append(booking3)

    # Pending bookings
    booking4 = Booking(
        user=users['student'],
        facility=facilities['gym'],
        start_time=now + datetime.timedelta(days=4, hours=16),
        end_time=now + datetime.timedelta(days=4, hours=18),
        status='pending',
        purpose='Workout session',
        participants=2
    )
    bookings.append(booking4)

    booking5 = Booking(
        user=users['faculty'],
        facility=facilities['basketball_court'],
        start_time=now + datetime.timedelta(days=5, hours=13),
        end_time=now + datetime.timedelta(days=5, hours=15),
        status='pending',
        purpose='Faculty basketball game',
        participants=15
    )
    bookings.append(booking5)

    # Completed bookings
    booking6 = Booking(
        user=users['student'],
        facility=facilities['tennis_court'],
        start_time=now - datetime.timedelta(days=2, hours=10),
        end_time=now - datetime.timedelta(days=2, hours=8),
        status='completed',
        purpose='Tennis practice',
        participants=2
    )
    # Fix the end time to be after start time
    booking6.end_time = booking6.start_time + datetime.timedelta(hours=2)
    bookings.append(booking6)

    booking7 = Booking(
        user=users['faculty'],
        facility=facilities['gym'],
        start_time=now - datetime.timedelta(days=3, hours=7),
        end_time=now - datetime.timedelta(days=3, hours=6),
        status='completed',
        purpose='Morning workout',
        participants=1
    )
    # Fix the end time to be after start time
    booking7.end_time = booking7.start_time + datetime.timedelta(hours=1)
    bookings.append(booking7)

    for booking in bookings:
        try:
            booking.save()
            print(f"Created booking: {booking}")
        except Exception as e:
            print(f"Error creating booking: {e}")

    return bookings

def create_maintenance_records(users, facilities, equipment):
    # Create maintenance records
    maintenance_records = [
        # Facility maintenance
        MaintenanceRecord(
            facility=facilities['football_field'],
            reported_by=users['staff'],
            issue_description='Artificial turf needs repair in several areas',
            status='in_progress',
            reported_at=timezone.now() - datetime.timedelta(days=5)
        ),

        # Equipment maintenance
        MaintenanceRecord(
            equipment=equipment[14],  # Exercise Bikes
            reported_by=users['student'],
            issue_description='Exercise bike #3 making strange noise when pedaling',
            status='reported',
            reported_at=timezone.now() - datetime.timedelta(days=2)
        ),
        MaintenanceRecord(
            equipment=equipment[8],  # Ball Machine
            reported_by=users['faculty'],
            issue_description='Tennis ball machine not feeding balls correctly',
            status='in_progress',
            reported_at=timezone.now() - datetime.timedelta(days=7)
        ),

        # Resolved maintenance
        MaintenanceRecord(
            facility=facilities['swimming_pool'],
            reported_by=users['student'],
            issue_description='Water temperature too cold',
            status='resolved',
            reported_at=timezone.now() - datetime.timedelta(days=10),
            resolved_at=timezone.now() - datetime.timedelta(days=8),
            resolution_notes='Adjusted water heater settings'
        )
    ]

    for record in maintenance_records:
        record.save()

    return maintenance_records

def main():
    print("Initializing SportSphere database with sample data...")

    # Check if data already exists
    if User.objects.filter(username='admin').exists():
        print("Sample data already exists. Skipping initialization.")
        return

    # Create sample data
    users = create_users()
    print("Created users: admin, staff, faculty, student")

    facilities = create_facilities()
    print("Created facilities: basketball court, tennis court, swimming pool, gym, football field")

    equipment = create_equipment(facilities)
    print(f"Created {len(equipment)} equipment items")

    bookings = create_bookings(users, facilities)
    print(f"Created {len(bookings)} bookings")

    maintenance_records = create_maintenance_records(users, facilities, equipment)
    print(f"Created {len(maintenance_records)} maintenance records")

    print("Database initialization complete!")

if __name__ == "__main__":
    main()
