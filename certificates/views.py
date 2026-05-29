# certificates/views.py
from .serializers import DepartmentSerializer, CertificateTypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Department, CertificateType
from drf_spectacular.utils import extend_schema  # ← agregar este import


class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer

    def get(self, request):
        departments = Department.objects.all()
        data = [{'id': d.id, 'name': d.name} for d in departments]
        return Response(data)
class DepartmentCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = DepartmentSerializer

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {'error': 'El campo name es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        department = Department.objects.create(name=name)
        return Response(
            {'id': department.id, 'name': department.name},
            status=status.HTTP_201_CREATED
        )

class CertificateTypeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CertificateTypeSerializer

    @extend_schema(                                          # ← agregar
        operation_id='certificate_type_list',               # ← agregar
        responses=CertificateTypeSerializer(many=True)      # ← agregar
    )                                                        # ← agregar
    def get(self, request):
        qs = CertificateType.objects.filter(is_active=True).select_related('department')
        department_id = request.query_params.get('department')
        if department_id:
            qs = qs.filter(department_id=department_id)
        data = [
            {
                'id': c.id,
                'name': c.name,
                'price': c.price,
                'description': c.description,
                'is_active':   c.is_active,  # ✅
                'department': {
                    'id': c.department.id,
                    'name': c.department.name,
                },
            }
            for c in qs
        ]
        return Response(data)


class CertificateTypeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CertificateTypeSerializer

    @extend_schema(                                          # ← agregar
        operation_id='certificate_type_detail',             # ← agregar
        responses=CertificateTypeSerializer                 # ← agregar
    )                                                        # ← agregar
    def get(self, request, pk):
        try:
            cert = CertificateType.objects.select_related('department').get(
                id=pk,
                is_active=True
            )
        except CertificateType.DoesNotExist:
            return Response(
                {'error': 'Certificado no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            'id': cert.id,
            'name': cert.name,
            'price': cert.price,
            'description': cert.description,
            'is_active': cert.is_active,
            'department': {
                'id': cert.department.id,
                'name': cert.department.name,
            },
        })


class CertificateTypeCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CertificateTypeSerializer

    def post(self, request):
        data = request.data
        required = ['name', 'price', 'department_id']
        for field in required:
            if not data.get(field):
                return Response(
                    {'error': f'El campo {field} es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            department = Department.objects.get(id=data['department_id'])
        except Department.DoesNotExist:
            return Response(
                {'error': 'Departamento no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        cert = CertificateType.objects.create(
            name=data['name'],
            price=data['price'],
            department=department,
            description=data.get('description', ''),
            actividad_economica=data.get('actividad_economica', '620100'),
            codigo_sin=data.get('codigo_sin', '99100'),
            codigo_producto=data.get('codigo_producto', ''),
            unidad_medida=data.get('unidad_medida', 62),
        )
        return Response({
            'id': cert.id,
            'name': cert.name,
            'price': cert.price,
        }, status=status.HTTP_201_CREATED)


class CertificateTypeUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CertificateTypeSerializer

    def put(self, request, pk):
        try:
            cert = CertificateType.objects.get(id=pk)
        except CertificateType.DoesNotExist:
            return Response(
                {'error': 'Certificado no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        cert.name = data.get('name', cert.name)
        cert.price = data.get('price', cert.price)
        cert.description = data.get('description', cert.description)
        cert.is_active = data.get('is_active', cert.is_active)
        cert.actividad_economica = data.get('actividad_economica', cert.actividad_economica)
        cert.codigo_sin = data.get('codigo_sin', cert.codigo_sin)
        cert.unidad_medida = data.get('unidad_medida', cert.unidad_medida)
        cert.save()
        return Response({
            'id': cert.id,
            'name': cert.name,
            'price': cert.price,
            'is_active': cert.is_active,
        })