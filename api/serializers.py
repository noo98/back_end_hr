from rest_framework import serializers # type: ignore
from .models import Employee_lcic
# from .models import Documentout,Documentin
from .models import systemlogins,Department,activity,document_lcic

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_lcic
        fields = '__all__'

class document_lcicSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)  # ດຶງຊື່ພະແນກ
    class Meta:
        model = document_lcic
        fields = ['doc_id','insert_date','doc_number','subject','section','doc_type','department_name','document_detail','name']  # ຫຼືລະບຸຟິວທີ່ຈະສົ່ງຄືນ

class activitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity
        fields = '__all__'  # ຄືນຄ່າທຸກ field ຂອງ model


class systemloginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = systemlogins
        fields = ['user_id', 'username', 'password']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']