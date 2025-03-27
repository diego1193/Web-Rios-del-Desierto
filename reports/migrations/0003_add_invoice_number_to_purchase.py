from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_purchase_invoice_number_purchase_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ] 