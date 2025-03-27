from django.db import models
from django.utils import timezone

# Create your models here.

class DocumentType(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Client(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['document_type', 'document_number']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.document_type.code} {self.document_number}"
    
    def get_total_purchases_last_month(self):
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        if today.month == 1:
            last_month = today.replace(year=today.year-1, month=12, day=1)
        else:
            last_month = today.replace(month=today.month-1, day=1)
        
        # Fix circular import by moving this import inside the method
        from reports.models import Purchase
        
        return Purchase.objects.filter(
            client=self,
            purchase_date__gte=last_month,
            purchase_date__lt=first_day_of_month
        ).aggregate(total=models.Sum('amount'))['total'] or 0
