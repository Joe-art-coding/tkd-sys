from rest_framework import serializers
from .models import Student, Parent
from fees.models import Fee
from schools.models import School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'monthly_fee']

class FeeSerializer(serializers.ModelSerializer):
    fee_type_display = serializers.CharField(source='get_fee_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Fee
        fields = ['id', 'fee_type', 'fee_type_display', 'amount', 'month', 'due_date', 
                  'paid_date', 'status', 'status_display', 'receipt_number']

class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    belt_display = serializers.CharField(source='get_belt_rank_display', read_only=True)
    fees = FeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'ic_number', 'school_name', 'belt_rank', 
                  'belt_display', 'join_date', 'is_active', 'phone', 'email', 'fees']

class ParentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_ic = serializers.CharField(source='student.ic_number', read_only=True)
    
    class Meta:
        model = Parent
        fields = ['id', 'user', 'student', 'student_name', 'student_ic', 'phone', 'relationship']