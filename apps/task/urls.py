# urls.py
from django.urls import path
from apps.task.views import deliveryview,mechanicview,advantageview,daxview

urlpatterns = [

    path('delivery/notes/', deliveryview.DeliveryNoteListCreateAPIView.as_view(), name='delivery-note-list-create'),
    path('delivery/', deliveryview.TaskListView.as_view(), name='delivery-list'),
    path('<int:delivery_id>/delivery/', deliveryview.TaskDetailView.as_view(), name='task-detail'),
    path('<int:delivery_id>/start/', deliveryview.StartTaskAPIView.as_view(), name='start-task'),
    path('<int:task_id>/start-details/', deliveryview.StartTaskDetailsAPIView.as_view(), name='start-task-details'),
    path('<int:delivery_id>/end/', deliveryview.CompleteDeliveryTaskAPIView.as_view(), name='end-task'),



    path('mechanic/part-numbers/', mechanicview.PartNumberListAPIView.as_view(), name='part-number-list'),
    path('mechanic/', mechanicview.MechanicTaskListAPIView.as_view(), name='mechanic-list'),
    path('mechanic/create/', mechanicview.CreateMechanicTaskView.as_view(), name='mechanic-create'),
    path('mechanic/<int:pk>/', mechanicview.MechanicTaskDetailAPIView.as_view(), name='mechanic-detail'),
    path('mechanic/<int:pk>/start/', mechanicview.StartMechanicTaskAPIView.as_view(), name='mechanic-start'),
    path('mechanic/<int:task_id>/start-details/', mechanicview.MechanicStartTaskDetailAPIView.as_view(), name='mechanic-start-details'),
    path('mechanic/<int:pk>/complete/', mechanicview.CompleteMechanicTaskAPIView.as_view(), name='mechanic-complete'),



    path('advantage/plu/', advantageview.PLUListAPIView.as_view(), name='plu-list'),
    path('advantage/', advantageview.AdvantageTaskListAPIView.as_view(), name='advantage-list'),
    path('advantage/create/', advantageview.CreateAdvantageTaskView.as_view(), name='advantage-create'),
    path('advantage/<int:pk>/', advantageview.AdvantageTaskDetailAPIView.as_view(), name='advantage-detail'),
    path('advantage/<int:pk>/start/', advantageview.StartAdvantageTaskAPIView.as_view(), name='advantage-start'),
    path('advantage/<int:task_id>/start-details/', advantageview.AdvantageStartTaskDetailAPIView.as_view(), name='advantage-start-details'),
    path('advantage/<int:pk>/complete/', advantageview.CompleteAdvantageTaskAPIView.as_view(), name='advantage-complete'),
    


    
    path('dax/create/', daxview.CreateDaxTaskView.as_view(), name='dax-create'),
    path('dax/', daxview.DaxTaskListAPIView.as_view(), name='dax-list'),
    path('dax/<int:pk>/', daxview.DaxTaskDetailAPIView.as_view(), name='dax-detail'),
    path('dax/<int:pk>/start/', daxview.StartDaxTaskView.as_view(), name='dax-start'),
    path('dax/<int:task_id>/start-details/', daxview.DaxTaskStartDetailAPIView.as_view(), name='dax-start-details'),
    path('dax/service-type/<int:pk>/complete/', daxview.CompleteDaxServiceTypeView.as_view(), name='dax-service-type-complete'),
    path('dax/<int:pk>/complete/', daxview.CompleteDaxTaskView.as_view(), name='dax-complete'),

]