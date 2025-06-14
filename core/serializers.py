from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_doctor', 'is_patient')
        read_only_fields = ('id', 'is_doctor', 'is_patient')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_patient=True),
        source='user',
        write_only=True
    )

    class Meta:
        model = Patient
        fields = ('id', 'user', 'user_id', 'date_of_birth', 'gender', 'address',
                 'phone_number', 'medical_history', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_doctor=True),
        source='user',
        write_only=True
    )

    class Meta:
        model = Doctor
        fields = ('id', 'user', 'user_id', 'specialization', 'license_number',
                 'years_of_experience', 'hospital', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'patient_id', 'doctor', 'doctor_id',
                 'assigned_date', 'is_active', 'notes')
        read_only_fields = ('id', 'assigned_date') 