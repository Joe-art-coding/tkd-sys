from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, date
from .models import Student, Parent
from fees.models import Fee
from schools.models import School, UserProfile
from .serializers import StudentSerializer, FeeSerializer, ParentSerializer, SchoolSerializer

# ==================== STUDENT VIEWSET ====================

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['get'])
    def fees(self, request, pk=None):
        student = self.get_object()
        fees = student.fees.all()
        serializer = FeeSerializer(fees, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_ic(self, request):
        ic_number = request.query_params.get('ic', None)
        if ic_number:
            try:
                student = Student.objects.get(ic_number=ic_number)
                serializer = self.get_serializer(student)
                return Response(serializer.data)
            except Student.DoesNotExist:
                return Response({'error': 'Student not found'}, status=404)
        return Response({'error': 'IC number required'}, status=400)

# ==================== PARENT API ====================

class ParentLoginView(APIView):
    """Parent login using IC number and password"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        ic_number = request.data.get('ic_number')
        password = request.data.get('password')
        
        try:
            student = Student.objects.get(ic_number=ic_number)
            parent = Parent.objects.get(student=student)
            user = parent.user
            
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'student_id': student.id,
                    'student_name': student.name,
                    'student_ic': student.ic_number,
                    'belt_rank': student.get_belt_rank_display(),
                    'school_name': student.school.name
                })
            else:
                return Response({'error': 'Invalid password'}, status=400)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent account not set up. Contact coach.'}, status=404)

class ParentStudentView(APIView):
    """Get student details for logged in parent"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            parent = Parent.objects.get(user=request.user)
            serializer = StudentSerializer(parent.student)
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent profile not found'}, status=404)

class ParentFeesView(APIView):
    """Get student fees for logged in parent"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            parent = Parent.objects.get(user=request.user)
            fees = parent.student.fees.all()
            serializer = FeeSerializer(fees, many=True)
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent profile not found'}, status=404)

# ==================== COACH API ====================

class CoachLoginView(APIView):
    """Coach login using username and password"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if hasattr(user, 'profile') and user.profile.role in ['coach', 'assistant_coach', 'super_admin']:
                    token, created = Token.objects.get_or_create(user=user)
                    
                    schools = user.profile.schools.all()
                    school_list = [{'id': s.id, 'name': s.name} for s in schools]
                    
                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'username': user.username,
                        'role': user.profile.role,
                        'schools': school_list
                    })
                else:
                    return Response({'error': 'Not authorized as coach'}, status=403)
            else:
                return Response({'error': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class CoachStudentsView(APIView):
    """Get all students from coach's schools"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        if request.user.profile.role == 'super_admin':
            schools = School.objects.all()
        else:
            schools = request.user.profile.schools.all()
        
        students = Student.objects.filter(school__in=schools, is_active=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Register new student"""
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        school_id = request.data.get('school')
        try:
            school = School.objects.get(id=school_id)
            
            if request.user.profile.role != 'super_admin':
                if school not in request.user.profile.schools.all():
                    return Response({'error': 'You do not have access to this school'}, status=403)
            
            student = Student.objects.create(
                student_id=request.data.get('student_id'),
                name=request.data.get('name'),
                ic_number=request.data.get('ic_number'),
                date_of_birth=request.data.get('date_of_birth'),
                gender=request.data.get('gender'),
                school=school,
                belt_rank=request.data.get('belt_rank', 'white'),
                phone=request.data.get('phone'),
                email=request.data.get('email', ''),
                address=request.data.get('address', ''),
                emergency_contact=request.data.get('emergency_contact'),
                emergency_name=request.data.get('emergency_name')
            )
            
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=201)
            
        except School.DoesNotExist:
            return Response({'error': 'School not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class CoachFeesView(APIView):
    """Get and update fees for coach's schools"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        student_id = request.query_params.get('student_id')
        
        if request.user.profile.role == 'super_admin':
            schools = School.objects.all()
        else:
            schools = request.user.profile.schools.all()
        
        if student_id:
            fees = Fee.objects.filter(student_id=student_id, student__school__in=schools)
        else:
            fees = Fee.objects.filter(student__school__in=schools)
        
        serializer = FeeSerializer(fees, many=True)
        return Response(serializer.data)
    
    def put(self, request):
        """Update fee payment"""
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        fee_id = request.data.get('fee_id')
        paid_date = request.data.get('paid_date')
        receipt_number = request.data.get('receipt_number', '')
        
        try:
            fee = Fee.objects.get(id=fee_id)
            
            if request.user.profile.role != 'super_admin':
                if fee.student.school not in request.user.profile.schools.all():
                    return Response({'error': 'You do not have access to this student'}, status=403)
            
            fee.paid_date = paid_date if paid_date else None
            fee.receipt_number = receipt_number
            fee.save()
            
            serializer = FeeSerializer(fee)
            return Response(serializer.data)
            
        except Fee.DoesNotExist:
            return Response({'error': 'Fee record not found'}, status=404)

class CoachAttendanceView(APIView):
    """Mark attendance for students"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        student_id = request.data.get('student_id')
        date = request.data.get('date')
        class_type = request.data.get('class_type')
        instructor = request.data.get('instructor')
        
        try:
            student = Student.objects.get(id=student_id)
            
            if request.user.profile.role != 'super_admin':
                if student.school not in request.user.profile.schools.all():
                    return Response({'error': 'You do not have access to this student'}, status=403)
            
            from attendance.models import Attendance
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=date,
                defaults={
                    'class_type': class_type,
                    'instructor': instructor or request.user.username
                }
            )
            
            if not created:
                attendance.class_type = class_type
                attendance.instructor = instructor or request.user.username
                attendance.save()
            
            from attendance.serializers import AttendanceSerializer
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)
            
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class CoachSchoolsView(APIView):
    """Get schools assigned to coach"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin']:
            return Response({'error': 'Not authorized'}, status=403)
        
        if request.user.profile.role == 'super_admin':
            schools = School.objects.filter(is_active=True)
        else:
            schools = request.user.profile.schools.filter(is_active=True)
        
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)


# ==================== DASHBOARD API ====================

class DashboardView(APIView):
    """Dashboard with statistics and charts"""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        current_year = datetime.now().year
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Get user's schools
        if hasattr(request.user, 'profile') and request.user.profile.role == 'super_admin':
            schools = School.objects.filter(is_active=True)
        else:
            schools = request.user.profile.schools.filter(is_active=True)
        
        # Total students per school
        students_per_school = []
        for school in schools:
            students_per_school.append({
                'school': school.name,
                'count': Student.objects.filter(school=school, is_active=True).count()
            })
        
        # Monthly fee collection per school
        monthly_fees = []
        for school in schools:
            fees = Fee.objects.filter(
                student__school=school,
                fee_type='monthly',
                status='paid',
                paid_date__year=current_year
            )
            
            months = [0] * 12
            for fee in fees:
                if fee.paid_date:
                    month = fee.paid_date.month - 1
                    months[month] += float(fee.amount)
            
            monthly_fees.append({
                'school': school.name,
                'months': months
            })
        
        # ===== COLLECTION BREAKDOWN (by school and month) =====
        collection_breakdown = []
        
        for school in schools:
            for month_index in range(12):
                total = 0
                fees = Fee.objects.filter(
                    student__school=school,
                    fee_type='monthly',
                    status='paid',
                    paid_date__year=current_year,
                    paid_date__month=month_index + 1
                )
                for fee in fees:
                    total += float(fee.amount)
                
                if total > 0:
                    collection_breakdown.append({
                        'school': school.name,
                        'month': month_names[month_index],
                        'month_number': month_index + 1,
                        'amount': total
                    })
        
        # Sort by month number (ascending)
        collection_breakdown.sort(key=lambda x: x['month_number'])
        
        # ===== PENDING FEES BY SCHOOL =====
        pending_by_school = []
        for school in schools:
            pending_count = Fee.objects.filter(
                student__school=school,
                fee_type='monthly',
                status='pending',
                due_date__year=current_year
            ).count()
            
            if pending_count > 0:
                pending_by_school.append({
                    'school_id': school.id,
                    'school': school.name,
                    'pending_count': pending_count
                })
        
        # ===== OVERDUE FEES BY SCHOOL =====
        overdue_by_school = []
        for school in schools:
            overdue_count = Fee.objects.filter(
                student__school=school,
                fee_type='monthly',
                status='overdue'
            ).count()
            
            if overdue_count > 0:
                overdue_by_school.append({
                    'school_id': school.id,
                    'school': school.name,
                    'overdue_count': overdue_count
                })
        
        # ===== PENDING FEES DETAILS (by student, for when school is clicked) =====
        pending_details = {}
        fees_pending = Fee.objects.filter(
            fee_type='monthly',
            status='pending',
            due_date__year=current_year
        ).order_by('due_date')
        
        for fee in fees_pending:
            school_name = fee.student.school.name
            if school_name not in pending_details:
                pending_details[school_name] = []
            pending_details[school_name].append({
                'student': fee.student.name,
                'student_id': fee.student.student_id,
                'month': fee.month.strftime('%B %Y') if fee.month else '-',
                'amount': float(fee.amount),
                'due_date': fee.due_date
            })
        
        # ===== OVERDUE FEES DETAILS (by student, for when school is clicked) =====
        overdue_details = {}
        fees_overdue = Fee.objects.filter(
            fee_type='monthly',
            status='overdue'
        ).order_by('due_date')
        
        for fee in fees_overdue:
            school_name = fee.student.school.name
            if school_name not in overdue_details:
                overdue_details[school_name] = []
            overdue_details[school_name].append({
                'student': fee.student.name,
                'student_id': fee.student.student_id,
                'month': fee.month.strftime('%B %Y') if fee.month else '-',
                'amount': float(fee.amount),
                'due_date': fee.due_date
            })
        
        # Fee collection summary
        total_collected = Fee.objects.filter(
            status='paid',
            fee_type='monthly',
            paid_date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_pending = Fee.objects.filter(
            status='pending',
            fee_type='monthly',
            due_date__year=current_year
        ).count()
        
        total_overdue = Fee.objects.filter(
            status='overdue',
            fee_type='monthly'
        ).count()
        
        total_students = Student.objects.filter(is_active=True).count()
        
        # Recent payments
        recent_payments = Fee.objects.filter(
            status='paid'
        ).order_by('-paid_date')[:10]
        
        recent_payments_data = []
        for fee in recent_payments:
            recent_payments_data.append({
                'student': fee.student.name,
                'amount': float(fee.amount),
                'paid_date': fee.paid_date,
                'school': fee.student.school.name
            })
        
        return Response({
            'summary': {
                'total_students': total_students,
                'total_collected': total_collected,
                'total_pending': total_pending,
                'total_overdue': total_overdue,
            },
            'students_per_school': students_per_school,
            'monthly_fees': monthly_fees,
            'recent_payments': recent_payments_data,
            'collection_breakdown': collection_breakdown,
            'pending_by_school': pending_by_school,
            'overdue_by_school': overdue_by_school,
            'pending_details': pending_details,
            'overdue_details': overdue_details,
            'current_year': current_year
        })

# ==================== DASHBOARD PAGE (HTML) ====================

class DashboardPageView(LoginRequiredMixin, TemplateView):
    """Dashboard HTML page - requires admin login"""
    template_name = 'students/dashboard.html'
    login_url = '/admin/login/'