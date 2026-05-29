from django.db import models
import uuid


class Department(models.Model):
    # ✅ UUID como PK
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CertificateType(models.Model):
    # ✅ UUID como PK
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name       = models.CharField(max_length=255)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    description = models.TextField(blank=True)

    actividad_economica = models.CharField(max_length=255, default='620100')
    codigo_sin          = models.CharField(max_length=20, default='99100')
    codigo_producto     = models.CharField(max_length=20, blank=True)
    unidad_medida       = models.IntegerField(default=62)

    is_active            = models.BooleanField(default=True)
    tiene_pdf_automatico = models.BooleanField(default=False)
    tipo_certificado     = models.CharField(
        max_length=50,
        choices=[
            ('baja_iimm',    'No haber sido dado de baja II.MM.'),
            ('titulo_grado', 'Título de Grado'),
            ('diplomado',    'Diplomado de Profesorado'),
            ('otro',         'Otro'),
        ],
        default='otro'
    )

    def __str__(self):
        return f"{self.name} - {self.price} Bs"