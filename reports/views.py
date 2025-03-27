from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
import pandas as pd
import csv
from io import BytesIO, StringIO
from clients.models import Client
from .models import Purchase
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def generate_loyalty_report(request):
    """Render the loyalty report page with description and download button"""
    return render(request, 'reports/loyalty_report.html')

def download_loyalty_report(request):
    """Generate and download the Excel loyalty report"""
    # Get the current date and calculate the first day of the current month
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Calculate the first day of the previous month
    if today.month == 1:
        last_month = today.replace(year=today.year-1, month=12, day=1)
    else:
        last_month = today.replace(month=today.month-1, day=1)
    
    # Get clients with purchases over 5,000,000 COP in the last month
    loyalty_clients = []
    
    for client in Client.objects.all():
        total_purchases = client.get_total_purchases_last_month()
        
        if total_purchases > 5000000:  # 5,000,000 COP
            loyalty_clients.append({
                'Document Type': client.document_type.name,
                'Document Number': client.document_number,
                'First Name': client.first_name,
                'Last Name': client.last_name,
                'Email': client.email,
                'Phone Number': client.phone_number,
                'Total Purchases (Last Month)': total_purchases
            })
    
    if not loyalty_clients:
        return HttpResponse("No loyalty clients found for the last month.")
    
    # Create Excel report
    df = pd.DataFrame(loyalty_clients)
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="loyalty_report_{last_month.strftime("%Y_%m")}.xlsx"'
    
    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Loyalty Clients')
    
    # Auto-adjust columns width
    worksheet = writer.sheets['Loyalty Clients']
    for i, column in enumerate(df.columns):
        column_width = max(df[column].astype(str).map(len).max(), len(column) + 2)
        worksheet.column_dimensions[chr(65 + i)].width = column_width
    
    writer.close()
    buffer.seek(0)
    
    response.write(buffer.getvalue())
    return response

def manage_purchases(request):
    """View for managing purchases - both individual and bulk uploads"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        # Process single purchase form
        if form_type == 'single_purchase':
            client_id = request.POST.get('client_id_actual')
            purchase_date = request.POST.get('purchase_date')
            
            # Fix amount format: replace both commas and periods before conversion
            amount_str = request.POST.get('amount', '0')
            # Remove all non-digit characters (periods, commas, spaces)
            amount_clean = ''.join(filter(str.isdigit, amount_str))
            
            description = request.POST.get('description', '')
            
            if not all([client_id, purchase_date, amount_clean]):
                messages.error(request, 'All required fields must be filled.')
                return redirect('manage_purchases')
            
            try:
                client = Client.objects.get(id=client_id)
                purchase = Purchase.objects.create(
                    client=client,
                    purchase_date=purchase_date,
                    amount=float(amount_clean),
                    description=description
                )
                messages.success(request, f'Purchase for {client.first_name} {client.last_name} added successfully.')
            except Client.DoesNotExist:
                messages.error(request, 'Invalid client selected.')
            except Exception as e:
                messages.error(request, f'Error adding purchase: {str(e)}')
        
        # Process bulk upload form
        elif form_type == 'bulk_upload':
            if 'file_upload' not in request.FILES:
                messages.error(request, 'Please select a file to upload.')
                return redirect('manage_purchases')
            
            uploaded_file = request.FILES['file_upload']
            skip_header = request.POST.get('skip_header') == 'on'
            
            try:
                # Process CSV or Excel file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:  # Excel file
                    df = pd.read_excel(uploaded_file)
                
                if skip_header and len(df) > 0:
                    df = df.iloc[1:]
                
                # Process each row
                success_count = 0
                error_count = 0
                
                for _, row in df.iterrows():
                    try:
                        # Find client
                        client = Client.objects.get(
                            document_type_id=row['document_type_id'],
                            document_number=str(row['document_number'])
                        )
                        
                        # Create purchase
                        Purchase.objects.create(
                            client=client,
                            purchase_date=row['purchase_date'],
                            amount=float(row['amount']),
                            description=row.get('description', '')
                        )
                        success_count += 1
                    except Exception:
                        error_count += 1
                
                if success_count > 0:
                    messages.success(request, f'Successfully added {success_count} purchases.')
                if error_count > 0:
                    messages.warning(request, f'Failed to add {error_count} purchases. Check your file format.')
            
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    
    # Get purchases with pagination
    purchases_list = Purchase.objects.all().order_by('-purchase_date')
    paginator = Paginator(purchases_list, 10)  # Show 10 purchases per page
    
    page = request.GET.get('page')
    try:
        recent_purchases = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        recent_purchases = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        recent_purchases = paginator.page(paginator.num_pages)
    
    return render(request, 'reports/manage_purchases.html', {
        'recent_purchases': recent_purchases
    })

def download_purchase_template(request):
    """Download a template file for bulk purchase uploads"""
    # Determine format (default to CSV)
    format_type = request.GET.get('format', 'csv')
    
    # Sample data
    data = {
        'document_type_id': [1, 1],
        'document_number': ['1234567890', '0987654321'],
        'purchase_date': ['2023-12-01', '2023-12-02'],
        'amount': [100000, 250000],
        'description': ['Sample purchase 1', 'Sample purchase 2']
    }
    
    df = pd.DataFrame(data)
    
    if format_type == 'excel':
        # Generate Excel file
        buffer = BytesIO()
        writer = pd.ExcelWriter(buffer, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Purchases')
        writer.close()
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=purchase_template.xlsx'
    else:
        # Generate CSV file
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        
        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=purchase_template.csv'
    
    return response

def search_clients_api(request):
    """API endpoint to search for clients by name or document number"""
    if request.method == 'GET':
        search_term = request.GET.get('term', '').strip()
        
        if not search_term:
            return JsonResponse({'error': 'Search term is required'}, status=400)
        
        # Search by document number or name
        clients = Client.objects.filter(
            models.Q(document_number__icontains=search_term) |
            models.Q(first_name__icontains=search_term) |
            models.Q(last_name__icontains=search_term)
        )[:10]
        
        if not clients.exists():
            return JsonResponse({'clients': []})
        
        client_list = []
        for client in clients:
            client_list.append({
                'id': client.id,
                'document_type': client.document_type.name,
                'document_number': client.document_number,
                'first_name': client.first_name,
                'last_name': client.last_name
            })
        
        return JsonResponse({'clients': client_list})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
