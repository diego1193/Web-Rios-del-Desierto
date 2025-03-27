from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
import json
import csv
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Client, DocumentType

def search_client(request):
    document_types = DocumentType.objects.all()
    return render(request, 'clients/search.html', {'document_types': document_types})

def search_client_api(request):
    if request.method == 'GET':
        document_type_id = request.GET.get('document_type')
        document_number = request.GET.get('document_number')
        
        if not all([document_type_id, document_number]):
            return JsonResponse({'error': 'Both document type and document number are required'}, status=400)
        
        try:
            client = Client.objects.get(
                document_type_id=document_type_id,
                document_number=document_number
            )
            
            data = {
                'id': client.id,
                'document_type': client.document_type.name,
                'document_number': client.document_number,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'email': client.email,
                'phone_number': client.phone_number,
                'address': client.address or '',
                'city': client.city or '',
            }
            
            return JsonResponse({'client': data})
        
        except Client.DoesNotExist:
            return JsonResponse({'error': 'Client not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def export_client_data(request, client_id, format_type):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return HttpResponse("Client not found", status=404)
    
    data = {
        'Document Type': client.document_type.name,
        'Document Number': client.document_number,
        'First Name': client.first_name,
        'Last Name': client.last_name,
        'Email': client.email,
        'Phone Number': client.phone_number,
        'Address': client.address or '',
        'City': client.city or '',
    }
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="client_{client.id}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(data.keys())
        writer.writerow(data.values())
        
        return response
    
    elif format_type == 'excel':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="client_{client.id}.xlsx"'
        
        df = pd.DataFrame([data])
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        response.write(buffer.getvalue())
        
        return response
    
    elif format_type == 'txt':
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="client_{client.id}.txt"'
        
        for key, value in data.items():
            response.write(f"{key}: {value}\n")
        
        return response
    
    return HttpResponse("Invalid format type", status=400)

def add_client(request):
    document_types = DocumentType.objects.all()
    
    if request.method == 'POST':
        # Extract form data
        document_type_id = request.POST.get('document_type')
        document_number = request.POST.get('document_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        
        # Validate required fields
        if not all([document_type_id, document_number, first_name, last_name, email, phone_number]):
            messages.error(request, 'Please fill all required fields')
            return render(request, 'clients/add_client.html', {
                'document_types': document_types,
                'form_data': request.POST
            })
        
        try:
            # Check if client already exists
            if Client.objects.filter(document_type_id=document_type_id, document_number=document_number).exists():
                messages.error(request, 'A client with this document type and number already exists')
                return render(request, 'clients/add_client.html', {
                    'document_types': document_types,
                    'form_data': request.POST
                })
            
            # Create new client
            client = Client(
                document_type_id=document_type_id,
                document_number=document_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                city=city
            )
            client.full_clean()  # Validate model fields
            client.save()
            
            messages.success(request, f'Client {first_name} {last_name} has been successfully added!')
            return redirect('search_client')
            
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                error_messages.extend(errors)
            
            for error in error_messages:
                messages.error(request, error)
                
            return render(request, 'clients/add_client.html', {
                'document_types': document_types,
                'form_data': request.POST
            })
    
    return render(request, 'clients/add_client.html', {'document_types': document_types})
