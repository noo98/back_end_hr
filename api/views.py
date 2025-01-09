from django.shortcuts import render
from django.http import HttpResponse # type: ignore
from .models import Item
from django.contrib.auth import authenticate # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Employee_lcic,document_lcic
from .serializers import EmployeeSerializer  # ສ້າງ Serializer ກ່ອນ
# from .models import Document_out, UserLogin
# from .serializers import Document_outSerializer
# from .serializers import DocumentEntrySerializer
# from .models import DocumentEntry
from .models import activity
from .serializers import activitySerializer
from .models import Department  # Import your model
from .serializers import DepartmentSerializer,systemloginsSerializer,document_lcicSerializer
from .models import systemlogins,UserLogin
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
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
        permission_classes = [AllowAny] # type: ignore
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


class document_lcic_ListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = document_lcic.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = document_lcicSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class document_lcic_AddView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = document_lcicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class document_lcic_UpdateView(APIView):
    def put(self, request, doc_id):
        try:
            # ຄົ້ນຫາ Document ທີ່ຈະອັບເດດ
            document = document_lcic.objects.get(doc_id=doc_id)
        except document_lcic.DoesNotExist:
            return Response(
                {"error": f"Document with ID {doc_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # ອັບເດດຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = document_lcicSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class document_lcic_DeleteView(APIView):
    def delete(self, request, doc_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = document_lcic.objects.get(doc_id=doc_id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"document_lcic with ID {doc_id} deleted successfully."}, status=status.HTTP_200_OK)
        except document_lcic.DoesNotExist:
            return Response({"error": f"document_lcic with ID {doc_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        

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
    

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class Department_AddView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Department_UpdateView(APIView):
    def put(self, request, id):
        try:
            # ຄົ້ນຫາ Document ທີ່ຈະອັບເດດ
            document = Department.objects.get(id=id)
        except Department.DoesNotExist:
            return Response(
                {"error": f"Document with ID {id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # ອັບເດດຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = DepartmentSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class Department_DeleteView(APIView):
    def delete(self, request, id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = Department.objects.get(id=id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"Department with ID {id} deleted successfully."}, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"error": f"Department with ID {id} not found."}, status=status.HTTP_404_NOT_FOUND)

class LoginlistView(APIView):
    def get(self, request):
        user = systemlogins.objects.all()  # ດຶງຂໍ້ມູນທັງໝົດ
        serializer = systemloginsSerializer(user, many=True)  # ຕັ້ງ `many=True` ສຳລັບລາຍການທັງໝົດ
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginaddView(APIView):
    def post(self, request):
        try:
            # Get data from request
            data = request.data
            password = data.get("password")

            # Hash the password before saving
            if password:
                data["password"] = make_password(password)

            # Serialize the data
            serializer = systemloginsSerializer(data=data)

            # Validate and save the new user
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "User created successfully", "user": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            # Fetch the user by ID
            user = systemlogins.objects.get(user_id=user_id)
            
            # Get data from request
            data = request.data
            password = data.get("password")

            # Update username if provided
            if "username" in data:
                user.username = data["username"]

            # Hash and update the password if provided
            if password:
                user.password = make_password(password)

            # Save the updated user
            user.save()

            # Serialize the updated user
            serializer = systemloginsSerializer(user)
            return Response(
                {"message": "User updated successfully", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        except systemlogins.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteUserView(APIView):
    def delete(self, request, user_id, *args, **kwargs):
        try:
            # ค้นหาผู้ใช้ตาม user_id
            user = systemlogins.objects.get(user_id=user_id)

            # ลบผู้ใช้
            user.delete()
            return Response(
                {"message": f"ຜູ້ໃຊ້ທີ່ມີ ID {user_id} ຖືກລົບສຳເລັດ"},
                status=status.HTTP_200_OK,
            )
        except systemlogins.DoesNotExist:
            return Response(
                {"error": "ບໍ່ພົບຜູ້ໃຊ້ທີ່ຕ້ອງການລົບ"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"ມີຄວາມຜິດພາດ: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # ดึงข้อมูล username และ password จาก request
            username = request.data.get("username")
            password = request.data.get("password")

            # ตรวจสอบว่าข้อมูลถูกต้อง
            if not username or not password:
                return Response(
                    {"error": "ຕ້ອງການຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ค้นหาผู้ใช้ในฐานข้อมูล
            try:
                user = systemlogins.objects.get(username=username)

                # ตรวจสอบรหัสผ่าน
                if check_password(password, user.password):
                    return Response(
                        {"message": "ເຂົ້າລະບົບສຳເລັດ", "user": username},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except systemlogins.DoesNotExist:
                return Response(
                    {"error": "ຊື່ຜູ້ໃຊ້ບໍ່ຖືກຕ້ອງ"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Exception as e:
            return Response(
                {"error": f"ມີຄວາມຜິດພາດ: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        
#ວິທີທົດສອບການຄັ້ນຫາ: http://127.0.0.1:8000/api/search/document_lcic/?start_date=2025-01-01&end_date=2025-01-07&department=HR&doc_type=Report

class document_lcic_SearchView(APIView):
    def get(self, request):
        # ດືງຄ່າຄົ້ນຫາຈາກ Query Parameters
        search_query = request.query_params.get('q', None)  # ຄົ້ນຫາຂໍ້ມູນໂດຍ subject
        start_date = request.query_params.get('start_date', None)  # ວັນທີເລີ່ມຕົ້ນ
        end_date = request.query_params.get('end_date', None)  # ວັນທີສິ້ນສຸດ
        department = request.query_params.get('department', None)  # ພະແນກ
        doc_type = request.query_params.get('doc_type', None)  # ປະເພດຂອງເອກະສານ

        # ສ້າງ Query ສຳລັບຄົ້ນຫາ
        filters = {}
        if search_query:
            filters['subject__icontains'] = search_query
        if department:
            filters['department__icontains'] = department
        if doc_type:
            filters['doc_type__icontains'] = doc_type

        # ຄົ້ນຫາຂໍ້ມູນຕາມຊ່ວງວັນທີ
        if start_date and end_date:
            filters['insert_date__range'] = [start_date, end_date]

        # ຄົ້ນຫາຂໍ້ມູນຈາກ Model ດ້ວຍ Filters
        documents = document_lcic.objects.filter(**filters)

        # ຕວງສອບຂໍ້ມູນທີ່ຄົ້ນຫາ
        if documents.exists():
            serializer = document_lcicSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "No documents found matching your search query."},
            status=status.HTTP_404_NOT_FOUND
        )
