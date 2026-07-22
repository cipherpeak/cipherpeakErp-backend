from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.organization.models import Company, Branch, Department
from apps.hr.models import Employee, LeaveRequest, EmpDocument
from apps.system.models import SystemUser
from .models import Notification, Announcement
from .serializers import NotificationSerializer, AnnouncementSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing system alerts/notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """
        Mark all notifications as read.
        """
        Notification.objects.filter(read=False).update(read=True)
        return Response({'message': 'All notifications marked as read'}, status=status.HTTP_200_OK)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing announcements.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]


class DashboardAPIView(APIView):
    """
    API endpoint returning dashboard metrics, recent leave requests, 
    unread notifications/alerts, and pinned announcements.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Calculate stats metrics
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status='active').count()
        pending_leave = LeaveRequest.objects.filter(status='pending').count()
        unread_notifs = Notification.objects.filter(read=False).count()
        expiring_docs = EmpDocument.objects.filter(status__in=['expiring', 'expired']).count()
        active_users = SystemUser.objects.filter(status='active').count()
        total_users = SystemUser.objects.count()

        # 2. Get organization component counts
        companies_count = Company.objects.count()
        branches_count = Branch.objects.count()
        departments_count = Department.objects.count()

        # 3. Get recent leave requests (limit 6)
        recent_leaves_queryset = LeaveRequest.objects.select_related('employee').order_by('-id')[:6]
        recent_leave = []
        for r in recent_leaves_queryset:
            recent_leave.append({
                'id': r.id,
                'emp_name': r.employee.name if r.employee else 'Unknown',
                'avatar_initials': r.employee.avatar_initials if r.employee else '',
                'avatar_color': r.employee.avatar_color if r.employee else 'from-brand/20 to-brand/5 text-brand',
                'type': r.type,
                'days': float(r.days),
                'from_date': r.start_date.strftime('%Y-%m-%d') if r.start_date else None,
                'status': r.status,
            })

        # 4. Get unread notifications/alerts (limit 5)
        unread_alerts_queryset = Notification.objects.filter(read=False).order_by('-time')[:5]
        unread_alerts_data = NotificationSerializer(unread_alerts_queryset, many=True).data

        # 5. Get pinned and published announcements
        pinned_announcements_queryset = Announcement.objects.filter(pinned=True, status='published').order_by('-publish_date', '-id')[:2]
        pinned_announcements_data = AnnouncementSerializer(pinned_announcements_queryset, many=True).data

        return Response({
            'stats': {
                'totalEmployees': total_employees,
                'activeEmployees': active_employees,
                'pendingLeave': pending_leave,
                'unreadNotifs': unread_notifs,
                'expiringDocs': expiring_docs,
                'activeUsers': active_users,
                'totalUsers': total_users,
            },
            'recentLeave': recent_leave,
            'unreadNotifs': unread_alerts_data,
            'pinnedAnnouncements': pinned_announcements_data,
            'orgOverview': {
                'companies': companies_count,
                'branches': branches_count,
                'departments': departments_count,
            }
        }, status=status.HTTP_200_OK)
