from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserSerializer, UserRegistrationSerializer, PatientSerializer,
    DoctorSerializer, PatientDoctorMappingSerializer
)

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request, format=None):
    return Response({
        'auth': {
            'register': reverse('register-list', request=request, format=format),
            'login': reverse('token_obtain_pair', request=request, format=format),
            'refresh': reverse('token_refresh', request=request, format=format),
        },
        'patients': reverse('patient-list', request=request, format=format),
        'doctors': reverse('doctor-list', request=request, format=format),
        'mappings': reverse('mapping-list', request=request, format=format),
    })

class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # If user_id is not provided, use the authenticated user
        if 'user_id' not in request.data:
            request.data['user_id'] = request.user.id
        
        # Check if the user exists
        try:
            user = User.objects.get(id=request.data['user_id'])
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found. Please register first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user already has a patient profile
        if hasattr(user, 'patient_profile'):
            return Response(
                {'error': 'User already has a patient profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set user as patient
        user.is_patient = True
        user.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Patient profile created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Doctor.objects.all()
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        user.is_doctor = True
        user.save()
        serializer.save(user=user)

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return PatientDoctorMapping.objects.all()
        elif hasattr(self.request.user, 'doctor_profile'):
            return PatientDoctorMapping.objects.filter(doctor=self.request.user.doctor_profile)
        elif hasattr(self.request.user, 'patient_profile'):
            return PatientDoctorMapping.objects.filter(patient=self.request.user.patient_profile)
        return PatientDoctorMapping.objects.none()

    @action(detail=False, methods=['get'])
    def patient_doctors(self, request):
        if not hasattr(request.user, 'patient_profile'):
            return Response(
                {'error': 'User is not a patient'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        mappings = self.get_queryset().filter(
            patient=request.user.patient_profile,
            is_active=True
        )
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def doctor_patients(self, request):
        if not hasattr(request.user, 'doctor_profile'):
            return Response(
                {'error': 'User is not a doctor'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        mappings = self.get_queryset().filter(
            doctor=request.user.doctor_profile,
            is_active=True
        )
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
