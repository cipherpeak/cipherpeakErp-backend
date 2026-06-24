from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, AttendanceRecord, LeaveRequest, EmpDocument
from .serializers import EmployeeSerializer, AttendanceRecordSerializer, LeaveRequestSerializer, EmpDocumentSerializer
from . import services


# ===========================================================================
# EMPLOYEE LOGIN
# ===========================================================================

class EmployeeLoginView(APIView):
    """
    POST /api/hr/login/
    Authenticate employee and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        emp_id = request.data.get('emp_id')
        password = request.data.get('password')

        if not emp_id or not password:
            return Response(
                {'error': 'emp_id and password are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Invalid emp_id or password'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not employee.check_password(password):
            return Response(
                {'error': 'Invalid emp_id or password'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not employee.is_active:
            return Response(
                {'error': 'Account is inactive'},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(employee)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'employee': {
                'id': employee.id,
                'emp_id': employee.emp_id,
                'name': employee.name,
                'email': employee.email,
                'department': employee.department,
                'designation': employee.designation,
                'branch': employee.branch,
                'is_staff': employee.is_staff,
            }
        }, status=status.HTTP_200_OK)


# ===========================================================================
# EMPLOYEE VIEWSET
# ===========================================================================

class EmployeeViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Employees to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        employees = services.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        employee = services.create_employee(serializer.validated_data)
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_employee = services.update_employee(employee, serializer.validated_data)
        return Response(EmployeeSerializer(updated_employee).data)

    def partial_update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_employee = services.update_employee(employee, serializer.validated_data)
        return Response(EmployeeSerializer(updated_employee).data)

    def destroy(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        services.deactivate_employee(employee)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# ATTENDANCE VIEWSET
# ===========================================================================

class AttendanceRecordViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Attendance Records to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        attendance = services.get_all_attendance()
        serializer = AttendanceRecordSerializer(attendance, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        attendance = get_object_or_404(AttendanceRecord, pk=pk)
        serializer = AttendanceRecordSerializer(attendance)
        return Response(serializer.data)

    def create(self, request):
        serializer = AttendanceRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        attendance = services.create_attendance(serializer.validated_data)
        return Response(AttendanceRecordSerializer(attendance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        attendance = get_object_or_404(AttendanceRecord, pk=pk)
        serializer = AttendanceRecordSerializer(attendance, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_attendance = services.update_attendance(attendance, serializer.validated_data)
        return Response(AttendanceRecordSerializer(updated_attendance).data)

    def partial_update(self, request, pk=None):
        attendance = get_object_or_404(AttendanceRecord, pk=pk)
        serializer = AttendanceRecordSerializer(attendance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_attendance = services.update_attendance(attendance, serializer.validated_data)
        return Response(AttendanceRecordSerializer(updated_attendance).data)

    def destroy(self, request, pk=None):
        attendance = get_object_or_404(AttendanceRecord, pk=pk)
        services.delete_attendance(attendance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# LEAVE REQUEST VIEWSET
# ===========================================================================

class LeaveRequestViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Leave Requests to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        leave_requests = services.get_all_leave_requests()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data)

    def create(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        leave_request = services.create_leave_request(serializer.validated_data)
        return Response(LeaveRequestSerializer(leave_request).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        serializer = LeaveRequestSerializer(leave_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_leave_request = services.update_leave_request(leave_request, serializer.validated_data)
        return Response(LeaveRequestSerializer(updated_leave_request).data)

    def partial_update(self, request, pk=None):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        serializer = LeaveRequestSerializer(leave_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_leave_request = services.update_leave_request(leave_request, serializer.validated_data)
        return Response(LeaveRequestSerializer(updated_leave_request).data)

    def destroy(self, request, pk=None):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        services.delete_leave_request(leave_request)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# EMPLOYEE DOCUMENT VIEWSET
# ===========================================================================

class EmpDocumentViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Employee Documents to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        documents = services.get_all_documents()
        serializer = EmpDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        document = get_object_or_404(EmpDocument, pk=pk)
        serializer = EmpDocumentSerializer(document)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmpDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document = services.create_document(serializer.validated_data)
        return Response(EmpDocumentSerializer(document).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        document = get_object_or_404(EmpDocument, pk=pk)
        serializer = EmpDocumentSerializer(document, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_document = services.update_document(document, serializer.validated_data)
        return Response(EmpDocumentSerializer(updated_document).data)

    def partial_update(self, request, pk=None):
        document = get_object_or_404(EmpDocument, pk=pk)
        serializer = EmpDocumentSerializer(document, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_document = services.update_document(document, serializer.validated_data)
        return Response(EmpDocumentSerializer(updated_document).data)

    def destroy(self, request, pk=None):
        document = get_object_or_404(EmpDocument, pk=pk)
        services.delete_document(document)
        return Response(status=status.HTTP_204_NO_CONTENT)
