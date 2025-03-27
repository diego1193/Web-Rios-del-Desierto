from django.db import models
from clients.models import Client
from django.utils import timezone
# Create your models here.

class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.client} - ${self.amount} on {self.purchase_date}"
