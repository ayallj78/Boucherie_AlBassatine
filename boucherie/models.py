from django.db import models


class Avis(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField()
    message = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('commande', 'Commande'),
        ('partenariat', 'Partenariat'),
        ('information', 'Information'),
        ('autre', 'Autre'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='autre')
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_treated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"