from rest_framework import serializers
from .models import Sample,Faculty,Company,Student,Applicants
from django.contrib.auth.hashers import make_password
from .models import Internship, FullTime, Rounds

class SampleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['id','name','description']





# Serializer for Faculty login request
class FacultyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# Serializer for Company login request
class CompanyLoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

# Serializer for Student login request
class StudentLoginSerializer(serializers.Serializer):
    SRN = serializers.CharField(max_length=15, required=False)
    password = serializers.CharField(write_only=True)

    





class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['faculty_id', 'role', 'staff_id', 'user_id', 'password', 'name', 'email', 'ph_number', 'department']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id', 'name', 'type', 'designation_role', 'location', 'package', 'user_id', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'SRN', 'branch', 'dob', 'email', 'ph_number', 'gender', 'cgpa', 'faculty_advisor', 'user_id', 'password', 'faculty']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class StudentSerializerForFaculty(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'SRN', 'branch', 'dob', 'email', 'ph_number', 'gender', 'cgpa', 'faculty_advisor']    






class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Internship
        fields = ['internship_id', 'name', 'location', 'stipend', 'ppo', 'type', 'duration', 'cutoff', 'company_id']

class FullTimeSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = FullTime
        fields = ['job_id', 'job_title', 'location', 'package', 'cutoff', 'company_id']

class ApplicantSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    internship = InternshipSerializer()
    job = FullTimeSerializer()

    class Meta:
        model = Applicants
        fields = ['applicant_id', 'student', 'type', 'internship', 'job', 'company']

class RoundsSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(read_only=True)  # Nested Applicant details (read-only)
    applicant_id = serializers.PrimaryKeyRelatedField(
        queryset=Applicants.objects.all(), source='applicant', write_only=True
    )  # Write applicant ID when creating/updating

    class Meta:
        model = Rounds
        fields = [
            'round_id',
            'round_no',
            'round_name',
            'date',
            'time_scheduled',
            'status',
            'applicant',
            'applicant_id',
        ]
        # Use applicant_id for input, and nested applicant details for output

    def create(self, validated_data):
        return Rounds.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update fields as needed
        instance.round_no = validated_data.get('round_no', instance.round_no)
        instance.round_name = validated_data.get('round_name', instance.round_name)
        instance.date = validated_data.get('date', instance.date)
        instance.time_scheduled = validated_data.get('time_scheduled', instance.time_scheduled)
        instance.status = validated_data.get('status', instance.status)
        instance.applicant = validated_data.get('applicant', instance.applicant)
        instance.save()
        return instance        