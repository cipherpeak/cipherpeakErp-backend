from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.task.serializers import (
    DaxTaskCreateSerializer, DaxTaskListSerializer, DaxTaskDetailSerializer,
    DaxTaskStartDetailSerializer, DaxCompleteTaskSerializer
)
from apps.authapp.models import Employee
from apps.task.models import ServiceTaskDax, ServiceDaxTypes
from apps.home.utils import validate_employee_status
from django.utils import timezone

import json
class CreateDaxTaskView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        employee = request.user
        data = request.data.copy()
        
        # Prepare data for serializer
        serializer_data = data
        service_types_raw = data.get('service_types')
        if isinstance(service_types_raw, str):
            try:
                parsed = json.loads(service_types_raw)
                if isinstance(parsed, (list, dict)):
                    # We can't easily put nested structures into QueryDict.
                    # So we convert everything to a regular dict for the serializer.
                    serializer_data = data.dict()
                    serializer_data['service_types'] = parsed
                    # Re-add lists that might have been lost in .dict()
                    if hasattr(data, 'getlist'):
                        if 'invoice_images' in data:
                            serializer_data['invoice_images'] = data.getlist('invoice_images')
            except json.JSONDecodeError:
                pass

        if hasattr(data, 'getlist') and serializer_data is data:
             # If we didn't switch to a dict, handle image list in QueryDict
            invoice_images = request.FILES.getlist('invoice_images')
            if invoice_images:
                data.setlist('invoice_images', invoice_images)

        serializer = DaxTaskCreateSerializer(data=serializer_data, context={'employee': employee})
        
        if serializer.is_valid():
            serializer.save()
            
            response_data = {
                "message": "Dax task created successfully",
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DaxTaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        employee = request.user
        
        dax_tasks = ServiceTaskDax.objects.filter(task__employee=employee).order_by('-created_at')[:7]
        
        serializer = DaxTaskListSerializer(dax_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DaxTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            dax_task = ServiceTaskDax.objects.get(pk=pk)
        except ServiceTaskDax.DoesNotExist:
            return Response({"error": "Dax task not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = DaxTaskDetailSerializer(dax_task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class StartDaxTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            dax_task = ServiceTaskDax.objects.select_related('task').get(pk=pk)
        except ServiceTaskDax.DoesNotExist:
            return Response({"error": "Dax task not found"}, status=status.HTTP_404_NOT_FOUND)


        if dax_task.task.employee != request.user:
             return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "starting a task")
        if not is_allowed:
            return response

        if dax_task.task.status == 'not_started':
            dax_task.task.status = 'in_progress'
            dax_task.task.save()
            dax_task.started_at = timezone.localtime(timezone.now())
            dax_task.save()
        
        return Response({"message": "Task started successfully"}, status=status.HTTP_200_OK)



class DaxTaskStartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = ServiceTaskDax.objects.get(id=task_id)
        
            serializer = DaxTaskStartDetailSerializer(
                task, 
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ServiceTaskDax.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )     




class CompleteDaxServiceTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            service_type = ServiceDaxTypes.objects.get(pk=pk)
        except ServiceDaxTypes.DoesNotExist:
            return Response({"error": "Service type not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check authorization - only the employee assigned to the task can complete it
        if service_type.dax_service.task.employee != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        service_type.completed = True
        service_type.save()

        return Response({"message": "Service type marked as completed"}, status=status.HTTP_200_OK)




class CompleteDaxTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            dax_task = ServiceTaskDax.objects.select_related('task').get(pk=pk)
        except ServiceTaskDax.DoesNotExist:
            return Response({"error": "Dax task not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check authorization
        if dax_task.task.employee != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Check status (Attendance + Break)
        is_allowed, response = validate_employee_status(request.user, "completing a task")
        if not is_allowed:
            return response

        serializer = DaxCompleteTaskSerializer(dax_task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Update Task Status
            dax_task.task.status = 'completed'
            dax_task.task.save()
            
            dax_task.completed_at = timezone.localtime(timezone.now())
            dax_task.save()
            
            return Response({"message": "Task completed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)