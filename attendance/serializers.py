from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'date', 'check_in_time', 'class_type', 'instructor', 'notes']