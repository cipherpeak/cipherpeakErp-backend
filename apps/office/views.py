from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from apps.home.models import AttendanceCheck, BreakTimer
from .models import Note, Meeting
from apps.authapp.models import Employee
from .serializers import (
    NoteSerializer, 
    NoteCreateSerializer, 
    NoteDetailSerializer,
    NoteUpdateSerializer,
    MeetingCreateSerializer,
    MeetingListSerializer,
    EmployeeListSerializer,
    MeetingListDetailSerializer
)
from apps.home.utils import validate_employee_status



class NoteListAndCreateView(APIView):

    permission_classes = [IsAuthenticated]
    
    def parse_date(self, date_str):
        from datetime import datetime
        date_formats = [
            '%d %B %Y', '%d-%b-%Y', '%Y-%m-%d', '%d/%m/%Y',
            '%m/%d/%Y', '%B %d, %Y', '%d %b %Y'
        ]
        
        date_str = date_str.strip()
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # Handle YYYY-M-D format like "2026-1-5"
        import re
        match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
        if match:
            try:
                from datetime import date
                return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError:
                pass
        return None

    def get(self, request):
        try:
            employee = request.user
            notes = Note.objects.filter(
                employee=employee, 
                is_deleted=False
            ).order_by('-created_at')
            
            today = timezone.localdate()
            
            today_notes = []
            future_notes = []
            completed_notes = []
            
            pending_with_dates = []
            
            for note in notes:
                if note.status == 'completed':
                    completed_notes.append(note)
                    continue

                note_date = self.parse_date(note.date)
                pending_with_dates.append((note, note_date))
            
            # Separate past/today notes from future notes
            past_today_pending = []
            
            for note, note_date in pending_with_dates:
                if note_date and note_date > today:
                    future_notes.append(note)
                else:
                    past_today_pending.append((note, note_date))
            
            # Sort past/today notes by date (most recent first, None dates last)
            def sort_by_date(item):
                note_date = item[1]
                if note_date is None:
                    return float('-inf')  # No date goes last
                return (today - note_date).days  # Days ago (0 for today, 1 for yesterday, etc.)
            
            past_today_pending.sort(key=sort_by_date)
            
            for note, note_date in past_today_pending:
                today_notes.append(note)
            
            return Response({
                "success": True,
                "message": "Notes retrieved successfully",
                "today_notes": NoteSerializer(today_notes, many=True).data,
                "future_notes": NoteSerializer(future_notes, many=True).data,
                "completed_notes": NoteSerializer(completed_notes, many=True).data
            }, status=status.HTTP_200_OK)
            
        except Employee.DoesNotExist:
            return Response({
                "success": False,
                "error": "Employee profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error retrieving notes: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            employee = request.user
            

            # Status Validation
            is_allowed, response = validate_employee_status(employee, "creating a note")
            if not is_allowed:
                return response

            serializer = NoteCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                note = Note.objects.create(
                    employee=employee,
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data['description'],
                    date=serializer.validated_data['date']
                )
                
                return Response({
                    "success": True,
                    "message": "Note created successfully",
                }, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return Response({
                    "success": False,
                    "error": "Validation failed",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Employee.DoesNotExist:
            return Response({
                "success": False,
                "error": "Employee profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error creating note: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoteDetailView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_note(self, note_id, employee):
        """Helper method to get note with permission check"""
        try:
            note = Note.objects.get(id=note_id, employee=employee, is_deleted=False)
            return note
        except Note.DoesNotExist:
            return None
    
    def get(self, request, note_id):
        """Get details of a specific note"""
        try:
            employee =request.user
            
            # Get the note
            note = self.get_note(note_id, employee)
            
            if not note:
                return Response({
                    "success": False,
                    "error": "Note not found or you don't have permission to view it"
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = NoteDetailSerializer(note)
            
            return Response({
                "success": True,
                "message": "Note details retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Employee.DoesNotExist:
            return Response({
                "success": False,
                "error": "Employee profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error retrieving note details: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class NoteEditView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_note(self, note_id, employee):
        try:
            note = Note.objects.get(id=note_id, employee=employee, is_deleted=False)
            return note
        except Note.DoesNotExist:
            return None
    
    def put(self, request, note_id):

        try:
            # Get the authenticated employee
            employee = request.user
            
            # Get the note
            note = self.get_note(note_id, employee)
            
            if not note:
                return Response({
                    "success": False,
                    "error": "Note not found or you don't have permission to edit it"
                }, status=status.HTTP_404_NOT_FOUND)

            # Status Validation
            is_allowed, response = validate_employee_status(employee, "editing a note")
            if not is_allowed:
                return response

            # Validate the incoming data (using new specific update serializer)
            serializer = NoteUpdateSerializer(note, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Save only the fields provided in request.data
                serializer.save()
                
                return Response({
                    "success": True,
                    "message": "Note updated successfully",
                }, status=status.HTTP_200_OK)
            else:
                # Return validation errors
                return Response({
                    "success": False,
                    "error": "Validation failed",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Employee.DoesNotExist:
            return Response({
                "success": False,
                "error": "Employee profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error updating note: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class NoteDeleteView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_note(self, note_id, employee):
        """Helper method to get note with permission check"""
        try:
            note = Note.objects.get(id=note_id, employee=employee, is_deleted=False)
            return note
        except Note.DoesNotExist:
            return None
    
    def delete(self, request, note_id):

        try:
            # Get the authenticated employee
            employee = request.user
            
            # Get the note
            note = self.get_note(note_id, employee)
            
            if not note:
                return Response({
                    "success": False,
                    "error": "Note not found or you don't have permission to delete it"
                }, status=status.HTTP_404_NOT_FOUND)

            # Status Validation
            is_allowed, response = validate_employee_status(employee, "deleting a note")
            if not is_allowed:
                return response

            note_title = note.title
            
            # Soft Delete the note
            note.is_deleted = True
            note.save()
            
            return Response({
                "success": True,
                "message": f"Note '{note_title}' deleted successfully",
            }, status=status.HTTP_200_OK)
            
        except Employee.DoesNotExist:
            return Response({
                "success": False,
                "error": "Employee profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error deleting note: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoteMarkDoneView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, note_id):
        """Mark a note as completed"""
        try:
            employee = request.user
            
            # Get the note
            try:
                note = Note.objects.get(id=note_id, employee=employee, is_deleted=False)
            except Note.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Note not found or you don't have permission to modify it"
                }, status=status.HTTP_404_NOT_FOUND)

            # Status Validation
            is_allowed, response = validate_employee_status(employee, "marking a note as done")
            if not is_allowed:
                return response
            
            # Update status and completed_at
            note.status = 'completed'
            note.completed_at = timezone.now()
            note.save()
            
            return Response({
                "success": True,
                "message": f"Note '{note.title}' marked as completed",
                "status": note.status
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error marking note as done: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class EmployeeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only list regular employees for meeting attendees
        employees = Employee.objects.filter(
            is_active=True, 
            role='employee'
        ).exclude(id=request.user.id)
        
        serializer = EmployeeListSerializer(employees, many=True)
        return Response({
            "success": True, 
            "employees": serializer.data
        }, status=status.HTTP_200_OK)


class MeetingCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ['admin', 'super_admin']:
             return Response({
                "success": False,
                "error": "Only admins can schedule meetings"
            }, status=status.HTTP_403_FORBIDDEN)

        # Status Validation
        is_allowed, response = validate_employee_status(request.user, "creating a meeting")
        if not is_allowed:
            return response

        serializer = MeetingCreateSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save(created_by=request.user)
            return Response({
                "success": True,
                "message": "Meeting scheduled successfully",
                "meeting_id": meeting.id
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "error": "Validation failed",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class MeetingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # If user is admin or super_admin, show all meetings
        if user.role in ['admin', 'super_admin']:
            meetings = Meeting.objects.all().order_by('date', 'time')
        else:
            # Get meetings created by user OR meetings where user is an attendee
            meetings = Meeting.objects.filter(
                Q(created_by=user) | Q(attendees=user)
            ).distinct().order_by('date', 'time')
        
        serializer = MeetingListSerializer(meetings, many=True, context={'request': request})
        
        return Response({
            "success": True,
            "meetings": serializer.data
        }, status=status.HTTP_200_OK)


class MeetingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, meeting_id):
        try:
            user = request.user
            
            # Fetch meeting
            meeting = Meeting.objects.get(id=meeting_id)
                        
            is_authorized = (
                user.role in ['admin', 'super_admin'] or 
                meeting.created_by == user or 
                meeting.attendees.filter(id=user.id).exists()
            )
            
            if not is_authorized:
                return Response({
                    "success": False,
                    "error": "You do not have permission to view this meeting"
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = MeetingListDetailSerializer(meeting, context={'request': request})
            
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Meeting.DoesNotExist:
            return Response({
                "success": False,
                "error": "Meeting not found"
            }, status=status.HTTP_404_NOT_FOUND)
