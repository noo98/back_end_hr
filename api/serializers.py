from time import timezone
from rest_framework import serializers # type: ignore
from .models import Employee_lcic
# from .models import Documentout,Documentin
from .models import Department,activity,document_lcic,Document_format,Document_type,SystemUser,document_general
from .models import (PersonalInformation,Education,SpecializedEducation,PoliticalTheoryEducation,Fuel_payment,
                     ForeignLanguage,WorkExperience,TrainingCourse,Award, DisciplinaryAction, FamilyMember, Evaluation)
from .models import Status,Sidebar,Document_Status,evaluation_score, uniform,evaluation_score_emp
from .models import Position,col_policy,job_mobility,income_tax, Saving_cooperative,welfare, Role, RolePermission, Menu, MainMenu
import datetime
import math
import re
from decimal import Decimal
from django.db.models import Max # type: ignore
from .models import (
    Position, Salary, SubsidyPosition, SubsidyYear,SpecialDay_Position,
    FuelSubsidy, AnnualPerformanceGrant, SpecialDayGrant,
    MobilePhoneSubsidy, SystemSetting, OvertimeWork,monthly_payment
)
from .models import (Overtime_history,colpolicy_history,fuel_payment_history,saving_cooperative_history,specialday_emp_history,monthly_payment_history,
                     uniform_history,evaluation_score_emp_history,MobilePhoneSubsidy_emp_History)
    # def to_internal_value(self, data):
    #     try:
    #         # ຮັບຂໍ້ມູນວັນທີໃນຮູບ ddmmyy
    #         return datetime.strptime(data, '%d%m%Y').date()
    #     except ValueError:
    #         raise serializers.ValidationError('Date must be in ddmmyy format (e.g. 200525)')
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class SystemUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=False)  # 👈 ป้องกัน error และไม่ส่งกลับ
    pic = serializers.ImageField(required=False, allow_null=True)      # 👈 ป้องกัน error เวลาไม่ส่งรูป

    class Meta:
        model = SystemUser
        fields = ['us_id', 'username','password', 'Department', 'Employee', 'pic']

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'

class MainMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMenu
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['menu_id', 'menu_name', 'url', 'icon',]

class MainMenuUserMenuSerializer(serializers.ModelSerializer):
    children = MenuSerializers(many=True, read_only=True, source='menus')  # ກໍາຫນົດ source ໃຫ້ຖືກຕ້ອງ

    class Meta:
        model = MainMenu
        fields = ['main_id', 'main_name', 'icon', 'children']

class UserMenuSerializer(serializers.ModelSerializer):
    menus = MainMenuUserMenuSerializer(many=True, read_only=True)

    class Meta:
        model = SystemUser
        fields = ['us_id', 'username', 'menus']
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
    # education = EducationSerializer(many=True, read_only=True, source='education_set')
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
    #         raise serializers.ValidationError('Department does not exist.')
    #     return value

    # def validate_pic(self, value):
    #     # เพิ่มการตรวจสอบเพิ่มเติมสำหรับ pic (ถ้าจำเป็น)
    #     if value:
    #         if value.size > 5 * 1024 * 1024:
    #             raise serializers.ValidationError('Image file too large (max 5MB).')
    #         if value.content_type not in ['image/jpeg', 'image/png']:
    #             raise serializers.ValidationError('Unsupported image format (only JPEG/PNG allowed).')
    #     return value 




class DocumentFormatSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source='Department.id', read_only=True)
    department_name = serializers.CharField(source='Department.name', read_only=True)
    user_id = serializers.IntegerField(source='us_id.us_id', read_only=True)
    user_name = serializers.CharField(source='us_id.username', read_only=True)
    class Meta:
        model = Document_format
        fields = ['dmf_id', 'name', 'department_id', 'department_name', 'user_id', 'user_name', 'insert_date', 'update_date']

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
            'doc_id',
            'insert_date',
            'doc_number',
            'subject',
            'format',
            'doc_type',
            'doc_type_info',
            'file',
            'department',
            'document_detail',
            'name',
            'department_into',
            'status',
            'status2'
        ]

class DocumentLcic_AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = document_lcic
        fields = '__all__'   
    def create(self, validated_data):
        if not validated_data.get('doc_number'):
            department = validated_data.get('department')
            if department:
                prefix = getattr(department, 'name_e', '')[:2].upper()
                # ດຶງເລກສູງສຸດທີ່ເຄີຍສ້າງແລ້ວ ຈາກ doc_number
                latest_doc = (
                    document_lcic.objects
                    .filter(doc_number__startswith=f'{prefix}-')
                    .aggregate(Max('doc_number'))
                )['doc_number__max']
                next_number = 1
                if latest_doc:
                    match = re.search(rf'{prefix}-\d{{8}}-(\d+)', latest_doc)
                    if match:
                        next_number = int(match.group(1)) + 1
                today = datetime.date.today()
                date_part = today.strftime('%d%m%Y')
                doc_number = f'{prefix}-{date_part}-{next_number:03d}'
                # ເຊັກອີກຄັ້ງວ່າບໍ່ຊ້ຳ
                while document_lcic.objects.filter(doc_number=doc_number).exists():
                    next_number += 1
                    doc_number = f'{prefix}-{date_part}-{next_number:03d}'
                validated_data['doc_number'] = doc_number
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
        if not validated_data.get('doc_number'):
            department = validated_data.get('department')
            if department:
                prefix = getattr(department, 'name_e', '')[:2].upper()
                # ດຶງເລກສູງສຸດທີ່ເຄີຍສ້າງແລ້ວ ຈາກ doc_number
                latest_doc = (
                    document_general.objects
                    .filter(doc_number__startswith=f'{prefix}-')
                    .aggregate(Max('doc_number'))
                )['doc_number__max']
                next_number = 1
                if latest_doc:
                    match = re.search(rf'{prefix}-\d{{8}}-(\d+)', latest_doc)
                    if match:
                        next_number = int(match.group(1)) + 1
                today = datetime.date.today()
                date_part = today.strftime('%d%m%Y')
                doc_number = f'{prefix}-{date_part}-{next_number:03d}'
                # ເຊັກອີກຄັ້ງວ່າບໍ່ຊ້ຳ
                while document_general.objects.filter(doc_number=doc_number).exists():
                    next_number += 1
                    doc_number = f'{prefix}-{date_part}-{next_number:03d}'
                validated_data['doc_number'] = doc_number
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


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        # ສະແດງຂໍ້ມູນວັນທີໃນຮູບ ddmmyy
        return value.strftime('%d-%m-%Y')

class user_empSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    # fuel_subsidy = serializers.CharField(source='fs_id.fuel_subsidy', read_only=True)
    # salary = serializers.CharField(source='sal_id.SalaryGrade', read_only=True)
    # SubsidyPosition = serializers.CharField(source='sp_id.grant', read_only=True)
    # mobilephone = serializers.CharField(source='mb.grant', read_only=True)
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

class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ['id', 'key', 'value']

class get_uniformSerializer(serializers.ModelSerializer):
    formal_suit = serializers.CharField(source='uniform_price.formal_suit', read_only=True)
    emp_uniform = serializers.CharField(source='uniform_price.emp_uniform', read_only=True)
    amount_sui = serializers.CharField(source='uniform_price.amount_sui', read_only=True)
    amount_uni = serializers.CharField(source='uniform_price.amount_uni', read_only=True)
    class Meta:
        model = uniform
        fields = ['uni_id','formal_suit','amount_sui', 'emp_uniform','amount_uni']

class uniformSerializer(serializers.ModelSerializer):
    class Meta:
        model = uniform
        fields = '__all__'

class FuelSubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelSubsidy
        fields = '__all__'

class get_FuelSubsidySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelSubsidy
        fields = ['fs_id','pos_id','fuel_subsidy' ]   

class fuel_paymentSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    position = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    fuel_subsidy = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    fuel_price = serializers.SerializerMethodField()
    total_fuel = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    def get_fuel_subsidy(self, obj):
        if not obj.emp_id or not obj.emp_id.pos_id:
            return None
        fuel_subsidy = FuelSubsidy.objects.filter(pos_id=obj.emp_id.pos_id).first()
        if fuel_subsidy:
            return fuel_subsidy.fuel_subsidy
        
    def get_date(self, obj):
        setting = SystemSetting.objects.filter(key="fuel_price").first()
        if setting:
            return setting.date
        return None

    def get_fuel_price(self, obj):
        if not obj.emp_id or not obj.emp_id.pos_id:
            return None
        fuel_subsidy = FuelSubsidy.objects.filter(pos_id=obj.emp_id.pos_id).first()
        if fuel_subsidy and fuel_subsidy.fuel_price:
            return fuel_subsidy.fuel_price.value
        return None
    def get_total_fuel(self, obj):
        if not obj.emp_id or not obj.emp_id.pos_id:
            return None
        fuel_subsidy = FuelSubsidy.objects.filter(pos_id=obj.emp_id.pos_id).first()
        if fuel_subsidy:
            return fuel_subsidy.total_fuel
        return None
    def get_status(self, obj):
        """ເຊັກຈາກ fuel_payment_history ວ່າມີບັນທຶກໃນເດືອນປັດຈຸບັນບໍ່"""
        from django.utils import timezone
        from .models import fuel_payment_history   # import ຂ້າງໃນ ຫຼື ໄວ້ດ້ານເທິງກໍ່ໄດ້

        now = timezone.now()

        exists = fuel_payment_history.objects.filter(
            
            date_insert__month=now.month
        ).exists()

        if exists:
            return f"ຄິດໄລ່ເດືອນ {now.month} ແລ້ວ"
        return f"ເດືອນ {now.month} ບໍ່ທັນຄິດໄລ່"
    
    class Meta:
        model = Fuel_payment
        fields = ['fp_id','date','emp_id','emp_name','pos_id','position','fuel_subsidy','fuel_price','total_fuel','status']

class AnnualPerformanceGrantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnnualPerformanceGrant
        fields = '__all__'

class SpecialDayGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialDayGrant
        fields = '__all__'
class Specialday_PositionSerializer(serializers.ModelSerializer):
    pos_name = serializers.CharField(source='pos_id.name', read_only=True)
    sdg_id = serializers.IntegerField(source='special_day.sdg_id', read_only=True)
    special_day = serializers.CharField(source='special_day.occasion_name', read_only=True)
    class Meta:
        model = SpecialDay_Position
        fields = ['id','sdg_id','special_day','pos_id','pos_name','grant']

from django.utils import timezone
from datetime import date

class Specialday_empserialiser(serializers.ModelSerializer):
    pos_name = serializers.CharField(source='pos_id.name', read_only=True)
    special_day = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    gender = serializers.CharField(source='Gender', read_only=True)  # ✅ map จาก field Gender ของ model

    def get_special_day(self, obj):
        now = timezone.now()
        try:
            employee = Employee_lcic.objects.get(emp_id=obj.emp_id)
            if employee.pos_id:
                specials = (
                    SpecialDay_Position.objects
                    .filter(pos_id=employee.pos_id)
                    .select_related("special_day")
                )

                results = []
                for s in specials:
                    if not s.special_day:
                        continue

                    # ❌ ຖ້າ gender = ຊາຍ ແລະ sdg_id = 3 ຂ້າມ
                    if employee.Gender == "ຊາຍ" and s.special_day.sdg_id == 3:
                        continue

                    exists = specialday_emp_history.objects.filter(
                        emp_id=obj.emp_id,
                        sdg_id=s.special_day.sdg_id,
                        date_insert__month=now.month
                    ).exists()

                    results.append({
                        "sdg_id": s.special_day.sdg_id,
                        "sdg_name": s.special_day.occasion_name,
                        "grant": s.grant,
                        "status": (
                            f"ຄິດໄລ່ເດືອນ {now.month} ແລ້ວ"
                            if exists else
                            f"ເດືອນ {now.month} ບໍ່ທັນຄິດໄລ່"
                        )
                    })

                return results
        except Employee_lcic.DoesNotExist:
            return []
        return []

    def get_date(self, obj):
        return date.today().strftime("%Y-%m-%d")

    class Meta:
        model = Employee_lcic
        fields = [
            'date',
            'emp_id',
            'lao_name',
            'gender',     # ✅ now matches the serializer field
            'pos_id',
            'pos_name',
            'special_day'
        ]

class MobilePhoneSubsidySerializer(serializers.ModelSerializer):
    pso_name = serializers.CharField(source='pos_id.name', read_only=True)
    class Meta:
        model = MobilePhoneSubsidy
        fields = ['mb_id', 'pos_id', 'pso_name', 'grant',]

class job_mobilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = job_mobility
        fields = ["jm_id","pos_id", "jm_policy", "number_of_days", "amount_per_day"]
        
class col_policySerializer(serializers.ModelSerializer):
    # emp_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    pos_id = serializers.CharField(source='emp_id.pos_id.pos_id', read_only=True)
    number_of_days = serializers.SerializerMethodField()
    amount_per_day = serializers.SerializerMethodField()
    jm_policy = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_payment = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def _get_job_mobility_data(self, obj):
        if obj.emp_id and obj.emp_id.pos_id:
            return job_mobility.objects.filter(pos_id=obj.emp_id.pos_id).first()
        return None

    def get_number_of_days(self, obj):
        jm = self._get_job_mobility_data(obj)
        return jm.number_of_days if jm else None

    def get_amount_per_day(self, obj):
        jm = self._get_job_mobility_data(obj)
        return jm.amount_per_day if jm else None
    def get_date(self, obj):
        jm = self._get_job_mobility_data(obj)
        return jm.date if jm else None

    def get_jm_policy(self, obj):
        jm = self._get_job_mobility_data(obj)
        return jm.jm_policy if jm else None

    def get_total_amount(self, obj):
        days = self.get_number_of_days(obj)
        rate = self.get_amount_per_day(obj)
        return days * rate if days and rate else 0

    def get_total_payment(self, obj):
        total = self.get_total_amount(obj)
        policy = self.get_jm_policy(obj)
        return total + policy if policy else total
    def get_status(self, obj):
        """ເຊັກຈາກ colpolicy_history ວ່າມີບັນທຶກໃນເດືອນປັດຈຸບັນບໍ່"""
        from django.utils import timezone
        from .models import colpolicy_history   # import ຂ້າງໃນ ຫຼື ໄວ້ດ້ານເທິງກໍ່ໄດ້
        now = timezone.now()
        exists = colpolicy_history.objects.filter(
            date_insert__month=now.month
        ).exists()
        if exists:
            return f"ຄິດໄລ່ເດືອນ {now.month} ແລ້ວ"
        return f"ເດືອນ {now.month} ບໍ່ທັນຄິດໄລ່"
    
    class Meta:
        model = col_policy
        fields = ['col_id','date', 'emp_id', 'date', 'pos_id',
                  'number_of_days', 'amount_per_day', 'total_amount',
                  'jm_policy', 'total_payment', 'status']

class OvertimeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimeWork
        fields = '__all__'

class get_OvertimeWorkSerializer(serializers.ModelSerializer):
    value_150 = serializers.SerializerMethodField()
    value_200 = serializers.SerializerMethodField()
    value_250 = serializers.SerializerMethodField()
    value_300 = serializers.SerializerMethodField()
    value_350 = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()
    position = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    emp_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    # recorder_name = serializers.CharField(source='recorder.username', read_only=True)
    status = serializers.SerializerMethodField()

    def get_salary(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return None
        salary = Salary.objects.filter(pos_id=employee.pos_id).first()
        return salary.SalaryGrade if salary else None

    def calculate_ot_value(self, obj, hours, rate_percent):
        if not obj.emp_id or not obj.emp_id.pos_id:
            return 0
        salary = Salary.objects.filter(pos_id=obj.emp_id.pos_id).first()
        if not salary or not hours:
            return 0
        base_hourly_rate = salary.SalaryGrade / 26 / 8
        ot_value = base_hourly_rate * hours * rate_percent / 100
        return math.ceil(ot_value)

    def get_value_150(self, obj):
        return self.calculate_ot_value(obj, obj.csd_evening, 150)

    def get_value_200(self, obj):
        return self.calculate_ot_value(obj, obj.csd_night, 200)

    def get_value_250(self, obj):
        return self.calculate_ot_value(obj, obj.hd_mor_after, 250)

    def get_value_300(self, obj):
        return self.calculate_ot_value(obj, obj.hd_evening, 300)

    def get_value_350(self, obj):
        return self.calculate_ot_value(obj, obj.hd_night, 350)

    def calculate_total_ot(self, obj):
        return (
            self.get_value_150(obj) +
            self.get_value_200(obj) +
            self.get_value_250(obj) +
            self.get_value_300(obj) +
            self.get_value_350(obj)
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.total_ot = self.calculate_total_ot(instance)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.total_ot = self.calculate_total_ot(instance)
        instance.save()
        return instance
    
    def get_status(self, obj):
        """ເຊັກຈາກ Overtime_history ວ່າມີບັນທຶກໃນເດືອນປັດຈຸບັນບໍ່"""
        from django.utils import timezone
        from .models import Overtime_history   # import ຂ້າງໃນ ຫຼື ໄວ້ດ້ານເທິງກໍ່ໄດ້

        now = timezone.now()

        exists = Overtime_history.objects.filter(
            date_insert__year=now.year,
            date_insert__month=now.month
        ).exists()

        if exists:
            return f"ຄິດໄລ່ເດືອນ {now.month} ແລ້ວ"
        return f"ເດືອນ {now.month} ບໍ່ທັນຄິດໄລ່"

    class Meta:
        model = OvertimeWork
        fields = [
            'ot_id',
            'date',
            'emp_id',
            'emp_name',
            'pos_id',
            'position',
            'csd_evening',
            'csd_night',
            'hd_mor_after',
            'hd_evening',
            'hd_night',
            'salary',
            'value_150',
            'value_200',
            'value_250',
            'value_300',
            'value_350',
            'total_ot',
            'status',
            # 'recorder',
            # 'recorder_name',
        ]

class Saving_cooperativeSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    total_Saving = serializers.SerializerMethodField()
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    pos_name = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    def get_total_Saving(self, obj):
        loan = obj.loan_amount or 0
        interest = obj.interest or 0
        deposit = obj.deposit or 0
        return loan + interest + deposit
    def get_date(self, obj):
        return date.today().strftime("%Y-%m-%d")
    def get_status(self, obj):
        """ເຊັກຈາກ saving_cooperative_history ວ່າມີບັນທຶກໃນເດືອນປັດຈຸບັນບໍ່"""
        from django.utils import timezone
        from .models import saving_cooperative_history   # import ຂ້າງໃນ ຫຼື ໄວ້ດ້ານເທິງກໍ່ໄດ້
        now = timezone.now()
        exists = saving_cooperative_history.objects.filter(
            date_insert__year=now.year,
            date_insert__month=now.month
        ).exists()

        if exists:
            return f"ຄິດໄລ່ເດືອນ {now.month} ແລ້ວ"
        return f"ເດືອນ {now.month} ບໍ່ທັນຄິດໄລ່"
    class Meta:
        model = Saving_cooperative
        fields = ['sc_id', 'date', 'emp_id', 'emp_name','pos_id','pos_name', 'loan_amount', 'interest', 'deposit', 'Loan_deduction_194','total_Saving','status']

class income_taxSerializer(serializers.ModelSerializer):
    class Meta:
        model = income_tax
        fields = '__all__'

class welfareSerializer(serializers.ModelSerializer):
    class Meta:
        model = welfare
        fields = '__all__'

class evaluation_scoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluation_score
        fields = '__all__'
class evaluation_score_empSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluation_score_emp
        fields = '__all__'

class health_allowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = monthly_payment
        fields  = '__all__'

class monthly_paymentSerializer(serializers.ModelSerializer):
    lao_name = serializers.CharField(source='emp_id.lao_name', read_only=True)
    pos_id = serializers.IntegerField(source='emp_id.pos_id.pos_id', read_only=True)
    position = serializers.CharField(source='emp_id.pos_id.name', read_only=True)
    salary = serializers.SerializerMethodField()
    ot = serializers.SerializerMethodField()
    net_salary = serializers.SerializerMethodField()
    fuel = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    year_subsidy = serializers.SerializerMethodField()
    year_subsidy_total = serializers.SerializerMethodField()
    position_subsidy = serializers.SerializerMethodField()
    basic_income = serializers.SerializerMethodField()
    wf_8 = serializers.SerializerMethodField()
    wf_5_5 = serializers.SerializerMethodField()
    wf_8_5 = serializers.SerializerMethodField()
    wf_6 = serializers.SerializerMethodField()
    unknown_1 = serializers.SerializerMethodField()
    unknown_2 = serializers.SerializerMethodField()
    unknown_3 = serializers.SerializerMethodField()
    unknown_4 = serializers.SerializerMethodField()
    unknown_5 = serializers.SerializerMethodField()
    unknown_6 = serializers.SerializerMethodField()
    unknown_7 = serializers.SerializerMethodField()
    regular_income = serializers.SerializerMethodField()
    other_income = serializers.SerializerMethodField()
    income_before_tax = serializers.SerializerMethodField()
    exempt = serializers.SerializerMethodField()
    tax_5 = serializers.SerializerMethodField()
    tax_10 = serializers.SerializerMethodField()
    tax_15 = serializers.SerializerMethodField()
    tax_20 = serializers.SerializerMethodField()
    tax_25 = serializers.SerializerMethodField()
    total_tax = serializers.SerializerMethodField()
    net_basic_income = serializers.SerializerMethodField()
    child_subsidy_total = serializers.SerializerMethodField()
    saving_total = serializers.SerializerMethodField()
    loan = serializers.SerializerMethodField()
    interest = serializers.SerializerMethodField()
    deposit = serializers.SerializerMethodField()
    loan_194 = serializers.SerializerMethodField()
    monthly_income = serializers.SerializerMethodField()

    def get_position_subsidy(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return None
        sp_id = SubsidyPosition.objects.filter(pos_id=employee.pos_id).first()
        return sp_id.grant if sp_id else None

    def get_age(self, obj):
        if not obj.emp_id:
            return None
        age_entry = Employee_lcic.objects.filter(emp_id=obj.emp_id.emp_id).first()
        return age_entry.age_entry if age_entry else None
    def get_year_subsidy(self, obj):
        age_entry = self.get_age(obj)
        try:
            age_entry = int(age_entry) if age_entry is not None else None
        except ValueError:
            age_entry = None
        if age_entry is not None and age_entry == 0:
            return 0
        if age_entry is not None and age_entry < 6:
            default_subsidy = SubsidyYear.objects.filter(sy_id=1).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry < 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=2).first()
            return default_subsidy.y_subsidy if default_subsidy else 0
        if age_entry is not None and age_entry > 26:
            default_subsidy = SubsidyYear.objects.filter(sy_id=3).first()
            return default_subsidy.y_subsidy if default_subsidy else 0

        subsidy_year = SubsidyYear.objects.filter(sy_id=obj.sy_id).first()
        return subsidy_year.y_subsidy if subsidy_year else 0

    def get_year_subsidy_total(self, obj):
        age_entry = self.get_age(obj)
        y_subsidy = self.get_year_subsidy(obj)
        unknown_1 = self.get_unknown_1(obj)
        unknown_2 = self.get_unknown_2(obj)
        unknown_3 = self.get_unknown_3(obj)
        unknown_4 = self.get_unknown_4(obj)
        unknown_5 = self.get_unknown_5(obj)
        unknown_6 = self.get_unknown_6(obj)
        unknown_7 = self.get_unknown_7(obj)
        try:
            age_entry = int(age_entry) if age_entry is not None else 0
        except ValueError:
            age_entry = 0
        try:
            y_subsidy = int(y_subsidy) if y_subsidy is not None else 0
        except ValueError:
            y_subsidy = 0
        return age_entry * y_subsidy +(unknown_1 or 0) + (unknown_2 or 0) + (unknown_3 or 0) + (unknown_4 or 0) + (unknown_5 or 0) + (unknown_6 or 0) + (unknown_7 or 0)

    def get_salary(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return None
        salary = Salary.objects.filter(pos_id=employee.pos_id).first()
        return salary.SalaryGrade if salary else None

    def get_ot(self, obj):
        overtime = OvertimeWork.objects.filter(emp_id=obj.emp_id).first()
        if not overtime:
            return None
        return overtime.total_ot if overtime.total_ot else 0

    def get_fuel(self, obj):
        employee = obj.emp_id
        if not employee or not employee.pos_id:
            return 0
        fuel_payment = FuelSubsidy.objects.filter(pos_id=employee.pos_id).first()
        return fuel_payment.total_fuel if fuel_payment and fuel_payment.total_fuel else 0

    def get_basic_income(self, obj):
        salary = self.get_salary(obj) or 0
        pos_subsidy = self.get_position_subsidy(obj) or 0
        year_subsidy = self.get_year_subsidy_total(obj) or 0
        ot = self.get_ot(obj) or 0
        return math.ceil(float(salary) + float(pos_subsidy) + float(year_subsidy) + float(ot))

    def get_regular_income(self, obj):
        return math.ceil(float(self.get_basic_income(obj) or 0) + float(self.get_fuel(obj) or 0))

    def get_other_income(self, obj):
        emp_id = obj.emp_id_id
        pos_id = obj.emp_id.pos_id_id
        employee = Employee_lcic.objects.filter(emp_id=emp_id).first()
        if not employee:
            return Decimal('0.0')
        jm = job_mobility.objects.filter(pos_id=pos_id).order_by('-date').first()
        if not jm:
            return Decimal('0.0')
        days = Decimal(jm.number_of_days or 0)
        amount = Decimal(jm.amount_per_day or 0)
        policy = Decimal(jm.jm_policy or 0)
        return float((days * amount) + policy)

    def get_income_before_tax(self, obj):
        return math.ceil(float(self.get_regular_income(obj) or 0) + float(self.get_other_income(obj) or 0))

    def get_tax_5(self, obj):
        income = self.get_income_before_tax(obj) or Decimal('0')
        if Decimal('1300000.00') < income <= Decimal('5000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            return (income - t1.calculation_base) * t2.tariff if t2 else Decimal('0')
        if income > Decimal('5000000.00'):
            t2 = income_tax.objects.filter(tax_id=2).first()
            return (t2.calculation_base * t2.tariff) if t2 else Decimal('0')

    def get_tax_10(self, obj):
        income = self.get_income_before_tax(obj) or Decimal('0')
        if Decimal('5000000.00') < income <= Decimal('15000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            return (income - (t1.calculation_base + t2.calculation_base)) * t3.tariff if t3 else Decimal('0')
        if income > Decimal('15000000.00'):
            t3 = income_tax.objects.filter(tax_id=3).first()
            return (t3.calculation_base * t3.tariff) if t3 else Decimal('0')

    def get_tax_15(self, obj):
        income = self.get_income_before_tax(obj) or Decimal('0')
        if Decimal('15000000.00') < income <= Decimal('25000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            t4 = income_tax.objects.filter(tax_id=4).first()
            return (income - (t1.calculation_base + t2.calculation_base + t3.calculation_base)) * t4.tariff if t4 else Decimal('0')
        if income > Decimal('25000000.00'):
            t4 = income_tax.objects.filter(tax_id=4).first()
            return (t4.calculation_base * t4.tariff) if t4 else Decimal('0')

    def get_tax_20(self, obj):
        income = self.get_income_before_tax(obj) or Decimal('0')
        if Decimal('25000000.00') < income <= Decimal('65000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            t4 = income_tax.objects.filter(tax_id=4).first()
            t5 = income_tax.objects.filter(tax_id=5).first()
            return (income - (t1.calculation_base + t2.calculation_base + t3.calculation_base + t4.calculation_base)) * t5.tariff if t5 else Decimal('0')
        if income > Decimal('65000000.00'):
            t5 = income_tax.objects.filter(tax_id=5).first()
            return (t5.calculation_base * t5.tariff) if t5 else Decimal('0')

    def get_tax_25(self, obj):
        income = self.get_income_before_tax(obj) or Decimal('0')
        if income > Decimal('65000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            t4 = income_tax.objects.filter(tax_id=4).first()
            t5 = income_tax.objects.filter(tax_id=5).first()
            t6 = income_tax.objects.filter(tax_id=6).first()
            return (income - (t1.calculation_base + t2.calculation_base + t3.calculation_base + t4.calculation_base + t5.calculation_base)) * t6.tariff if t6 else Decimal('0')

    def get_total_tax(self, obj):
        return math.ceil(float(sum([
            self.get_tax_5(obj) or 0,
            self.get_tax_10(obj) or 0,
            self.get_tax_15(obj) or 0,
            self.get_tax_20(obj) or 0,
            self.get_tax_25(obj) or 0
        ])))

    def get_net_basic_income(self, obj):
        return math.ceil(float(self.get_basic_income(obj) or 0) - float(self.get_total_tax(obj) or 0))

    def get_child_subsidy_total(self, obj):
        return math.ceil(float(obj.child_Subsidy) * float(obj.child))

    def get_loan(self, obj):
        saving = Saving_cooperative.objects.filter(emp_id=obj.emp_id).first()
        return saving.loan_amount if saving and saving.loan_amount else 0

    def get_interest(self, obj):
        saving = Saving_cooperative.objects.filter(emp_id=obj.emp_id).first()
        return saving.interest if saving and saving.interest else 0

    def get_deposit(self, obj):
        saving = Saving_cooperative.objects.filter(emp_id=obj.emp_id).first()
        return saving.deposit if saving and saving.deposit else 0

    def get_saving_total(self, obj):
        saving = Saving_cooperative.objects.filter(emp_id=obj.emp_id).first()
        if not saving:
            return 0
        return sum([saving.loan_amount or 0, saving.interest or 0, saving.deposit or 0])

    def get_loan_194(self, obj):
        saving = Saving_cooperative.objects.filter(emp_id=obj.emp_id).first()
        return saving.Loan_deduction_194 if saving and saving.Loan_deduction_194 else 0

    def get_net_salary(self, obj):
        return ((self.get_net_basic_income(obj) + self.get_child_subsidy_total(obj) + (obj.health_Subsidy or 0)) - (self.get_saving_total(obj) + self.get_loan_194(obj)))

    def get_exempt(self, obj):
        return 1300000

    def get_wf_8(self, obj): return 0
    def get_wf_5_5(self, obj): return 0
    def get_wf_8_5(self, obj): return 0
    def get_wf_6(self, obj): return 0
    def get_unknown_1(self, obj): return 0
    def get_unknown_2(self, obj): return 0
    def get_unknown_3(self, obj): return 0
    def get_unknown_4(self, obj): return 0
    def get_unknown_5(self, obj): return 0
    def get_unknown_6(self, obj): return 0
    def get_unknown_7(self, obj): return 0

    def get_monthly_income(self, obj):
        return math.ceil(float(self.get_other_income(obj) or 0) + float(self.get_net_salary(obj) or 0) + float(self.get_fuel(obj) or 0))

    class Meta:
        model = monthly_payment
        fields = [
            "id", "date", "emp_id", "lao_name", "pos_id", "position", "salary",
            "wf_8", "wf_5_5", "wf_8_5", "wf_6", "position_subsidy", "age", "year_subsidy",
            "unknown_1","unknown_2","unknown_3","unknown_4","unknown_5","unknown_6","unknown_7",
            "year_subsidy_total",
            "ot", "basic_income", "fuel", "regular_income", "other_income",
            "income_before_tax", "exempt", "tax_5", "tax_10", "tax_15", "tax_20", "tax_25",
            "total_tax", "net_basic_income", "child", "child_Subsidy", "child_subsidy_total",
            "health_Subsidy", "loan", "interest", "deposit", "saving_total", "loan_194",
            "net_salary","monthly_income"
        ]

class test_monlyserializers(serializers.ModelSerializer):
    class Meta:
        model = monthly_payment
        fields = '__all__'

#history serializers

class post_Overtime_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime_history
        fields = '__all__'
class get_Overtime_historyserializer(serializers.ModelSerializer):
    emp_name = serializers.SerializerMethodField()
    pos_name = serializers.SerializerMethodField()
    def get_emp_name(self, obj):
        emp_name = Employee_lcic.objects.filter(emp_id=obj.emp_id).first()
        if not obj.emp_id:
            return None
        return emp_name.lao_name
    def get_pos_name(self, obj):
        pos_name = Position.objects.filter(pos_id=obj.pos_id).first()
        if not obj.pos_id:
            return None
        return pos_name.name if pos_name else None
    class Meta:
        model = Overtime_history
        fields = ['date','ot_id', 'emp_id', 'emp_name','pos_name', 'csd_evening', 'csd_night', 
                  'hd_mor_after', 'hd_evening', 'hd_night','salary','value_150', 'value_200', 
                  'value_250', 'value_300', 'value_350', 'total_ot','recorder','recorder_name']

class post_colpolicy_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = colpolicy_history
        fields = '__all__'
class get_colpolicy_historyserializer(serializers.ModelSerializer):
    emp_name = serializers.SerializerMethodField()
    pos_name = serializers.SerializerMethodField()
    def get_emp_name(self, obj):
        emp_name = Employee_lcic.objects.filter(emp_id=obj.emp_id).first()
        if not obj.emp_id:
            return None
        return emp_name.lao_name
    def get_pos_name(self, obj):
        pos_name = Position.objects.filter(pos_id=obj.pos_id).first()
        if not obj.pos_id:
            return None
        return pos_name.name if pos_name else None
    class Meta:
        model = colpolicy_history
        fields = ['col_id', 'date','emp_id','emp_name', 'pos_name', 'number_of_days', 'amount_per_day', 'total_amount', 'jm_policy', 'total_payment','recorder','recorder_name']

class post_specialday_emp_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = specialday_emp_history
        fields = '__all__'
class get_specialday_emp_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = specialday_emp_history
        fields = '__all__'

class post_MobilePhoneSubsidy_emp_Historyserializer(serializers.ModelSerializer):
    class Meta:
        model = MobilePhoneSubsidy_emp_History
        fields = '__all__'
class get_MobilePhoneSubsidy_emp_Historyserializer(serializers.ModelSerializer):
    class Meta:
        model = MobilePhoneSubsidy_emp_History
        fields = '__all__'

class post_fuel_payment_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = fuel_payment_history
        fields = '__all__'
class get_fuel_payment_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = fuel_payment_history
        fields = ['fp_id', 'date', 'emp_name', 'position', 'fuel_subsidy', 'fuel_price', 'total_fuel','recorder','recorder_name']

class post_saving_cooperative_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = saving_cooperative_history
        fields = '__all__'
class get_saving_cooperative_historyserializer(serializers.ModelSerializer):
    emp_name = serializers.SerializerMethodField()
    def get_emp_name(self, obj):
        emp_name = Employee_lcic.objects.filter(emp_id=obj.emp_id).first()
        if not obj.emp_id:
            return None
        return emp_name.lao_name
    class Meta:
        model = saving_cooperative_history
        fields = ['id', 'date', 'emp_id', 'emp_name', 'loan_amount', 'interest', 'deposit', 'Loan_deduction_194', 'total_Saving','recorder','recorder_name']

class post_uniform_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = uniform_history
        fields = '__all__'
class get_uniform_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = uniform_history
        fields = '__all__'
    
class post_evaluation_score_emp_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = evaluation_score_emp_history
        fields = '__all__'
class get_evaluation_score_emp_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = evaluation_score_emp_history
        fields = '__all__'

class post_monthly_payment_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = monthly_payment_history
        fields = '__all__'
class get_monthly_payment_historyserializer(serializers.ModelSerializer):
    class Meta:
        model = monthly_payment_history
        fields = '__all__'
