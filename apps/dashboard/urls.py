from django.urls import path
from .views import *
from . import views, plu_views, part_number_views, office_views

urlpatterns = [
    path('', AdminDashboard.as_view(), name='dashboard'),
    path('admin-login/', AdminLogin.as_view(), name='admin-login'),
    path('admin-logout/', AdminLogout.as_view(), name='admin-logout'),
    
    path('employee-manage/', EmployeeManage.as_view(), name='employee-manage'),
    path('create-employee/', EmployeeCreate.as_view(), name='create-employee'),
    path('employee-details/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-details'),
    path('edit-employee/<int:employee_id>/', EmployeeEditView.as_view(), name='edit-employee'),
    path('delete-employee/<int:employee_id>/', EmployeeDeleteView.as_view(), name='delete-employee'),

    path('assign-vehicle/<int:employee_id>/', AssignVehicleView.as_view(), name='assign-vehicle'),
    path('add-vehicle/', AddVehicleView.as_view(), name='add-vehicle'),    
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/update/<int:pk>/', VehicleUpdateView.as_view(), name='update-vehicle'),
    path('vehicles/delete/<int:pk>/', VehicleDeleteView.as_view(), name='delete-vehicle'),
    path('vehicles/image/delete/<int:pk>/', DeleteVehicleImageView.as_view(), name='delete-vehicle-image'),

    path('attendance/daily/', DailyAttendanceView.as_view(), name='daily-attendance'),
    path('attendance/employee/<int:pk>/', EmployeeAttendanceDetailView.as_view(), name='employee-attendance-detail'),
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('reports/', ReportIssueListView.as_view(), name='report-issue-list'),


    path('forgot-password/<int:employee_id>/', ForgotPasswordView.as_view(), name='forgot-password'),
    
    path('company/list/', CompanyListView.as_view(), name='company-list'),
    path('company/create/', CompanyCreateView.as_view(), name='create-company'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company-details'),
    path('company/<int:pk>/update/', CompanyUpdateView.as_view(), name='update-company'),
    path('company/<int:company_id>/delete/', CompanyDeleteView.as_view(), name='delete-company'),

    path('company-announcements-list/', CompanyAnnouncementListView.as_view(), name='company-announcements-list'),
    path('company-announcements/create/', CompanyAnnouncementCreateView.as_view(), name='create-announcement'),
    path('company-announcements/<int:pk>/delete/', CompanyAnnouncementDeleteView.as_view(), name='delete-announcement'),


    path('tasks/dashboard/', TaskDashboardView.as_view(), name='task-dashboard'),
    path('tasks/dashboard-list/', TaskListView.as_view(), name='task-dashboard-list'),
    path('api/employees/by-company/', GetEmployeesByCompanyView.as_view(), name='api-employees-by-company'),
    
    # Task Type Specific URLs
    path('tasks/service/dax/', DaxServiceListView.as_view(), name='dashboard-dax-service-list'),
    path('tasks/service/dax/<int:task_id>/', DaxServiceDetailView.as_view(), name='dax-service-detail'),
    path('tasks/service/advantage/', AdvantageServiceListView.as_view(), name='dashboard-advantage-service-list'),
    path('tasks/service/advantage/<int:task_id>/', AdvantageServiceDetailView.as_view(), name='advantage-service-detail'),
    path('tasks/delivery/', DeliveryTaskListView.as_view(), name='dashboard-delivery-task-list'),
    path('tasks/delivery/create/', CreateDeliveryTaskView.as_view(), name='create-delivery-task'),
    path('tasks/delivery/<int:task_id>/', DeliveryTaskDetailView.as_view(), name='delivery-task-detail'),
    path('tasks/delivery/<int:task_id>/edit/', EditDeliveryTaskView.as_view(), name='edit-delivery-task'),
    path('tasks/mechanic/', MechanicTaskListView.as_view(), name='dashboard-mechanic-task-list'),
    path('tasks/mechanic/create/', CreateMechanicTaskView.as_view(), name='create-mechanic-task'),
    path('tasks/mechanic/<int:task_id>/', MechanicTaskDetailView.as_view(), name='mechanic-task-detail'),
    path('tasks/mechanic/<int:task_id>/edit/', EditMechanicTaskView.as_view(), name='edit-mechanic-task'),

    # Office Tasks
    path('tasks/office/notes/', office_views.NoteListView.as_view(), name='dashboard-office-note-list'),
    path('tasks/office/notes/<int:pk>/', office_views.NoteDetailView.as_view(), name='office-note-detail'),


    # Delivery Notes
    path('tasks/delivery/notes/', DeliveryNoteListView.as_view(), name='dashboard-delivery-note-list'),



    path('dashboard-leaves/', LeaveListView.as_view(), name='dashboard-leave-list'),
    path('dashboard-leaves/<int:pk>/', LeaveDetailView.as_view(), name='dashboard-leave-detail'),
    path('dashboard-leaves/<int:pk>/approve/', ApproveLeaveView.as_view(), name='dashboard-approve-leave'),
    path('dashboard-leaves/<int:pk>/reject/', RejectLeaveView.as_view(), name='dashboard-reject-leave'),
    path('dashboard-leaves/<int:pk>/cancel/', CancelLeaveView.as_view(), name='dashboard-cancel-leave'),
    
    path('notifications/send/', SendNotificationView.as_view(), name='send-notification'),
    path('notifications/list/', NotificationListView.as_view(), name='notification-list'),
    path('clear-all-notifications/', ClearAllNotificationsView.as_view(), name='clear-all-notifications'),
    
    # Admin Profile
    path('my-profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('my-profile/update/', AdminProfileUpdateView.as_view(), name='admin-profile-update'),

    
    # Master Data - PLU
    path('master-data/plu/', plu_views.PLUListView.as_view(), name='dashboard-plu-list'),
    path('master-data/plu/create/', plu_views.PLUCreateView.as_view(), name='dashboard-plu-create'),
    path('master-data/plu/edit/<int:pk>/', plu_views.PLUUpdateView.as_view(), name='dashboard-plu-edit'),
    path('master-data/plu/delete/<int:pk>/', plu_views.PLUDeleteView.as_view(), name='dashboard-plu-delete'),

    
    # Part Number Management (Master Data)
    path('master-data/part-numbers/', part_number_views.PartNumberListView.as_view(), name='dashboard-part-number-list'),
    path('master-data/part-numbers/create/', part_number_views.PartNumberCreateView.as_view(), name='dashboard-part-number-create'),
    path('master-data/part-numbers/edit/<int:pk>/', part_number_views.PartNumberUpdateView.as_view(), name='dashboard-part-number-edit'),
    path('master-data/part-numbers/delete/<int:pk>/', part_number_views.PartNumberDeleteView.as_view(), name='dashboard-part-number-delete'),
]