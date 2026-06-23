from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from apps.authapp.models import Employee
from apps.home.utils import validate_employee_status
from apps.task.models import Mechanic, PartNumber

from apps.task.serializers import MechanicSerializer, MechanicCreateSerializer, MechanicCompleteTaskSerializer, MechanicTaskDetailSerializer,MechanicStartTaskDetailSerializer, PartNumberSerializer




class MechanicTaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employee = request.user
        
        try:
            # Get mechanic tasks assigned to this employee
            mechanic_tasks = Mechanic.objects.filter(
                task__employee=employee
            ).select_related('task').order_by('-task__priority', '-task__created_at')[:7]
            
            # Get maintenance tasks (is_maintenance=True)
            maintenance_tasks = Mechanic.objects.filter(
                task__is_maintenance=True
            ).select_related('task').order_by('-task__priority', '-task__created_at')
            
            # Combine both querysets
            all_tasks = mechanic_tasks | maintenance_tasks
            
            # Remove duplicates if any task appears in both sets
            all_tasks = all_tasks.distinct()
            
            # Serialize all tasks
            serializer = MechanicSerializer(all_tasks, many=True)
            
            response_data = {
                'tasks': serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class CreateMechanicTaskView(APIView):

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
        
        serializer = MechanicCreateSerializer(data=request_data, context={'request': request})
        
        if serializer.is_valid():
            mechanic_task = serializer.save()
            
            response_data = {
                "message": "Mechanic task created successfully",
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MechanicTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            mechanic_task = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response(
                {"error": "Mechanic task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MechanicTaskDetailSerializer(mechanic_task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartMechanicTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            mechanic_task = Mechanic.objects.select_related('task').get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({"error": "Mechanic task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "starting a task")
        if not is_allowed:
            return response

        task = mechanic_task.task

        if task.is_maintenance:
            if task.status == 'in_progress':
                if task.employee:
                    return Response(
                        {
                            "error": f"This maintenance task is already being worked on by {task.employee.employee_name or task.employee.employeeId}",
                            "current_worker": {
                                "id": task.employee.id,
                                "employeeId": task.employee.employeeId,
                                "name": task.employee.employee_name
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"error": "This maintenance task is already in progress by another employee"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # If maintenance task is not started, assign it to current employee
            if task.status == 'not_started':
                task.employee = request.user
                task.status = 'in_progress'
                task.save()
                mechanic_task.started_at = timezone.localtime(timezone.now())
                mechanic_task.save()
                
                # Create a record of who started the maintenance task
                MaintenanceTaskAssignment.objects.create(
                    task=task,
                    employee=request.user,
                    started_at=timezone.localtime(timezone.now())
                )
                
                return Response(
                    {
                        "message": "Maintenance task started",
                        "assigned_to_you": True,
                        "task_type": "maintenance"
                    },
                    status=status.HTTP_200_OK
                )
                
        # For non-maintenance tasks (personal tasks)
        else:
            # Check if task belongs to user
            if task.employee != request.user:
                return Response({"error": "Not authorized to start this task"}, status=status.HTTP_403_FORBIDDEN)

            if task.status == 'not_started':
                task.status = 'in_progress'
                task.save()
                mechanic_task.started_at = timezone.localtime(timezone.now())
                mechanic_task.save()
                
                return Response(
                    {
                        "message": "Personal task started",
                        "assigned_to_you": True,
                        "task_type": "personal"
                    },
                    status=status.HTTP_200_OK
                )

        # If task is already in progress
        if task.status == 'in_progress':
            # If it's a maintenance task and this employee is the one working on it
            if task.is_maintenance and task.employee == request.user:
                return Response(
                    {
                        "message": "You are already working on this maintenance task",
                        "already_working": True
                    },
                    status=status.HTTP_200_OK
                )
            elif not task.is_maintenance and task.employee == request.user:
                return Response(
                    {
                        "message": "You are already working on this task",
                        "already_working": True
                    },
                    status=status.HTTP_200_OK
                )

        return Response({"error": "Task cannot be started in its current state"}, status=status.HTTP_400_BAD_REQUEST)



class MechanicStartTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = Mechanic.objects.get(id=task_id)
        
            serializer = MechanicStartTaskDetailSerializer(
                task, 
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Mechanic.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        


class CompleteMechanicTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            mechanic_task = Mechanic.objects.select_related('task').get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({"error": "Mechanic task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "completing a task")
        if not is_allowed:
            return response

        serializer = MechanicCompleteTaskSerializer(mechanic_task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Update Task Status
            mechanic_task.task.status = 'completed'
            mechanic_task.task.save()
            
            mechanic_task.completed_at = timezone.localtime(timezone.now())
            mechanic_task.save()
            
            return Response({"message": "Task completed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartNumberListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            parts = PartNumber.objects.all().order_by('part_number')
            serializer = PartNumberSerializer(parts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )