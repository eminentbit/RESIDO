from django.db import models

class Payment(models.Model):
    PROVIDER_CHOICES = [
        ('MTN', 'MTN'),
        ('Orange', 'Orange'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    reference = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.reference} - {self.provider}"