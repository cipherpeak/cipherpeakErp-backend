from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from apps.authapp.models import Employee
from apps.task.models import ServiceAdvantage, PLU
from apps.home.utils import validate_employee_status
from apps.task.serializers import AdvantageSerializer, AdvantageCreateSerializer, AdvantageStartTaskDetailSerializer, AdvantageCompleteTaskSerializer,AdvantageDetailSerializer, PLUSerializer






class AdvantageTaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employee = request.user
        
        try:
            # Filter tasks where the related task has the employee
            advantage_tasks = ServiceAdvantage.objects.filter(
                task__employee=employee
            ).select_related('task').order_by('-task__priority', '-task__created_at')[:7]
            
            # Serialize all tasks
            serializer = AdvantageSerializer(advantage_tasks, many=True)
            
            response_data = {
                'tasks': serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class CreateAdvantageTaskView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            employee = request.user
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        request_data = request.data.copy()
        request_data['employee'] = employee.id
        if hasattr(request_data, 'setlist'):
            images = request.FILES.getlist('images')
            if images:
                request_data.setlist('images', images)

        serializer = AdvantageCreateSerializer(data=request_data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            
            response_data = {
                "message": "Advantage task created successfully",
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdvantageTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            advantage_task = ServiceAdvantage.objects.get(pk=pk)
        except ServiceAdvantage.DoesNotExist:
            return Response(
                {"error": "Advantage task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AdvantageDetailSerializer(advantage_task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class AdvantageStartTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = ServiceAdvantage.objects.get(id=task_id)
        
            serializer = AdvantageStartTaskDetailSerializer(
                task, 
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ServiceAdvantage.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )     



class StartAdvantageTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            advantage_task = ServiceAdvantage.objects.select_related('task').get(pk=pk)
        except ServiceAdvantage.DoesNotExist:
            return Response({"error": "Advantage task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if task belongs to user
        if advantage_task.task.employee != request.user:
             return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "starting a task")
        if not is_allowed:
            return response

        if advantage_task.task.status == 'not_started':
            advantage_task.task.status = 'in_progress'
            advantage_task.task.save()
            advantage_task.started_at = timezone.localtime(timezone.now())
            advantage_task.save()
        
        return Response({"message": "Advantage task started successfully"}, status=status.HTTP_200_OK)


class CompleteAdvantageTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            advantage_task = ServiceAdvantage.objects.select_related('task').get(pk=pk)
        except ServiceAdvantage.DoesNotExist:
            return Response({"error": "Advantage task not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "completing a task")
        if not is_allowed:
            return response

        serializer = AdvantageCompleteTaskSerializer(advantage_task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Update Task Status
            advantage_task.task.status = 'completed'
            advantage_task.task.save()
            
            advantage_task.completed_at = timezone.localtime(timezone.now())
            advantage_task.save()
            
            return Response({"message": "Task completed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PLUListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            plus = PLU.objects.all().order_by('category', 'plu')
            serializer = PLUSerializer(plus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )