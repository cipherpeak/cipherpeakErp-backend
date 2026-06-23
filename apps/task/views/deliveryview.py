from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, date, time
from apps.task.serializers import CompleteDeliveryTaskSerializer, DeliveryTaskDetailSerializer, DeliveryTaskSerializer, DeliveryTaskStartDetailSerializer, DeliveryNoteSerializer
from apps.task.models import DeliveryTask, Task, DeliveryNote, DeliveryTaskImage
from rest_framework.permissions import IsAuthenticated
from apps.home.utils import validate_employee_status


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.localtime(timezone.now())
        employee = request.user
        
        # Base queryset - don't slice yet
        tasks_queryset = Task.objects.select_related(
            'employee', 'delivery_details'
        ).order_by('-priority', '-created_at')
        
        if employee:
            tasks_queryset = tasks_queryset.filter(employee=employee)
        
        # Apply all filters BEFORE slicing
        today_tasks_qs = tasks_queryset.filter(
            ~Q(status__in=['completed', 'delivered']) & 
            (
                Q(delivery_details__due_date=now.date()) |  
                Q(delivery_details__task_assign_datetime__date=now.date())
            )
        ).distinct()
        
        pending_tasks_qs = tasks_queryset.filter(
            ~Q(status__in=['completed', 'delivered']) &  
            ~Q(id__in=today_tasks_qs.values('id')) &  
            (
                Q(delivery_details__due_date__gt=now.date()) | 
                Q(delivery_details__due_date__isnull=True) 
            )
        ).distinct()
        
        completed_tasks_qs = tasks_queryset.filter(
            Q(status__in=['completed', 'delivered']) &
            Q(delivery_details__task_completed_date=now.date())  
        ).distinct()
        
        # Slice each queryset separately (limit to 7 per category)
        today_tasks = today_tasks_qs[:7]
        pending_tasks = pending_tasks_qs[:7]
        completed_tasks = completed_tasks_qs[:7]
        
        today_delivery_tasks = DeliveryTask.objects.filter(
            task__in=today_tasks
        ).select_related('task')
        
        pending_delivery_tasks = DeliveryTask.objects.filter(
            task__in=pending_tasks
        ).select_related('task')
        
        completed_delivery_tasks = DeliveryTask.objects.filter(
            task__in=completed_tasks
        ).select_related('task')
        
        today_serializer = DeliveryTaskSerializer(today_delivery_tasks, many=True)
        pending_serializer = DeliveryTaskSerializer(pending_delivery_tasks, many=True)
        completed_serializer = DeliveryTaskSerializer(completed_delivery_tasks, many=True)
        
        response_data = {
            'today_tasks': today_serializer.data,
            'pending_tasks': pending_serializer.data,
            'completed_tasks': completed_serializer.data,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    


from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404

class TaskDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryTaskDetailSerializer
    
    def get_object(self):
        delivery_id = self.kwargs.get('delivery_id')
        
        employee = self.request.user
        
        delivery_task = get_object_or_404(
            DeliveryTask.objects.select_related('task'),
            id=delivery_id,
            task__employee=employee
        )
        
        return delivery_task
    





class StartTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, delivery_id):
        try:
            task = DeliveryTask.objects.get(id=delivery_id)

            # Check status (Attendance + Break)
            is_allowed, response = validate_employee_status(request.user, "starting a task")
            if not is_allowed:
                return response
            
            if task.task.status == 'in_progress':
                return Response(
                    {"error": "Task is already in progress"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if task.task.status in ['completed', 'delivered']:
                return Response(
                    {"error": f"Cannot start task that is already {task.status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            task.task.status = 'in_progress'
            task.task_start_datetime = timezone.localtime(timezone.now())

            task.save()
            task.task.save()
            
            return Response(
                {"message": "task started"},
                status=status.HTTP_200_OK
            )
            
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class StartTaskDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = DeliveryTask.objects.get(id=task_id)
        
            serializer = DeliveryTaskStartDetailSerializer(
                task, 
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

from rest_framework.parsers import MultiPartParser, FormParser
import os

class CompleteDeliveryTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  
    
    def post(self, request, delivery_id):
        try:
            delivery_task = DeliveryTask.objects.get(id=delivery_id)
            
            # Check status (Attendance + Break)
            is_allowed, response = validate_employee_status(request.user, "completing a task")
            if not is_allowed:
                return response

            if delivery_task.task.status != 'in_progress':
                return Response(
                    {
                        "error": f"Task must be in progress to complete. Current status: {delivery_task.task.status}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = CompleteDeliveryTaskSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            images = serializer.validated_data.get('images', [])
            if not images and hasattr(request.data, 'getlist'):
                images = request.data.getlist('images')

            notes = serializer.validated_data.get('notes', '')
            status_of_delivery = serializer.validated_data.get('status_of_delivery', '')
            
            delivery_task.status_of_delivery = status_of_delivery
            
            for index, image in enumerate(images):
                filename = f"delivery_{delivery_id}_{int(timezone.localtime(timezone.now()).timestamp())}_{index}{os.path.splitext(image.name)[1]}"
                image.name = filename
                DeliveryTaskImage.objects.create(
                    delivery_task=delivery_task,
                    image=image
                )

            if notes:
                delivery_task.delivery_notes = notes 

            
            current_time = timezone.localtime(timezone.now())

            delivery_task.task_completed_date = current_time.date()
            delivery_task.task_completed_time = current_time.time()
            
            delivery_task.task.status = 'delivered'
            
            delivery_task.save()
            delivery_task.task.save()
            
            # Prepare response
            response_data = {
                "message": "Task completed successfully",
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except DeliveryTask.DoesNotExist:
            return Response(
                {"error": "Delivery task not found or you are not authorized"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeliveryNoteListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            delivery_task_id = request.GET.get('delivery_task_id')
            if delivery_task_id:
                notes = DeliveryNote.objects.filter(delivery_task_id=delivery_task_id).order_by('-created_at')
            else:
                # Get all notes for tasks assigned to the current employee
                notes = DeliveryNote.objects.filter(
                    delivery_task__task__employee=request.user
                ).order_by('-created_at')
            serializer = DeliveryNoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = DeliveryNoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"note created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )