from rest_framework import serializers
from .models import Department, CertificateType


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class CertificateTypeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )

    class Meta:
        model = CertificateType
        fields = (
            'id',
            'name',
            'price',
            'description',
            'department',
            'department_id',
            'actividad_economica',
            'codigo_sin',
            'codigo_producto',
            'unidad_medida',
            'is_active',
        )