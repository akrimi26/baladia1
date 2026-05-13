from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Demande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE , null=True,
    blank=True)
    TYPE_SERVICE = [
        ('eau', 'ماء'),
        ('electricite', 'كهرباء'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'قيد الانتظار'),
        ('en_cours', 'قيد المعالجة'),
        ('acceptee', 'مقبولة'),
        ('refusee', 'مرفوضة'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cin = models.CharField(max_length=8)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    copie_cin = models.FileField(upload_to='documents/cin/', blank=True, null=True)
    plan_situation = models.FileField(upload_to='documents/plans/', blank=True, null=True)
    plan_architacturel = models.FileField(upload_to='documents/plans/', blank=True, null=True)
    certificat_propriete = models.FileField(upload_to='documents/certificats/', blank=True, null=True)
    certificat_exoneration = models.FileField(upload_to='documents/certificats/', blank=True, null=True)
    type_service = models.CharField(max_length=20, choices=TYPE_SERVICE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    description = models.TextField(blank=True)
    date_demande = models.DateTimeField(auto_now_add=True)

    recu = models.FileField(
    upload_to='recus/',
    blank=True,
    null=True
)
    def __str__(self):
        return f"{self.nom} {self.prenom}"