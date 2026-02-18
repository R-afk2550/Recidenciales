"""
Management command to populate database with sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, timedelta
from apps.residents.models import Building, Unit, Resident
from apps.visitors.models import Visitor, TemporaryCode
from apps.access_control.models import AccessPoint, AccessCode
from apps.access_logs.models import AccessLog
from utils.code_generator import generate_temporary_access_code

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to populate database...'))
        
        # Create users if they don't exist
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@test.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if _:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
        
        guard_user, created = User.objects.get_or_create(
            username='guard1',
            defaults={
                'email': 'guard1@test.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'role': User.Role.GUARD,
                'phone': '+52 55 1234 5678',
                'is_staff': True
            }
        )
        if created:
            guard_user.set_password('guard123')
            guard_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created guard user: {guard_user.username}'))
        
        # Create buildings
        building_a, _ = Building.objects.get_or_create(
            code='A',
            defaults={
                'name': 'Torre A',
                'address': 'Av. Principal 123',
                'floors': 10,
                'units_per_floor': 4
            }
        )
        if _:
            self.stdout.write(self.style.SUCCESS(f'Created building: {building_a.name}'))
        
        building_b, _ = Building.objects.get_or_create(
            code='B',
            defaults={
                'name': 'Torre B',
                'address': 'Av. Principal 125',
                'floors': 8,
                'units_per_floor': 6
            }
        )
        if _:
            self.stdout.write(self.style.SUCCESS(f'Created building: {building_b.name}'))
        
        # Create units
        units_data = [
            (building_a, '101', 1, 'Carlos González', '+52 55 9876 5432'),
            (building_a, '102', 1, 'María López', '+52 55 8765 4321'),
            (building_a, '201', 2, 'José Martínez', '+52 55 7654 3210'),
            (building_b, '101', 1, 'Ana Rodríguez', '+52 55 6543 2109'),
            (building_b, '102', 1, 'Pedro Sánchez', '+52 55 5432 1098'),
        ]
        
        units = []
        for building, number, floor, owner_name, owner_phone in units_data:
            unit, created = Unit.objects.get_or_create(
                building=building,
                number=number,
                defaults={
                    'floor': floor,
                    'owner_name': owner_name,
                    'owner_phone': owner_phone,
                    'is_occupied': True
                }
            )
            units.append(unit)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created unit: {unit}'))
        
        # Create residents
        residents_data = [
            (units[0], 'Carlos', 'González', 'ID123456', '+52 55 9876 5432', 'carlos@email.com', Resident.ResidentType.OWNER),
            (units[0], 'Laura', 'González', 'ID123457', '+52 55 9876 5433', 'laura@email.com', Resident.ResidentType.FAMILY),
            (units[1], 'María', 'López', 'ID234567', '+52 55 8765 4321', 'maria@email.com', Resident.ResidentType.OWNER),
            (units[2], 'José', 'Martínez', 'ID345678', '+52 55 7654 3210', 'jose@email.com', Resident.ResidentType.TENANT),
            (units[3], 'Ana', 'Rodríguez', 'ID456789', '+52 55 6543 2109', 'ana@email.com', Resident.ResidentType.OWNER),
        ]
        
        residents = []
        for unit, first_name, last_name, document_id, phone, email, resident_type in residents_data:
            resident, created = Resident.objects.get_or_create(
                document_id=document_id,
                defaults={
                    'unit': unit,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'email': email,
                    'resident_type': resident_type,
                    'is_authorized': True,
                    'move_in_date': date.today() - timedelta(days=365),
                    'emergency_contact_name': 'Contacto de Emergencia',
                    'emergency_contact_phone': '+52 55 1111 2222'
                }
            )
            residents.append(resident)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created resident: {resident.full_name}'))
        
        # Create access points
        access_points_data = [
            ('Puerta Principal', 'MAIN-01', AccessPoint.AccessType.MAIN_GATE, 'Entrada principal del residencial', None, True, True, True, True, True),
            ('Puerta Peatonal A', 'PED-A-01', AccessPoint.AccessType.PEDESTRIAN, 'Entrada peatonal Torre A', building_a, True, False, True, True, False),
            ('Garage Torre A', 'GAR-A-01', AccessPoint.AccessType.GARAGE, 'Entrada vehicular Torre A', building_a, True, True, False, True, False),
            ('Puerta Peatonal B', 'PED-B-01', AccessPoint.AccessType.PEDESTRIAN, 'Entrada peatonal Torre B', building_b, True, False, True, True, False),
        ]
        
        access_points = []
        for name, code, access_type, location, building, supports_qr, supports_rfid, supports_numeric, is_entry, is_exit in access_points_data:
            access_point, created = AccessPoint.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'access_type': access_type,
                    'location': location,
                    'building': building,
                    'supports_qr': supports_qr,
                    'supports_rfid': supports_rfid,
                    'supports_numeric': supports_numeric,
                    'is_entry': is_entry,
                    'is_exit': is_exit,
                    'is_active': True
                }
            )
            access_points.append(access_point)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created access point: {access_point.name}'))
        
        # Create access codes for residents
        for resident in residents[:3]:  # Create codes for first 3 residents
            code = f'RFID{resident.document_id[-6:]}'
            access_code, created = AccessCode.objects.get_or_create(
                code=code,
                defaults={
                    'resident': resident,
                    'code_type': AccessCode.CodeType.RFID,
                    'is_active': True,
                    'issued_by': admin_user
                }
            )
            if created:
                access_code.access_points.set(access_points)
                self.stdout.write(self.style.SUCCESS(f'Created access code for {resident.full_name}: {code}'))
        
        # Create visitors
        visitors_data = [
            (units[0], residents[0], 'Juan', 'Pérez', 'VIS123456', '+52 55 1111 1111', Visitor.VisitorType.GUEST, 'Visita social'),
            (units[1], residents[2], 'Delivery', 'Express', '', '+52 55 2222 2222', Visitor.VisitorType.DELIVERY, 'Entrega de paquete'),
            (units[2], residents[3], 'Plomero', 'Servicios', 'SRV123', '+52 55 3333 3333', Visitor.VisitorType.SERVICE, 'Reparación de tubería'),
        ]
        
        visitors = []
        for unit, resident, first_name, last_name, document_id, phone, visitor_type, purpose in visitors_data:
            visitor, created = Visitor.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                unit=unit,
                expected_date=date.today(),
                defaults={
                    'document_id': document_id,
                    'phone': phone,
                    'visitor_type': visitor_type,
                    'resident': resident,
                    'purpose': purpose,
                    'expected_time': time(14, 0),
                    'status': Visitor.Status.APPROVED,
                    'authorized_by': guard_user
                }
            )
            visitors.append(visitor)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created visitor: {visitor.full_name}'))
        
        # Create temporary codes for visitors
        for visitor in visitors:
            code = generate_temporary_access_code('alphanumeric', 8)
            temp_code, created = TemporaryCode.objects.get_or_create(
                visitor=visitor,
                code=code,
                defaults={
                    'code_type': TemporaryCode.CodeType.ALPHANUMERIC,
                    'valid_from': timezone.now(),
                    'valid_until': timezone.now() + timedelta(hours=24),
                    'max_uses': 2,
                    'is_active': True,
                    'generated_by': guard_user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created temporary code for {visitor.full_name}: {code}'))
        
        # Create some access logs
        for i in range(5):
            resident = residents[i % len(residents)]
            access_point = access_points[0]
            
            log, created = AccessLog.objects.get_or_create(
                resident=resident,
                person_name=resident.full_name,
                access_point=access_point,
                timestamp=timezone.now() - timedelta(hours=i),
                defaults={
                    'person_document': resident.document_id,
                    'access_type': AccessLog.AccessType.ENTRY if i % 2 == 0 else AccessLog.AccessType.EXIT,
                    'access_method': AccessLog.AccessMethod.RFID,
                    'status': AccessLog.Status.SUCCESS,
                    'authorized_by': guard_user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created access log for {resident.full_name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write(self.style.SUCCESS('- Login to admin: http://localhost:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('  Username: admin'))
        self.stdout.write(self.style.SUCCESS('  Password: admin123'))
        self.stdout.write(self.style.SUCCESS('\n- Or use the API with JWT authentication'))
