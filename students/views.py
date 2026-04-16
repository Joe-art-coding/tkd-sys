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
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.shortcuts import redirect
from datetime import datetime, date
from .models import Student, Parent
from fees.models import Fee
from schools.models import School, UserProfile, Club
from .serializers import StudentSerializer, FeeSerializer, ParentSerializer, SchoolSerializer


def get_user_club(request):
    """Helper function to get the current club from request"""
    return getattr(request, 'club', None)


def filter_by_club(queryset, club, field_name='club'):
    """Helper function to filter any queryset by club"""
    if club:
        return queryset.filter(**{field_name: club})
    return queryset


# ==================== STUDENT VIEWSET ====================

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        club = get_user_club(self.request)
        queryset = Student.objects.filter(is_active=True)
        return filter_by_club(queryset, club)

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
                club = get_user_club(request)
                queryset = Student.objects.filter(ic_number=ic_number)
                if club:
                    queryset = queryset.filter(club=club)
                student = queryset.first()
                if student:
                    serializer = self.get_serializer(student)
                    return Response(serializer.data)
                return Response({'error': 'Student not found'}, status=404)
            except Exception:
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
                    'school_name': student.school.name,
                    'club_name': student.club.name if student.club else '',
                    'club_logo': student.club.logo.url if student.club and student.club.logo else '',
                    'club_primary_color': student.club.primary_color if student.club else '#667eea',
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
            data = serializer.data
            # Add club info
            if parent.student.club:
                data['club_name'] = parent.student.club.name
                data['club_logo'] = parent.student.club.logo.url if parent.student.club.logo else ''
                data['club_primary_color'] = parent.student.club.primary_color
            return Response(data)
        except Parent.DoesNotExist:
            return Response({'error': 'Parent profile not found'}, status=404)


class ParentFeesView(APIView):
    """Get student fees for logged in parent"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all parent records for this user (support multiple children)
            parents = Parent.objects.filter(user=request.user)
            if not parents.exists():
                return Response({'error': 'Parent profile not found'}, status=404)

            # Get student_id from query parameter (if specified)
            student_id = request.query_params.get('student_id')

            if student_id:
                # Show fees for specific student
                parent = parents.filter(student_id=student_id).first()
                if not parent:
                    return Response({'error': 'Student not found for this parent'}, status=404)
                fees = parent.student.fees.all()
                current_student = parent.student
            else:
                # Show fees for first student (fallback)
                fees = parents.first().student.fees.all()
                current_student = parents.first().student

            # Serialize fees with additional receipt info
            fees_data = []
            for fee in fees:
                fee_dict = {
                    'id': fee.id,
                    'month': fee.month,
                    'fee_type': fee.fee_type,  # ADD THIS
                    'fee_type_display': fee.get_fee_type_display(),  # ADD THIS
                    'amount': str(fee.amount),
                    'due_date': fee.due_date,
                    'status': fee.status,
                    'paid_date': fee.paid_date if hasattr(fee, 'paid_date') else None,
                    'can_download': fee.status == 'paid',  # Receipt available only for paid fees
                }
                fees_data.append(fee_dict)

            return Response(fees_data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ParentAttendanceView(APIView):
    """Get attendance history for logged in parent"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            from attendance.models import Attendance
            from attendance.serializers import AttendanceSerializer

            # Get all parent records for this user
            parents = Parent.objects.filter(user=request.user)
            if not parents.exists():
                return Response({'error': 'Parent profile not found'}, status=404)

            # Get student_id from query parameter (if specified)
            student_id = request.query_params.get('student_id')

            if student_id:
                # Show attendance for specific student
                parent = parents.filter(student_id=student_id).first()
                if not parent:
                    return Response({'error': 'Student not found for this parent'}, status=404)
                attendance = Attendance.objects.filter(student=parent.student).order_by('-date')
            else:
                # Show attendance for first student (fallback)
                attendance = Attendance.objects.filter(student=parents.first().student).order_by('-date')

            serializer = AttendanceSerializer(attendance, many=True)

            # Calculate statistics
            total_present = attendance.filter(is_present=True).count()
            total_absent = attendance.filter(is_present=False).count()
            total_records = attendance.count()
            attendance_rate = round((total_present / total_records * 100) if total_records > 0 else 0)

            return Response({
                'attendance': serializer.data,
                'stats': {
                    'total_present': total_present,
                    'total_absent': total_absent,
                    'total_records': total_records,
                    'attendance_rate': attendance_rate
                }
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)


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
                if hasattr(user, 'profile') and user.profile.role in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
                    token, created = Token.objects.get_or_create(user=user)

                    # Get schools filtered by user's club
                    if user.profile.role == 'super_admin':
                        schools = School.objects.filter(is_active=True)
                    else:
                        schools = user.profile.schools.filter(is_active=True)
                        if user.profile.club:
                            schools = schools.filter(club=user.profile.club)

                    school_list = [{'id': s.id, 'name': s.name} for s in schools]

                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'username': user.username,
                        'role': user.profile.role,
                        'schools': school_list,
                        'club_id': user.profile.club.id if user.profile.club else None,
                        'club_name': user.profile.club.name if user.profile.club else None,
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
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
            return Response({'error': 'Not authorized'}, status=403)

        if request.user.profile.role == 'super_admin':
            schools = School.objects.all()
        else:
            schools = request.user.profile.schools.all()
            # Filter by club
            if request.user.profile.club:
                schools = schools.filter(club=request.user.profile.club)

        students = Student.objects.filter(school__in=schools, is_active=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Register new student"""
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
            return Response({'error': 'Not authorized'}, status=403)

        school_id = request.data.get('school')
        try:
            school = School.objects.get(id=school_id)

            # Check club access
            if request.user.profile.role != 'super_admin':
                if school not in request.user.profile.schools.all():
                    return Response({'error': 'You do not have access to this school'}, status=403)

            # Get club from school
            club = school.club

            student = Student.objects.create(
                student_id=request.data.get('student_id'),
                name=request.data.get('name'),
                ic_number=request.data.get('ic_number'),
                date_of_birth=request.data.get('date_of_birth'),
                gender=request.data.get('gender'),
                school=school,
                club=club,  # Assign to club
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
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
            return Response({'error': 'Not authorized'}, status=403)

        student_id = request.query_params.get('student_id')

        if request.user.profile.role == 'super_admin':
            schools = School.objects.all()
        else:
            schools = request.user.profile.schools.all()
            if request.user.profile.club:
                schools = schools.filter(club=request.user.profile.club)

        if student_id:
            fees = Fee.objects.filter(student_id=student_id, student__school__in=schools)
        else:
            fees = Fee.objects.filter(student__school__in=schools)

        serializer = FeeSerializer(fees, many=True)
        return Response(serializer.data)

    def put(self, request):
        """Update fee payment"""
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
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
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
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
                    'instructor': instructor or request.user.username,
                    'is_present': True
                }
            )

            if not created:
                attendance.class_type = class_type
                attendance.instructor = instructor or request.user.username
                attendance.is_present = True
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
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['coach', 'assistant_coach', 'super_admin', 'club_admin']:
            return Response({'error': 'Not authorized'}, status=403)

        if request.user.profile.role == 'super_admin':
            schools = School.objects.filter(is_active=True)
        else:
            schools = request.user.profile.schools.filter(is_active=True)
            if request.user.profile.club:
                schools = schools.filter(club=request.user.profile.club)

        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)


# ==================== DASHBOARD API ====================

class DashboardView(APIView):
    """Dashboard with statistics and charts - filtered by club"""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_year = datetime.now().year
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Get current club from request
        current_club = get_user_club(request)

        # Get user's schools
        if hasattr(request.user, 'profile') and request.user.profile.role == 'super_admin':
            schools = School.objects.filter(is_active=True)
            if current_club:
                schools = schools.filter(club=current_club)
        else:
            schools = request.user.profile.schools.filter(is_active=True)
            if current_club:
                schools = schools.filter(club=current_club)

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

        # Collection breakdown
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

        collection_breakdown.sort(key=lambda x: x['month_number'])

        # Pending fees by school
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

        # Overdue fees by school
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

        # Pending fees details
        pending_details = {}
        fees_pending = Fee.objects.filter(
            fee_type='monthly',
            status='pending',
            due_date__year=current_year,
            student__school__in=schools
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

        # Overdue fees details
        overdue_details = {}
        fees_overdue = Fee.objects.filter(
            fee_type='monthly',
            status='overdue',
            student__school__in=schools
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
            paid_date__year=current_year,
            student__school__in=schools
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_pending = Fee.objects.filter(
            status='pending',
            fee_type='monthly',
            due_date__year=current_year,
            student__school__in=schools
        ).count()

        total_overdue = Fee.objects.filter(
            status='overdue',
            fee_type='monthly',
            student__school__in=schools
        ).count()

        total_students = Student.objects.filter(is_active=True, school__in=schools).count()

        # Recent payments
        recent_payments = Fee.objects.filter(
            status='paid',
            student__school__in=schools
        ).order_by('-paid_date')[:10]

        recent_payments_data = []
        for fee in recent_payments:
            recent_payments_data.append({
                'student': fee.student.name,
                'amount': float(fee.amount),
                'paid_date': fee.paid_date,
                'school': fee.student.school.name
            })

        # Club info for response
        club_info = {}
        if current_club:
            club_info = {
                'id': current_club.id,
                'name': current_club.name,
                'subdomain': current_club.subdomain,
                'primary_color': current_club.primary_color,
                'secondary_color': current_club.secondary_color,
                'logo_url': current_club.logo.url if current_club.logo else '',
            }

        return Response({
            'club': club_info,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_club'] = get_user_club(self.request)
        return context


# ==================== MARTIAL ARTS HOMEPAGE VIEW ====================

class MartialArtsHomeView(TemplateView):
    """Martial arts themed homepage with login modals"""
    template_name = 'students/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_authenticated'] = self.request.user.is_authenticated
        context['current_club'] = get_user_club(self.request)
        return context


# ==================== PARENT DASHBOARD PAGE ====================

class ParentDashboardView(TemplateView):
    """Parent dashboard showing list of children, fees, attendance, schedule, and contact info"""
    template_name = 'students/parent_fee_display.html'

    def post(self, request, *args, **kwargs):
        ic_number = request.POST.get('ic')
        password = request.POST.get('password')
        selected_student_id = request.POST.get('student_id')

        if not ic_number or not password:
            return redirect('/')

        try:
            student = Student.objects.get(ic_number=ic_number)
            parent = Parent.objects.get(student=student)
            user = parent.user

            if user.check_password(password):
                # Get all children for this parent
                all_children = Parent.objects.filter(user=user).select_related('student')
                children_list = [p.student for p in all_children]

                # Select which child to show
                if selected_student_id:
                    current_student = Student.objects.filter(
                        id=selected_student_id,
                        parent__user=user
                    ).first()
                    if not current_student and children_list:
                        current_student = children_list[0]
                else:
                    # Kalau takde selected_student_id, guna student yang login
                    current_student = student  # ← GUNA STUDENT YANG LOGIN, BUKAN ANAK PERTAMA

                # Get token for API calls
                token, created = Token.objects.get_or_create(user=user)

                # Get attendance records for current student
                attendance_records = []
                attendance_stats = {'present': 0, 'absent': 0, 'rate': 0}

                if current_student:
                    from attendance.models import Attendance

                    all_attendance = Attendance.objects.filter(student=current_student)
                    total_present = all_attendance.filter(is_present=True).count()
                    total_records = all_attendance.count()

                    attendance_stats = {
                        'present': total_present,
                        'absent': total_records - total_present,
                        'rate': round((total_present / total_records * 100) if total_records > 0 else 0)
                    }

                    attendance_records = all_attendance.order_by('-date')[:30]

                # Get class schedule and contact info for parent's club
                class_schedule = []
                contact_info = []

                if current_student and current_student.club:
                    from schools.models import ClassSchedule, ContactInfo

                    class_schedule = ClassSchedule.objects.filter(
                        club=current_student.club,
                        school=current_student.school,
                        is_active=True
                    ).order_by('day', 'start_time')

                    contact_info = ContactInfo.objects.filter(
                        club=current_student.club
                    ).order_by('order')

                context = self.get_context_data(**kwargs)
                context['children'] = children_list
                context['current_student'] = current_student
                context['student_name'] = current_student.name if current_student else ''
                context['student_ic'] = current_student.ic_number if current_student else ''
                context['belt_rank'] = current_student.get_belt_rank_display() if current_student else ''
                context['school_name'] = current_student.school.name if current_student else ''
                context['club_name'] = current_student.club.name if current_student and current_student.club else ''
                context['club_logo'] = current_student.club.logo.url if current_student and current_student.club and current_student.club.logo else ''
                context['club_primary_color'] = current_student.club.primary_color if current_student and current_student.club else '#667eea'
                context['token'] = token.key
                context['attendance_records'] = attendance_records
                context['attendance_stats'] = attendance_stats
                context['class_schedule'] = class_schedule
                context['contact_info'] = contact_info
                return self.render_to_response(context)
            else:
                return redirect('/?error=invalid_password')
        except Student.DoesNotExist:
            return redirect('/?error=student_not_found')
        except Parent.DoesNotExist:
            return redirect('/?error=parent_not_found')

    def get(self, request, *args, **kwargs):
        # Redirect GET requests to home page
        return redirect('/')

