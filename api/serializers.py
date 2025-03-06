from rest_framework import serializers # type: ignore
from .models import Employee_lcic
# from .models import Documentout,Documentin
from .models import Department,activity,document_lcic,Document_format,Document_type,SystemUser,document_general
from .models import (PersonalInformation,Education,SpecializedEducation,PoliticalTheoryEducation,
                     ForeignLanguage,WorkExperience,TrainingCourse,Award, DisciplinaryAction, FamilyMember, Evaluation)
from .models import Status,Sidebar,Document_Status

class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = '__all__'

class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
class SpecializedEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializedEducation
        fields = '__all__'
class PoliticalTheoryEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalTheoryEducation
        fields = '__all__'
class ForeignLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignLanguage
        fields = '__all__'
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
class TrainingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCourse
        fields = '__all__'
class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'
class DisciplinaryActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryAction
        fields = '__all__'
class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Employee_lcic
        fields = '__all__'

class DocumentFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_format
        fields = ['dmf_id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class DocStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_Status
        fields = '__all__'

class DocumentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ['us_id']

class DocumentStatusSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='us_id.username', read_only=True) 
    class Meta:
        model = Document_Status
        fields = ['Doc_status','user_name','us_id']#'docstat_id', 'doc_id', 'us_id', 'user_name', 'timestamp'


class document_lcicSerializer(serializers.ModelSerializer):
    format = DocumentFormatSerializer()  
    department = DepartmentSerializer()  
    department_into = DepartmentSerializer(many=True)
    status = DocumentStatusSerializer(source='statuses.all', many=True, read_only=True)
    class Meta:
        model = document_lcic
        fields = [  # ระบุฟิลด์ที่ต้องการรวม (ยกเว้น 'status')
            "doc_id",
            "insert_date",
            "doc_number",
            "subject",
            "format",
            "doc_type",
            "doc_type_info",
            "file",
            "department",
            "document_detail",
            "name",
            "department_into",
            "status",
            "status2"
        ]

class document_lcic_addSerializer(serializers.ModelSerializer):
    class Meta:
        model = document_lcic
        fields = '__all__'  

class activitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity
        fields = '__all__'  

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
        fields = '__all__'  

# class document_generalSerializer(serializers.ModelSerializer):
#     format = DocumentFormatSerializer()  # Nested format
#     department = DepartmentSerializer()  # Nested department
#     class Meta:
#         model = document_general
#         fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'

class SidebarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sidebar
        fields = '__all__'
class UpdateDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = document_lcic
        fields = '__all__'

