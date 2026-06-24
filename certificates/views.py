# certificates/views.py
import os
from .serializers import DepartmentSerializer, CertificateTypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from .models import Department, CertificateType
from drf_spectacular.utils import extend_schema  # ← agregar este import


class DepartmentListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DepartmentSerializer

    def get(self, request):
        auth_header    = request.META.get('HTTP_AUTHORIZATION', '')
        internal_token = os.environ.get('INTERNAL_SERVICE_TOKEN', '')
        is_internal    = auth_header == f"Internal {internal_token}"

        if not is_internal and not request.user.is_authenticated:
            return Response({'error': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)

        departments = Department.objects.all()
        data = [{'id': str(d.id), 'name': d.name} for d in departments]
        return Response(data)

class DepartmentListPublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        departments = Department.objects.all()
        data = [{'id': str(d.id), 'name': d.name} for d in departments]
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
    permission_classes = [AllowAny]  # 👈 cambia a AllowAny
    serializer_class = CertificateTypeSerializer

    @extend_schema(
        operation_id='certificate_type_list',
        responses=CertificateTypeSerializer(many=True)
    )
    def get(self, request):
        # ✅ Verificar autenticación — JWT normal O token interno
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        internal_token = os.environ.get('INTERNAL_SERVICE_TOKEN', '')
        
        is_internal = auth_header == f"Internal {internal_token}"
        is_authenticated = request.user and request.user.is_authenticated

        if not is_internal and not is_authenticated:
            return Response({'error': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)

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
                'is_active':   c.is_active,
                'tiene_pdf_automatico': c.tiene_pdf_automatico,
                'department': {
                    'id': c.department.id,
                    'name': c.department.name,
                },
            }
            for c in qs
        ]
        return Response(data)

class CertificateTypeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        auth_header    = request.META.get('HTTP_AUTHORIZATION', '')
        internal_token = os.environ.get('INTERNAL_SERVICE_TOKEN', '')
        is_internal    = auth_header == f"Internal {internal_token}"
        is_auth        = request.user and request.user.is_authenticated

        if not is_internal and not is_auth:
            return Response({'error': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            c = CertificateType.objects.select_related('department').get(id=pk)
        except CertificateType.DoesNotExist:
            return Response({'error': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id':                   c.id,
            'name':                 c.name,
            'price':                float(c.price),
            'description':          c.description,
            'is_active':            c.is_active,
            'tiene_pdf_automatico': c.tiene_pdf_automatico,
            'actividad_economica':  c.actividad_economica,
            'unidad_medida':        c.unidad_medida,
            'codigo_producto':      c.codigo_producto,
            'codigo_sin':           c.codigo_sin,
            'department_name':      c.department.name if c.department else '—',
            'department': {
                'id':   c.department.id,
                'name': c.department.name,
            } if c.department else None,
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
        cert.tiene_pdf_automatico = data.get('tiene_pdf_automatico', cert.tiene_pdf_automatico)
        cert.actividad_economica = data.get('actividad_economica', cert.actividad_economica)
        cert.codigo_sin = data.get('codigo_sin', cert.codigo_sin)
        cert.unidad_medida = data.get('unidad_medida', cert.unidad_medida)
        cert.save()
        return Response({
            'id': cert.id,
            'name': cert.name,
            'price': cert.price,
            'is_active': cert.is_active,
            'tiene_pdf_automatico': cert.tiene_pdf_automatico,
        })