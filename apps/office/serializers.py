from .models import Note, Meeting
from rest_framework import serializers
from apps.authapp.models import Employee
from datetime import datetime
import pytz

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_name', 'profile_pic', 'role', 'employee_type']

class MeetingCreateSerializer(serializers.ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Employee.objects.all(),
        required=True
    )

    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time', 'location', 'agenda', 'attendees']
    
    def validate_attendees(self, value):
        if not value:
            raise serializers.ValidationError("At least one attendee is required")
        return value

class MeetingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = [
            'id', 
            'title', 
            'date', 
            'time', 
            'location', 
        ]


class MeetingListDetailSerializer(serializers.ModelSerializer):
    created_by = EmployeeListSerializer(read_only=True)
    attendees = EmployeeListSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = [
            'id', 
            'title', 
            'date', 
            'time', 
            'location', 
            'agenda', 
            'created_by', 
            'attendees', 
        ]
      


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'description',
            'date',
            'status',
            'created_at',
            'updated_at',
        ]
    

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description', 'date']
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters")
        return value.strip()
    
    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description is required")
        return value.strip()
    
    def validate_date(self, value):
        if not value.strip():
            raise serializers.ValidationError("Date is required")
        return value.strip()


class NoteUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=False)
    description = serializers.CharField(required=False, allow_blank=False)
    date = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = Note
        fields = ['title', 'description', 'date']
    
    def validate_title(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Title cannot be blank")
        return value.strip() if value else value
    
    def validate_description(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Description cannot be blank")
        return value.strip() if value else value


class NoteDetailSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        fields = NoteSerializer.Meta.fields + ['description']