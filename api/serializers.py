from rest_framework import serializers # type: ignore
from .models import Employee_lcic
# from .models import Documentout,Documentin
from .models import Department,activity,document_lcic,Document_format,Document_type,SystemUser,document_general
from .models import (PersonalInformation,Education,SpecializedEducation,PoliticalTheoryEducation,
                     ForeignLanguage,WorkExperience,TrainingCourse,Award, DisciplinaryAction, FamilyMember, Evaluation)
from .models import Status,Sidebar,Document_Status
from .models import Position
import datetime
import re
from django.db import transaction
from django.db.models import Max
from django.db import IntegrityError
from .models import (
    Position, Salary, SubsidyPosition, SubsidyYear,
    FuelSubsidy, AnnualPerformanceGrant, SpecialDayGrant,
    MobilePhoneSubsidy, OvertimeWork
)




class SystemUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # 👈 ป้องกัน error และไม่ส่งกลับ
    pic = serializers.ImageField(required=False, allow_null=True)      # 👈 ป้องกัน error เวลาไม่ส่งรูป

    class Meta:
        model = SystemUser
        fields = ['us_id', 'username','password', 'status', 'Department', 'Employee', 'pic']
    # def get_pic(self, obj):
    #     # ສົມມຸດວ່າ SystemUser ມີຄວາມສຳພັນ: obj.Employee.pic
    #     return obj.Employee.pic.url if obj.Employee and obj.Employee.pic else None

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

class PersonalInformationSerializer(serializers.ModelSerializer):
    # education = EducationSerializer(many=True, read_only=True, source="education_set")
    class Meta:
        model = PersonalInformation
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_lcic
        fields = '__all__'


    # def validate_Department(self, value):
    #     # ตรวจสอบว่า Department มีอยู่ในฐานข้อมูล
    #     if not Department.objects.filter(id=value.id).exists():
    #         raise serializers.ValidationError("Department does not exist.")
    #     return value

    # def validate_pic(self, value):
    #     # เพิ่มการตรวจสอบเพิ่มเติมสำหรับ pic (ถ้าจำเป็น)
    #     if value:
    #         if value.size > 5 * 1024 * 1024:
    #             raise serializers.ValidationError("Image file too large (max 5MB).")
    #         if value.content_type not in ['image/jpeg', 'image/png']:
    #             raise serializers.ValidationError("Unsupported image format (only JPEG/PNG allowed).")
    #     return value 




class DocumentFormatSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source="Department.id", read_only=True)
    department_name = serializers.CharField(source="Department.name", read_only=True)
    user_id = serializers.IntegerField(source="us_id.us_id", read_only=True)
    user_name = serializers.CharField(source="us_id.username", read_only=True)
    class Meta:
        model = Document_format
        fields = ["dmf_id", "name", "department_id", "department_name", "user_id", "user_name", "insert_date", "update_date"]

class DocumentFormat_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Document_format
        fields = '__all__'


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

class DocumentLcic_AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = document_lcic
        fields = '__all__'   
    def create(self, validated_data):
        # ທຳງານເມື່ອບໍ່ມີ doc_number ຖືກສົ່ງມາ
        if not validated_data.get("doc_number"):
            department = validated_data.get("department")
            if department:
                prefix = getattr(department, "name_e", "")[:2].upper()

                # ດຶງ doc_number ທີ່ສູງສຸດທີ່ຂຶ້ນຕົ້ນດ້ວຍ prefix
                latest_doc = (
                    document_lcic.objects
                    .filter(doc_number__startswith=f"{prefix}-")
                    .aggregate(Max("doc_number"))
                )["doc_number__max"]
                next_number = 1
                if latest_doc:
                    # ດຶງເລກທ້າຍອອກຈາກ doc_number
                    match = re.search(rf"{prefix}-\d{{8}}-(\d+)", latest_doc)
                    if match:
                        next_number = int(match.group(1)) + 1
                today = datetime.date.today()
                date_part = today.strftime("%d%m%Y")
                doc_number = f"{prefix}-{date_part}-{next_number:03d}"
                # ເຊັກວ່າບໍ່ຊ້ຳ
                while document_lcic.objects.filter(doc_number=doc_number).exists():
                    next_number += 1
                    doc_number = f"{prefix}-{date_part}-{next_number:03d}"
                validated_data["doc_number"] = doc_number
        return super().create(validated_data)


class activitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity
        fields = '__all__'  

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'name_e']

# class Document_formatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document_format
#         fields = ['dmf_id', 'name']

class Document_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_type
        fields = ['dmt_id', 'name']

class document_general_Serializer(serializers.ModelSerializer):  
    class Meta:
        model = document_general
        fields = '__all__' 
    def create(self, validated_data):
        if not validated_data.get("doc_number"):
            department = validated_data.get("department")
            if department:
                prefix = getattr(department, "name_e", "")[:2].upper()
                # ດຶງເລກສູງສຸດທີ່ເຄີຍສ້າງແລ້ວ ຈາກ doc_number
                latest_doc = (
                    document_general.objects
                    .filter(doc_number__startswith=f"{prefix}-")
                    .aggregate(Max("doc_number"))
                )["doc_number__max"]
                next_number = 1
                if latest_doc:
                    match = re.search(rf"{prefix}-\d{{8}}-(\d+)", latest_doc)
                    if match:
                        next_number = int(match.group(1)) + 1
                today = datetime.date.today()
                date_part = today.strftime("%d%m%Y")
                doc_number = f"{prefix}-{date_part}-{next_number:03d}"
                # ເຊັກອີກຄັ້ງວ່າບໍ່ຊ້ຳ
                while document_general.objects.filter(doc_number=doc_number).exists():
                    next_number += 1
                    doc_number = f"{prefix}-{date_part}-{next_number:03d}"
                validated_data["doc_number"] = doc_number
        return super().create(validated_data)
    
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

class User_emp_Serializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    class Meta:
        model = SystemUser
        fields = '__all__'
    def get_pic(self, obj):
        # ສົມມຸດວ່າ SystemUser ມີຄວາມສຳພັນ: obj.Employee.pic
        return obj.Employee.pic.url if obj.Employee and obj.Employee.pic else None

# class Asset_typeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Asset_type
#         fields = '__all__'

# class categorySerializer(serializers.ModelSerializer):
#         class Meta:
#                 model = Category
#                 fields = ['cat_id', 'ast_id', 'cat_num', 'cat_name']
#                 read_only_fields = ['cat_id', 'cat_num']  # ກຳນົດໃຫ້ cat_num ບໍ່ສາມາດແກ້ໄຂໄດ້

#         def create(self, validated_data):
#                 with transaction.atomic():
#                     # ຄົ້ນຫາ cat_num ທີ່ມີຄ່າສູງສຸດ
#                     max_num = Category.objects.aggregate(Max('cat_num'))['cat_num__max']
#                     if max_num:
#                         # ສະກັດຕົວເລກຈາກ cat_num (ເຊັ່ນ: "01" -> 1)
#                         num = int(max_num) + 1
#                     else:
#                         num = 1
#                     # ສ້າງລະຫັດໃໝ່ໃນຮູບແບບ 01, 02, ...
#                     validated_data['cat_num'] = f'{num:02d}'
#                     # ສ້າງ object ໃໝ່
#                     return Category.objects.create(**validated_data)

# class AssetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Asset
#         fields = '__all__'


class user_empSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'


class SubsidyPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsidyPosition
        fields = '__all__'


class SubsidyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsidyYear
        fields = '__all__'


class FuelSubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelSubsidy
        fields = '__all__'


class AnnualPerformanceGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualPerformanceGrant
        fields = '__all__'


class SpecialDayGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialDayGrant
        fields = '__all__'


class MobilePhoneSubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = MobilePhoneSubsidy
        fields = '__all__'


class OvertimeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimeWork
        fields = '__all__'
