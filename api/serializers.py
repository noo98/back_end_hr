from rest_framework import serializers # type: ignore
from .models import Employee_lcic
# from .models import Documentout,Documentin
from .models import Department,activity,document_lcic,Document_format,Document_type,SystemUser,document_general
from .models import PersonalInformation,Education
from .models import Status,Sidebar

class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = '__all__'

class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Employee_lcic
        fields = '__all__'

# class document_lcicSerializer(serializers.ModelSerializer):
#     department_name = serializers.CharField(source='department.name', read_only=True)  # ດຶງຊື່ພະແນກ
#     department_into_name = serializers.CharField(source='department_into.name', read_only=True)# ດຶງຊື່ພະແນກທີ່ສົ່ງໃຫ້
#     format_name = serializers.CharField(source='format.name', read_only=True)  # ດຶງຊື່ format
#     # doc_type_name = serializers.CharField(source='doc_type.name', read_only=True)  # ດຶງຊື່ doc_type
#     class Meta:
#         model = document_lcic
#         fields = ['doc_id', 'insert_date', 'doc_number', 'subject', 'format_name','format', 'doc_type', 'file', 'department_name','doc_type_info','department','department_into','department_into_name', 'document_detail', 'name','status']

# Serializer ສຳລັບ Document_format
class DocumentFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_format
        fields = ['dmf_id', 'name']

# Serializer ສຳລັບ Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

# Serializer ສຳລັບ document_lcic
class document_lcicSerializer(serializers.ModelSerializer):
    format = DocumentFormatSerializer()  # Nested format
    department = DepartmentSerializer()  # Nested department
    department_into = DepartmentSerializer(many=True)  # Many-to-Many nested data

    class Meta:
        model = document_lcic
        fields = '__all__'


class document_lcic_addSerializer(serializers.ModelSerializer):
    class Meta:
        model = document_lcic
        fields = '__all__'  # ລວມທຸກ Field ຂອງ Model

class activitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity
        fields = '__all__'  # ຄືນຄ່າທຸກ field ຂອງ model

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class Document_formatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_format
        fields = ['dmf_id', 'name']

class Document_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_type
        fields = ['dmt_id', 'name']

class document_general_Serializer(serializers.ModelSerializer):
    class Meta:
        model = document_general
        fields = '__all__'  # ລວມທຸກ Field ຂອງ Model

# class document_generalSerializer(serializers.ModelSerializer):
#     format = DocumentFormatSerializer()  # Nested format
#     department = DepartmentSerializer()  # Nested department
#     class Meta:
#         model = document_general
#         fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    # roles = serializers.StringRelatedField(many=True)
    class Meta:
        model = Status
        fields = '__all__'

class SidebarSerializer(serializers.ModelSerializer):
    # roles = serializers.StringRelatedField(many=True)
    class Meta:
        model = Sidebar
        fields = '__all__'