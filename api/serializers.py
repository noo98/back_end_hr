from rest_framework import serializers # type: ignore
from .models import Employee_lcic
from .models import Document_out,DocumentEntry,activity
from .models import UserLogin,Department

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_lcic
        fields = '__all__'


class Document_outSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_out
        fields = '__all__'  # ຫຼືລະບຸຟິວທີ່ຈະສົ່ງຄືນ

class DocumentEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentEntry
        fields = ['date', 'number', 'subject', 'section', 'receiver', 'document', 'file']  # ຫຼືລະບຸຟິວທີ່ຈະສົ່ງຄືນ

class activitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity
        fields = '__all__'  # ຄືນຄ່າທຸກ field ຂອງ model


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['user_id', 'username', 'password']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']