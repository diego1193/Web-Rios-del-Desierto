from django.core.management.base import BaseCommand
from django.utils import timezone
from clients.models import DocumentType, Client
from reports.models import Purchase
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Loads test data for clients and purchases'

    def handle(self, *args, **kwargs):
        # Create document types
        self.stdout.write('Creating document types...')
        doc_types = [
            {'name': 'National ID', 'code': 'ID'},
            {'name': 'Passport', 'code': 'PASS'},
            {'name': 'NIT', 'code': 'NIT'},
        ]
        
        for dt in doc_types:
            DocumentType.objects.get_or_create(name=dt['name'], code=dt['code'])
        
        id_type = DocumentType.objects.get(code='ID')
        passport_type = DocumentType.objects.get(code='PASS')
        nit_type = DocumentType.objects.get(code='NIT')
        
        # Create clients
        self.stdout.write('Creating clients...')
        clients_data = [
            {
                'document_type': id_type,
                'document_number': '1234567890',
                'first_name': 'Juan',
                'last_name': 'Perez',
                'email': 'juan.perez@example.com',
                'phone_number': '3001234567',
                'address': 'Calle 123 #45-67',
                'city': 'Bogotá'
            },
            {
                'document_type': passport_type,
                'document_number': 'AB123456',
                'first_name': 'Maria',
                'last_name': 'Gomez',
                'email': 'maria.gomez@example.com',
                'phone_number': '3109876543',
                'address': 'Carrera 78 #90-12',
                'city': 'Medellín'
            },
            {
                'document_type': nit_type,
                'document_number': '900123456-7',
                'first_name': 'Empresa',
                'last_name': 'Colombia SAS',
                'email': 'info@empresacolombia.com',
                'phone_number': '6013456789',
                'address': 'Av. El Dorado #123-45',
                'city': 'Bogotá'
            },
            {
                'document_type': id_type,
                'document_number': '2345678901',
                'first_name': 'Carlos',
                'last_name': 'Rodriguez',
                'email': 'carlos.rodriguez@example.com',
                'phone_number': '3201234567',
                'address': 'Diagonal 45 #67-89',
                'city': 'Cali'
            },
            {
                'document_type': id_type,
                'document_number': '3456789012',
                'first_name': 'Ana',
                'last_name': 'Martinez',
                'email': 'ana.martinez@example.com',
                'phone_number': '3507654321',
                'address': 'Calle 67 #89-01',
                'city': 'Barranquilla'
            },
        ]
        
        clients = []
        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                document_type=client_data['document_type'],
                document_number=client_data['document_number'],
                defaults=client_data
            )
            clients.append(client)
            if created:
                self.stdout.write(f'Created client: {client}')
            else:
                self.stdout.write(f'Client already exists: {client}')
        
        # Create purchases
        self.stdout.write('Creating purchases...')
        today = timezone.now().date()
        
        # Get the first day of the current month and the previous month
        first_day_of_month = today.replace(day=1)
        if today.month == 1:
            first_day_of_prev_month = today.replace(year=today.year-1, month=12, day=1)
        else:
            first_day_of_prev_month = today.replace(month=today.month-1, day=1)
        
        # Generate purchases for the previous month
        # Ensure one client has over 5,000,000 COP in purchases for testing the loyalty report
        loyalty_client = clients[0]  # Juan Perez will be our loyalty client
        
        # Create a large purchase for the loyalty client
        Purchase.objects.create(
            client=loyalty_client,
            amount=6000000.00,  # Over 5,000,000 COP
            purchase_date=first_day_of_prev_month + timedelta(days=random.randint(0, 27)),
            description='Large purchase for loyalty program testing'
        )
        
        # Create additional random purchases for all clients
        for i in range(50):
            client = random.choice(clients)
            purchase_date = first_day_of_prev_month + timedelta(days=random.randint(0, 27))
            
            # Amounts between 100,000 and 1,000,000 COP
            amount = random.uniform(100000, 1000000)
            
            Purchase.objects.create(
                client=client,
                amount=amount,
                purchase_date=purchase_date
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded test data!')) 