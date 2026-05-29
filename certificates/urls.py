# certificates/urls.py
from django.urls import path
from .views import (
    DepartmentListView,
    DepartmentCreateView,
    CertificateTypeListView,
    CertificateTypeDetailView,
    CertificateTypeCreateView,
    CertificateTypeUpdateView,
)

urlpatterns = [
    # Públicas (ciudadano autenticado)
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/crear/', DepartmentCreateView.as_view(), name='department-create'),

    
    path('tipos/', CertificateTypeListView.as_view(), name='certificate-type-list'),
    path('tipos/crear/', CertificateTypeCreateView.as_view(), name='certificate-create'),
    path('tipos/<uuid:pk>/', CertificateTypeDetailView.as_view(), name='certificate-type-detail'),

    # Solo admin
    path('tipos/<uuid:pk>/editar/', CertificateTypeUpdateView.as_view(), name='certificate-update'),
]