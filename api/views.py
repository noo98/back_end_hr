from django.shortcuts import render
from django.http import HttpResponse # type: ignore
from .models import Item
from django.contrib.auth import authenticate # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Employee_lcic
from .serializers import EmployeeSerializer  # ສ້າງ Serializer ກ່ອນ
from .models import Document_out, UserLogin
from .serializers import Document_outSerializer
from .serializers import DocumentEntrySerializer
from .models import DocumentEntry
from .models import activity
from .serializers import activitySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




def get_items(request):
    items = Item.objects.all().values('id', 'name', 'description', 'price')
    return Response(items)


class EmployeeListAPI(APIView):
    def get(self, request):
        employees = Employee_lcic.objects.all()  # ດຶງຂໍ້ມູນທັງໝົດ
        serializer = EmployeeSerializer(employees, many=True)  # ຕັ້ງ `many=True` ສຳລັບລາຍການທັງໝົດ
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeDetailView(APIView):
    def get(self, request, emp_id=None):
        """
        ດຶງຂໍ້ມູນຂອງພະນັກງານຈາກ emp_id
        """
        try:
            if emp_id:
                employee = Employee_lcic.objects.get(emp_id=emp_id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "emp_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Employee_lcic.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


class EmployeeCreateView(APIView):
    
    def post(self, request):
        permission_classes = [AllowAny]
        # ຮັບຂໍ້ມູນຈາກຄຳຂໍ
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EmployeeDeleteView(APIView):
    def delete(self, request, emp_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            employee = Employee_lcic.objects.get(emp_id=emp_id)
            employee.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"Employee with ID {emp_id} deleted successfully."}, status=status.HTTP_200_OK)
        except Employee_lcic.DoesNotExist:
            return Response({"error": f"Employee with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)


  # ໃຊ້ Serializer ທີ່ສ້າງໄວ້ແລ້ວ

class EmployeeUpdateView(APIView):
    def put(self, request, emp_id):
        try:
            # ຄົ້ນຫາ Employee ທີ່ຈະອັບເດດ
            employee = Employee_lcic.objects.get(emp_id=emp_id)
        except Employee_lcic.DoesNotExist:
            return Response({"error": f"Employee with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # ປັບປຸງຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Document_outListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = Document_out.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = Document_outSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Document_outCreateView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = Document_outSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Document_outDeleteView(APIView):
    def delete(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = Document_out.objects.get(id=id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"Document_out with ID {id} deleted successfully."}, status=status.HTTP_200_OK)
        except Document_out.DoesNotExist:
            return Response({"error": f"Document_out with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
class Document_outUpdateView(APIView):
    def put(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ທີ່ຈະອັບເດດ
            Document = Document_out.objects.get(id=id)
        except Document_out.DoesNotExist:
            return Response({"error": f"Document_out with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # ປັບປຸງຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = Document_outSerializer(Document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentEntryListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = DocumentEntry.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = DocumentEntrySerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DocumentEntryCreateView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = DocumentEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentEntryDeleteView(APIView):
    def delete(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = DocumentEntry.objects.get(id=id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"DocumentEntry with ID {id} deleted successfully."}, status=status.HTTP_200_OK)
        except DocumentEntry.DoesNotExist:
            return Response({"error": f"DocumentEntry with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
class DocumentEntryUpdateView(APIView):
    def put(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ທີ່ຈະອັບເດດ
            Document = DocumentEntry.objects.get(id=id)
        except DocumentEntry.DoesNotExist:
            return Response({"error": f"DocumentEntry with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # ປັບປຸງຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = DocumentEntrySerializer(Document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class activityListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = activity.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = activitySerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class activityCreateView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = activitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class activityDeleteView(APIView):
    def delete(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = activity.objects.get(id=id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"activity with ID {id} deleted successfully."}, status=status.HTTP_200_OK)
        except activity.DoesNotExist:
            return Response({"error": f"activity with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
class activityUpdateView(APIView):
    def put(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ທີ່ຈະອັບເດດ
            Document = activity.objects.get(id=id)
        except activity.DoesNotExist:
            return Response({"error": f"activity with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # ປັບປຸງຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = activitySerializer(Document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from .models import UserLogin as UserLoginModel  # Alias for the model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')  # Use "password" instead of "password_hash"

        # Check for missing fields
        if not username or not password:
            return Response(
                {'msg': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch user by username
            user = UserLoginModel.objects.get(username=username,password_hash=password)


            # On successful authentication
            return Response(
                {'msg': 'Login successful', 'redirect_url': '/'},
                status=status.HTTP_200_OK
            )
        

        except UserLoginModel.DoesNotExist:
            return Response(
                {'msg': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)