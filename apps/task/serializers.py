from rest_framework import serializers
from .models import (
    DeliveryTask, Mechanic, Task, ServiceAdvantage, ServiceTaskDax, 
    ServiceDaxTypes, PLU, PartNumber, DeliveryNote,
    ServiceTaskDaxInvoiceImage, ServiceTaskDaxCompletionImage,
    ServiceAdvantageImage, ServiceAdvantageCompletionImage, MechanicPartItem
)
from apps.authapp.models import Employee


# ____________________________________________________________

class DeliveryTaskSerializer(serializers.ModelSerializer):
    task_priority = serializers.CharField(source='task.priority')
    status = serializers.CharField(source='task.status')

    class Meta:
        model = DeliveryTask
        fields = [
            'id', 'DeliveryId', 'customer_name',
            'delivery_location','task_priority','status'
        ]


class DeliveryTaskDetailSerializer(serializers.ModelSerializer):
    task_priority = serializers.CharField(source='task.priority')
    
    class Meta:
        model = DeliveryTask
        fields = [
            'DeliveryId', 'customer_name', 'customer_phone',
             'due_time', 'delivery_notes',
            'delivery_location', 'task_priority'
        ]


class DeliveryTaskStartDetailSerializer(serializers.ModelSerializer):
    task_status = serializers.CharField(source='task.status')
    task_priority = serializers.CharField(source='task.priority')
    
    class Meta:
        model = DeliveryTask
        fields = [
            'DeliveryId', 'customer_name', 'customer_phone',
            'due_time', 'delivery_location', 'task_status', 'task_priority'
        ]

class DeliveryTaskOngoingDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')
    address = serializers.CharField(source='delivery_location')
    heading = serializers.CharField(source='DeliveryId')
    task_assign_time = serializers.DateTimeField(source='task_assign_datetime', format="%d-%m-%Y %I:%M %p")
    percentage_completed = serializers.IntegerField(source='task.percentage_completed')

    class Meta:
        model = DeliveryTask
        fields = [
            'heading',
            'task_assign_time', 'status', 'address', 'percentage_completed'
        ]



class DeliveryTodayTaskDetailSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='DeliveryId')
    address_or_sub_details = serializers.CharField(source='delivery_location')
    time_of_task = serializers.DateTimeField(source='task_assign_datetime', format="%d-%m-%Y %I:%M %p")
    status = serializers.CharField(source='task.status', default='not_started')

    class Meta:
        model = DeliveryTask
        fields = [
            'heading',
            'time_of_task', 'address_or_sub_details', 'status'
        ]





import os
class CompleteDeliveryTaskSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(required=True),
        required=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    status_of_delivery = serializers.CharField(required=False, allow_blank=True)
    
    def validate_images(self, value):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        max_size = 5 * 1024 * 1024  # 5MB
        
        for img in value:
            ext = os.path.splitext(img.name)[1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError(f"Unsupported file extension {ext}. Please upload JPG, JPEG, PNG, or GIF.")
            if img.size > max_size:
                raise serializers.ValidationError(f"File {img.name} size too large. Maximum size is 5MB.")
        return value

# ____________________________________________________________

class DeliveryNoteSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p", read_only=True)
    delivery_task_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = DeliveryNote
        fields = ['id', 'note', 'delivery_task', 'delivery_task_info', 'created_at']
    
    def get_delivery_task_info(self, obj):
        if obj.delivery_task:
            return {
                'id': obj.delivery_task.id,
                'delivery_id': obj.delivery_task.DeliveryId,
                'customer_name': obj.delivery_task.customer_name,
                'customer_phone': obj.delivery_task.customer_phone,
                'delivery_location': obj.delivery_task.delivery_location,
            }
        return None




# ____________________________________________________________

class PartNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartNumber
        fields = ['id', 'part_number', 'item']


class MechanicSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')

    class Meta:
        model = Mechanic
        fields = [
        
            'id','Machine_type', 'Site_number','bay_number','heading','status'
        ]


class MechanicTodayTaskDetailSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='Machine_type')
    address_or_sub_details = serializers.CharField(source='Site_number')
    time_of_task = serializers.DateTimeField(source='task.created_at', format="%d-%m-%Y %I:%M %p")
    status = serializers.CharField(source='task.status', default='not_started')

    class Meta:
        model = Mechanic
        fields = [
            'heading',
            'time_of_task', 'address_or_sub_details', 'status'
        ]        


class MechanicTaskOngoingDetailSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='Machine_type')
    status = serializers.CharField(source='task.status')
    address = serializers.CharField(source='Site_number')
    maintenance_heading = serializers.CharField(source='heading')
    task_assign_time = serializers.DateTimeField(source='task.created_at', format="%d-%m-%Y %I:%M %p")
    percentage_completed = serializers.IntegerField(source='task.percentage_completed')

    class Meta:
        model = Mechanic
        fields = [
            'heading',
            'task_assign_time', 'status', 'address', 'percentage_completed','maintenance_heading'
        ]


class MechanicCreateSerializer(serializers.ModelSerializer):
    Site_number = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    bay_number = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    Machine_type = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    Machine_serial_number = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    job_description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    spare_part_details = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    part_items = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True
    )

    
    class Meta:
        model = Mechanic
        fields = [
            'employee',
            'Site_number', 'bay_number', 'Machine_type',
            'Machine_serial_number', 'job_description', 'spare_part_details',
            'part_items'
        ]
        read_only_fields = ['task']
    
    def create(self, validated_data):
        employee = validated_data.pop('employee')
        part_items_data = validated_data.pop('part_items', [])
        
        task = Task.objects.create(
            employee=employee,
            task_type='mechanic',
            status='not_started',
            icon_type='mechanic',
        )
        
        mechanic = Mechanic.objects.create(
            task=task,
            **validated_data
        )
        
        # Create part items in separate table
        for item_data in part_items_data:
            part_number_id = item_data.get('part_number_id') or item_data.get('part_number')
            quantity = item_data.get('quantity', 1)
            if part_number_id:
                try:
                    part_num = PartNumber.objects.get(id=part_number_id)
                    MechanicPartItem.objects.create(
                        mechanic=mechanic,
                        part_number=part_num,
                        quantity=quantity
                    )
                except PartNumber.DoesNotExist:
                    pass
        
        return mechanic



class MechanicTaskDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')
    part_items = serializers.SerializerMethodField()

    class Meta:
        model = Mechanic
        fields = [
            'heading',
            'Site_number',
            'Machine_type',
            'bay_number',
            'Machine_serial_number',
            'spare_part_details',
            'job_description',
            'part_items',
            'status'
        ]

    def get_part_items(self, obj):
        items = obj.part_items.all()
        return [
            {
                'part_number': item.part_number.part_number,
                'item': item.part_number.item,
                'quantity': item.quantity
            }
            for item in items
        ]

        

class MechanicStartTaskDetailSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(source='task.id') 
    machine_info = serializers.SerializerMethodField()
    status = serializers.CharField(source='task.status')
    
    class Meta:
        model = Mechanic
        fields = [
            'task_id',
            'machine_info',
            'bay_number',
            'started_at',
            'status'
        ]
        
    def get_machine_info(self, obj):
        # Combine Type and Serial for display
        m_type = obj.Machine_type if obj.Machine_type else ""
        serial = obj.Machine_serial_number if obj.Machine_serial_number else ""
        if m_type and serial:
             return f"{m_type} - {serial.split(' - ')[0]}" 
        return f"{m_type} {serial}"



class MechanicCompleteTaskSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='completion_image', required=True)
    notes = serializers.CharField(source='completion_remarks', required=False, allow_blank=True)
    
    class Meta:
        model = Mechanic
        fields = ['image', 'notes']

# ____________________________________________________________



# ____________________________________________________________



class PLUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLU
        fields = ['id', 'plu', 'category', 'sub_service']


class AdvantageTaskOngoingDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')
    address = serializers.CharField(source='detailing_site')
    heading = serializers.CharField(source='plu.category', read_only=True)
    task_assign_time = serializers.DateTimeField(source='created_at', format="%d-%m-%Y %I:%M %p")
    percentage_completed = serializers.IntegerField(source='task.percentage_completed')

    class Meta:
        model = ServiceAdvantage
        fields = [
            'heading',
            'task_assign_time', 'status', 'address', 'percentage_completed'
        ]

class AdvantageSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')
    category = serializers.CharField(source='plu.category', read_only=True)

    class Meta:
        model = ServiceAdvantage
        fields = [
            'id',
            'detailing_site', 
            'category', 
            'status'
        ]


class AdvantageTodayTaskDetailSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='detailing_site')
    address_or_sub_details = serializers.CharField(source='plu.category')
    time_of_task = serializers.DateTimeField(source='created_at', format="%d-%m-%Y %I:%M %p")
    status = serializers.CharField(source='task.status', default='not_started')

    class Meta:
        model = ServiceAdvantage
        fields = [
            'heading',
            'time_of_task', 'address_or_sub_details', 'status'
        ]        



class AdvantageDetailSerializer(serializers.ModelSerializer):
    plu = serializers.CharField(source='plu.plu', read_only=True)
    category = serializers.CharField(source='plu.category', read_only=True)
    sub_service = serializers.CharField(source='plu.sub_service', read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = ServiceAdvantage
        fields = [
            'id',
            'detailing_site', 
            'plu', 
            'category', 
            'sub_service', 
            'chassis_number', 
            'images',
        ]

    def get_images(self, obj):
        images = obj.images.all()
        request = self.context.get('request')
        if request:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return [img.image.url for img in images]



class AdvantageCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        required=False,
        allow_null=True,
        write_only=True
    )
    
    class Meta:
        model = ServiceAdvantage
        fields = [
            'employee',
            'detailing_site', 
            'plu', 
            'chassis_number', 
            'images'
        ]
        read_only_fields = ['task']
    
    def create(self, validated_data):
        employee = validated_data.pop('employee')
        images = validated_data.pop('images', [])
        
        # Backup extraction for direct QueryDict list
        if not images and hasattr(self.initial_data, 'getlist'):
            images = self.initial_data.getlist('images')

        task = Task.objects.create(
            employee=employee,
            task_type='service', 
            status='not_started',
            icon_type='service',
        )
        
        advantage_task = ServiceAdvantage.objects.create(
            task=task,
            **validated_data
        )
        
        for image in images:
            ServiceAdvantageImage.objects.create(
                advantage_service=advantage_task,
                image=image
            )
        
        return advantage_task



class AdvantageStartTaskDetailSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(source='task.id')
    status = serializers.CharField(source='task.status')
    plu = serializers.CharField(source='plu.plu', read_only=True)
    category = serializers.CharField(source='plu.category', read_only=True)
    sub_service = serializers.CharField(source='plu.sub_service', read_only=True)
    images = serializers.SerializerMethodField()
    class Meta:
        model = ServiceAdvantage
        fields = [
            'task_id',
            'detailing_site',
            'plu',
            'category',
            'sub_service',
            'chassis_number',
            'started_at',
            'status',
            'images'
        ]

    def get_images(self, obj):
        images = obj.images.all()
        request = self.context.get('request')
        if request:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return [img.image.url for img in images]
        



class AdvantageCompleteTaskSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        required=True,
        write_only=True
    )
    notes = serializers.CharField(source='completion_remarks', required=False, allow_blank=True)
    
    class Meta:
        model = ServiceAdvantage
        fields = ['images', 'notes']

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        
        # Backup extraction for direct QueryDict list
        if not images and hasattr(self.initial_data, 'getlist'):
            images = self.initial_data.getlist('images')

        instance.completion_remarks = validated_data.get('completion_remarks', instance.completion_remarks)
        instance.save()
        
        for image in images:
            ServiceAdvantageCompletionImage.objects.create(
                advantage_service=instance,
                image=image
            )
            
        return instance

# ____________________________________________________________



class DaxTaskCreateSerializer(serializers.Serializer):
    detailing_site = serializers.CharField(required=True)
    service_types = serializers.ListField(child=serializers.DictField(), required=True)
    remark = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    chassis_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vehicle_model = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    invoice_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        required=False,
        allow_null=True
    )
    proof_of_invoice = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        employee = self.context.get('employee')
        service_types_data = validated_data.pop('service_types')
        detailing_site = validated_data.get('detailing_site')
        remark = validated_data.get('remark', '')
        chassis_number = validated_data.get('chassis_number', '')
        vehicle_model = validated_data.get('vehicle_model', '')
        invoice_images = validated_data.get('invoice_images')
        proof_of_invoice = validated_data.get('proof_of_invoice')
        
        # Create the main Task
        task = Task.objects.create(
            employee=employee,
            task_type='service',
            status='not_started',
            icon_type='service'
        )

        invoice_status = 'invoice_received' if proof_of_invoice and proof_of_invoice.lower() == 'yes' else None
        

        dax_service = ServiceTaskDax.objects.create(
            task=task,
            detailing_site=detailing_site,
            remarks=remark,
            vehicle_model=vehicle_model,
            chassis_no=chassis_number,
            invoice_status=invoice_status,
        )



        if invoice_images:
            for image in invoice_images:
                ServiceTaskDaxInvoiceImage.objects.create(
                    dax_service=dax_service,
                    image=image
                )


        for i, st_data in enumerate(service_types_data):            
            # Create duties based on service type
            s_type = st_data.get('type', '')
            s_sub_type = st_data.get('sub_type', '')
            layers = st_data.get('layer', '')
            
            ServiceDaxTypes.objects.create(
                dax_service=dax_service,
                service_type=st_data.get('type'),
                service_sub_type=st_data.get('sub_type'),
                level=st_data.get('level'),
                layers=st_data.get('layer'),
                roll_meter=st_data.get('roll_meter')
            )
            
        return task




class DaxTaskOngoingDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='task.status')
    address = serializers.CharField(source='detailing_site')
    heading = serializers.SerializerMethodField(method_name='get_service_name')
    task_assign_time = serializers.DateTimeField(source='created_at', format="%d-%m-%Y %I:%M %p")
    percentage_completed = serializers.IntegerField(source='task.percentage_completed')

    class Meta:
        model = ServiceTaskDax
        fields = [
            'heading',
            'task_assign_time', 'status', 'address', 'percentage_completed'
        ]

    def get_service_name(self, obj):
        dax_types = obj.service_dax_types.all()
        names = []
        for dax_type in dax_types:
            if dax_type.service_sub_type and dax_type.service_sub_type.lower() != 'none':
                names.append(dax_type.service_sub_type.title())
            elif dax_type.service_type:
                names.append(dax_type.service_type.title())
        
        if names:
            return ", ".join(names)
        return "Unknown Service"


class DaxTaskListSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    status = serializers.CharField(source='task.status')

    class Meta:
        model = ServiceTaskDax
        fields = ['id', 'service_name', 'detailing_site','status']

    def get_service_name(self, obj):
        dax_types = obj.service_dax_types.all()
        names = []
        for dax_type in dax_types:
            if dax_type.service_sub_type and dax_type.service_sub_type.lower() != 'none':
                names.append(dax_type.service_sub_type.title())
            elif dax_type.service_type:
                names.append(dax_type.service_type.title())
        
        if names:
            return ", ".join(names)
        return "Unknown Service"


class DaxTodayTaskDetailSerializer(serializers.ModelSerializer):
    heading = serializers.SerializerMethodField()
    address_or_sub_details = serializers.CharField(source='detailing_site')
    time_of_task = serializers.DateTimeField(source='created_at', format="%d-%m-%Y %I:%M %p")
    status = serializers.CharField(source='task.status', default='not_started')

    class Meta:
        model = ServiceTaskDax
        fields = [
            'heading',
            'time_of_task', 'address_or_sub_details', 'status'
        ]

    def get_heading(self, obj):
        dax_types = obj.service_dax_types.all()
        names = []
        for dax_type in dax_types:
            if dax_type.service_sub_type and dax_type.service_sub_type.lower() != 'none':
                names.append(dax_type.service_sub_type.title())
            elif dax_type.service_type:
                names.append(dax_type.service_type.title())
        
        if names:
            return ", ".join(names)
        return "Unknown Service"




class ServiceInfoSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = ServiceDaxTypes
        fields = ['id', 'service_name', 'detail', 'roll_meter', 'completed']

    def get_service_name(self, obj):
        return obj.service_sub_type.title() if obj.service_sub_type and obj.service_sub_type.lower() != 'none' else (obj.service_type.title() if obj.service_type else "")

    def get_detail(self, obj):
        parts = []
        if obj.level and obj.level.lower() != 'none':
            parts.append(obj.level)
        if obj.layers and obj.layers.lower() != 'none':
            parts.append(obj.layers)
        return " - ".join(parts) if parts else ""




class DaxTaskDetailSerializer(serializers.ModelSerializer):
    service_title = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    invoice_images = serializers.SerializerMethodField()

    class Meta:
        model = ServiceTaskDax
        fields = [
            'id', 'service_title', 'services', 'detailing_site', 
            'remarks', 'chassis_no', 'vehicle_model', 'invoice_images'
        ]

    def get_service_title(self, obj):
        dax_types = obj.service_dax_types.all()
        names = []
        for dax_type in dax_types:
            if dax_type.service_sub_type and dax_type.service_sub_type.lower() != 'none':
                names.append(dax_type.service_sub_type.title())
            elif dax_type.service_type:
                names.append(dax_type.service_type.title())
        
        if names:
            return ", ".join(names)
        return "Unknown Service"

    def get_services(self, obj):
        dax_types = obj.service_dax_types.all()
        return ServiceInfoSerializer(dax_types, many=True).data


    def get_invoice_images(self, obj):
        images = obj.invoice_images.all()
        request = self.context.get('request')
        if request:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return [img.image.url for img in images]




class DaxTaskStartDetailSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(source='task.id')
    status = serializers.CharField(source='task.status')
    services = serializers.SerializerMethodField()
    service_title = serializers.SerializerMethodField()
    invoice_images = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceTaskDax
        fields = [
            'task_id',
            'service_title',
            'services',
            'detailing_site',
            'created_at',
            'status',
            'invoice_images'
        ]

    def get_created_at(self, obj):
        return obj.started_at

    def get_service_title(self, obj):
        dax_types = obj.service_dax_types.all()
        names = []
        for dax_type in dax_types:
            if dax_type.service_sub_type and dax_type.service_sub_type.lower() != 'none':
                names.append(dax_type.service_sub_type.title())
            elif dax_type.service_type:
                names.append(dax_type.service_type.title())
        
        if names:
            return ", ".join(names)
        return "Unknown Service"


    def get_invoice_images(self, obj):
        images = obj.invoice_images.all()
        request = self.context.get('request')
        if request:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return [img.image.url for img in images]


    def get_services(self, obj):
        dax_types = obj.service_dax_types.all()
        return ServiceInfoSerializer(dax_types, many=True).data




class DaxCompleteTaskSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        required=True,
        write_only=True
    )
    notes = serializers.CharField(source='completion_remarks', required=False, allow_blank=True)
    
    class Meta:
        model = ServiceTaskDax
        fields = ['images', 'notes']

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        
        # Backup extraction for direct QueryDict list
        if not images and hasattr(self.initial_data, 'getlist'):
            images = self.initial_data.getlist('images')

        instance.completion_remarks = validated_data.get('completion_remarks', instance.completion_remarks)
        instance.save()
        
        for image in images:
            ServiceTaskDaxCompletionImage.objects.create(
                dax_service=instance,
                image=image
            )
            
        return instance
