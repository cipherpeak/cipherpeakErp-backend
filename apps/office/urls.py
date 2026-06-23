

from django.urls import path
from .views import *

urlpatterns = [
    path('notes/', NoteListAndCreateView.as_view(), name='note-list'),
    path('notes/<int:note_id>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:note_id>/edit/', NoteEditView.as_view(), name='note-edit'),
    path('notes/<int:note_id>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('notes/<int:note_id>/mark-done/', NoteMarkDoneView.as_view(), name='note-mark-done'),
    
    # Meeting URLs
    path('meetings/create/', MeetingCreateAPIView.as_view(), name='meeting-create'),
    path('meetings/list/', MeetingListAPIView.as_view(), name='meeting-list'),
    path('meetings/<int:meeting_id>/', MeetingDetailAPIView.as_view(), name='meeting-detail'),
    path('employees/list/', EmployeeListAPIView.as_view(), name='employee-list'),
]
