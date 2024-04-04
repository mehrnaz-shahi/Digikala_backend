from django.db import models


class Retailer(models.Model):
    PERFORMANCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    performance = models.CharField(max_length=10, choices=PERFORMANCE_CHOICES, default='medium')

    def __str__(self):
        return self.name
