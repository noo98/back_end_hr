from django.shortcuts import render
from django.http import HttpResponse # type: ignore
from .models import Item
from django.contrib.auth import authenticate # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Employee_lcic,document_lcic
from .serializers import EmployeeSerializer  # ສ້າງ Serializer ກ່ອນ
from .models import activity
from .models import SystemUser
from .serializers import SystemUserSerializer
from .serializers import activitySerializer,Document_formatSerializer
from .models import Department,Document_format,document_general
from .serializers import DepartmentSerializer,document_lcicSerializer,document_lcic_addSerializer,document_general_Serializer,StatusSerializer,SidebarSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import os
from django.conf import settings
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
from .authentication import CustomJWTAuthentication  # Import custom authentication
from .models import Status,Sidebar
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
def update_view_status(request, doc_id):
    if request.method == "POST":
        try:
            doc = document_lcic.objects.get(doc_id=doc_id)
            doc.status = "viewed"
            doc.save()
            return JsonResponse({"success": True, "message": "ປ່ຽນສະຖານະເປັນ viewed ສຳເລັດ"})
        except document_lcic.DoesNotExist:
            return JsonResponse({"success": False, "message": "ບໍ່ພົບເອກະສານ"}, status=404)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

def get_items(request):
    items = Item.objects.all().values('id', 'name', 'description', 'price')
    return Response(items)

class Employee_lcicView(APIView):

    # authentication_classes = [CustomJWTAuthentication]  # Use custom authentication
    # permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, emp_id=None):
        if emp_id:
            try:
                employee = Employee_lcic.objects.get(emp_id=emp_id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee_lcic.DoesNotExist:
                return Response({"error": "Employee_lcic not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            employees = Employee_lcic.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, emp_id):
        try:
            employee = Employee_lcic.objects.get(emp_id=emp_id)
        except Employee_lcic.DoesNotExist:
            return Response({"error": f"Employee with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, emp_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            employee = Employee_lcic.objects.get(emp_id=emp_id)
            employee.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"employee with ID {emp_id} deleted successfully."}, status=status.HTTP_200_OK)
        except Employee_lcic.DoesNotExist:
            return Response({"error": f"employee with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)


class document_lcic_ListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = document_lcic.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = document_lcicSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class document_lcic_List_idView(APIView):
    def get(self, request, doc_id):
        """
        ດຶງຂໍ້ມູນຂອງພະນັກງານຈາກ doc_id
        """
        if not doc_id:
            return Response({"error": "doc_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = document_lcic.objects.get(doc_id=doc_id)
            serializer = document_lcicSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except document_lcic.DoesNotExist:
            return Response({"error": "document_lcic not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class document_lcic_AddView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = document_lcic_addSerializer(data=request.data)
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
             

class document_lcic_deleteView(APIView):
    def delete(self, request, doc_id):
        """
        ລຶບຂໍ້ມູນ document ຈາກ database ແລະລົບໄຟລ໌ທີ່ກ່ຽວຂ້ອງອອກຈາກ server
        """
        try:
            # ຄົ້ນຫາຂໍ້ມູນ document ຈາກ doc_id
            document = document_lcic.objects.get(doc_id=doc_id)
            
            # ກວດສອບທາງໄຟລ໌
            if document.file:  # ສັນດານເວລາຂຽນ Model ໄຟລ໌ຈະມີຊື່ field ວ່າ file_field
                file_path = os.path.join(settings.MEDIA_ROOT, document.file .name)
                
                # ລຶບໄຟລ໌ຖ້າມີ
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # ລຶບຂໍ້ມູນ document ຈາກ database
            document.delete()
            return Response({"message": "Document and file deleted successfully"}, status=status.HTTP_200_OK)

        except document_lcic.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
           
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
    
class DepartmentList_idView(APIView):
    def get(self, request, id):
        if not id:
            return Response({"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            document = Department.objects.get(id=id)
            serializer = DepartmentSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        # authentication_classes = [CustomJWTAuthentication]  # Use custom authentication
        # permission_classes = [IsAuthenticated]  # Require authentication
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

#
#
#


class Document_format_ListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = Document_format.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = Document_formatSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Document_format_idView(APIView):
    def get(self, request, dmf_id):
        """
        ດຶງຂໍ້ມູນຂອງພະນັກງານຈາກ dmf_id
        """
        if not id:
            return Response({"error": "dmf_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = Document_format.objects.get(dmf_id=dmf_id)
            serializer = Document_formatSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Document_format.DoesNotExist:
            return Response({"error": "Document_format not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
class Document_format_AddView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = Document_formatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Document_format_UpdateView(APIView):
    def put(self, request, dmf_id):
        try:
            # ຄົ້ນຫາ Document ທີ່ຈະອັບເດດ
            document = Document_format.objects.get(dmf_id=dmf_id)
        except Document_format.DoesNotExist:
            return Response(
                {"error": f"Document_format with ID {dmf_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # ອັບເດດຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = Document_formatSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             

class Document_format_DeleteView(APIView):
    def delete(self, request, dmf_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Document = Document_format.objects.get(dmf_id=dmf_id)
            Document.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"Department with ID {dmf_id} deleted successfully."}, status=status.HTTP_200_OK)
        except Document_format.DoesNotExist:
            return Response({"error": f"Department with ID {dmf_id} not found."}, status=status.HTTP_404_NOT_FOUND)
#
#
#



class UserView(APIView):

    def get(self, request, username=None):
            # authentication_classes = [CustomJWTAuthentication]  # Use custom authentication
            # permission_classes = [IsAuthenticated]  # Require authentication
            if username:  # If us_id is provided, fetch the specific user
                try:
                    user = SystemUser.objects.get(username=username)
                    serializer = SystemUserSerializer(user) 
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except SystemUser.DoesNotExist:
                    return Response({"error": "SystemUser not found"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # If no us_id is provided, fetch all users
                users = SystemUser.objects.all()
                serializer = SystemUserSerializer(users, many=True)
                return Response(serializer.data)

    def post(self, request):
        try:
            data = request.data
            password = data.get("password")

            if password:
                data["password"] = make_password(password)

            serializer = SystemUserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "User created successfully", "user": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, us_id):
        try:
            user = SystemUser.objects.get(us_id=us_id)
            data = request.data
            password = data.get("password")

            if "username" in data:
                user.username = data["username"]
            if password:
                user.password = make_password(password)

            user.save()
            serializer = SystemUserSerializer(user)
            return Response(
                {"message": "User updated successfully", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        except SystemUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, us_id):
        try:
            user = SystemUser.objects.get(us_id=us_id)
            user.delete()
            return Response(
                {"message": f"User with ID {us_id} deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except SystemUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "ຈຳເປັນຕ້ອງມີຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = SystemUser.objects.get(username=username)
        except SystemUser.DoesNotExist:
            return Response(
                {"error": "ຊື່ຜູ້ໃຊ້ ຫລື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if check_password(password, user.password):
            # Create JWT tokens manually
            refresh = RefreshToken()
            refresh["user_id"] = user.us_id  # Store user ID in the token
            refresh["username"] = user.username  # Optional: Store username for debugging

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "message": "ການລ໋ອກອິນສຳເລັດ",
                    "user": username,
                    "access_token": access_token,
                    # "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "ຊື່ຜູ້ໃຊ້ ຫລື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class document_lcic_SearchView(APIView):
    def get(self, request):
        # Get search query parameters
        search_query = request.query_params.get('subject', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        department = request.query_params.get('department', None)
        department_id = request.query_params.get('department_id', None)
        department_into = request.query_params.get('department_into', None)
        doc_type = request.query_params.get('doc_type', None)
        doc_type_info = request.query_params.get('doc_type_info', None)
        format_name = request.query_params.get('format', None)

        # Initialize the base query
        documents = document_lcic.objects.all()

        # Apply search filters
        if search_query:
            documents = documents.filter(subject__icontains=search_query)
        if department:
            documents = documents.filter(department__name__icontains=department)
        if department_id:
            documents = documents.filter(department__id=department_id)
        if doc_type:
            documents = documents.filter(doc_type__icontains=doc_type)
        if doc_type_info:
            documents = documents.filter(doc_type_info__icontains=doc_type_info)
        if format_name:
            documents = documents.filter(format__name__icontains=format_name)

        # Handle date range filtering
        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__gte=start_date)
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__lte=end_date)
        except ValueError:
            return Response(
                {"message": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if department_into:
            # Filter documents by department name (case-insensitive)
            documents = documents.filter(department_into__name__icontains=department_into)
            print(f"{documents.count()} matching documents found for department '{department_into}'")

        # Check if any documents match the filters
        if documents.exists():
            serializer = document_lcicSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "No documents found matching your search query."},
            status=status.HTTP_404_NOT_FOUND
        )

class EmployeeInfoAPI(APIView):
    def get(self, request):
        users = SystemUser.objects.select_related('Department', 'Employee').all()
        employee_data = []

        for user in users:
            employee_data.append({
                "Department": user.Department.name if hasattr(user.Department, 'name') else "N/A",
                "Employee Name (Lao)": user.Employee.lao_name,
                "Employee Name (Eng)": user.Employee.eng_name,
                "Nickname": user.Employee.nickname,
                "Gender": user.Employee.Gender
            })

        return Response(employee_data, status=status.HTTP_200_OK)


class document_general_View(APIView):
    # authentication_classes = [CustomJWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, docg_id=None):
        if docg_id:
            try:
                doc = document_general.objects.get(docg_id=docg_id)
                serializer = document_general_Serializer(doc)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except document_general.DoesNotExist:
                return Response({"error": "document_general not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            doc = document_general.objects.all()
            serializer = document_general_Serializer(doc, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = document_general_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, emp_id):
        try:
            doc = document_general.objects.get(emp_id=emp_id)
        except document_general.DoesNotExist:
            return Response({"error": f"document_general with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = document_general_Serializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, emp_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            doc = document_general.objects.get(emp_id=emp_id)
            doc.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"document_general with ID {emp_id} deleted successfully."}, status=status.HTTP_200_OK)
        except document_general.DoesNotExist:
            return Response({"error": f"document_general with ID {emp_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PersonalInformation, Education
from .serializers import PersonalInformationSerializer, EducationSerializer
from django.db import transaction

class PersonalEducationCreateView(APIView):
    # authentication_classes = [CustomJWTAuthentication]  # Use custom authentication
    # permission_classes = [IsAuthenticated]  # Require authentication
    def get(self, request):
        # Get all personal information
        personal_data = PersonalInformation.objects.all()
        personal_serializer = PersonalInformationSerializer(personal_data, many=True)

        result = []
        for person in personal_serializer.data:
            # Get related education records
            education_data = Education.objects.filter(per_id=person['per_id'])
            education_serializer = EducationSerializer(education_data, many=True)
            
            # Combine personal and education data
            person_info = {
                "personal_information": person,
                "education": education_serializer.data
            }
            result.append(person_info)

        return Response(result, status=status.HTTP_200_OK)
        
    def post(self, request):
        personal_data = request.data.get('personal_information')
        education_data = request.data.get('education')

        # Validate and save PersonalInformation
        personal_serializer = PersonalInformationSerializer(data=personal_data)
        if personal_serializer.is_valid():
            personal_instance = personal_serializer.save()
        else:
            return Response(personal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save Education
        for edu in education_data:
            edu['per_id'] = personal_instance.per_id  # Attach personal FK
            education_serializer = EducationSerializer(data=edu)
            if education_serializer.is_valid():
                education_serializer.save()
            else:
                return Response(education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "saved successfully"},
            status=status.HTTP_201_CREATED
        )
    def delete(self, request, per_id):
            try:
                with transaction.atomic():  # Ensure atomicity
                    # Get the personal information record
                    personal_instance = PersonalInformation.objects.get(per_id=per_id)
                    
                    # Delete related education records
                    Education.objects.filter(per_id=per_id).delete()
                    
                    # Delete personal information record
                    personal_instance.delete()
                    
                return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            
            except PersonalInformation.DoesNotExist:
                return Response({"error": "Personal information not found"}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class permission_lcic_View(APIView):
    def get(self, request, sta_id=None):
        if sta_id:
            try:
                sta_id = Status.objects.get(sta_id=sta_id)
                serializer = StatusSerializer(sta_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Status.DoesNotExist:
                return Response({"error": "Status_lcic not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            sta_id = Status.objects.all()
            serializer = StatusSerializer(sta_id, many=True)
            return Response(serializer.data)

    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ບັນທຶກຂໍ້ມູນໃນ Database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, sta_id):
        # authentication_classes = [CustomJWTAuthentication]  # Use custom authentication
        # permission_classes = [IsAuthenticated]  # Require authentication
        try:
            # ຄົ້ນຫາ Document ທີ່ຈະອັບເດດ
            Sid = Status.objects.get(sta_id=sta_id)
        except Status.DoesNotExist:
            return Response(
                {"error": f"Status with ID {sta_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # ອັບເດດຂໍ້ມູນໃນ Database ຜ່ານ Serializer
        serializer = StatusSerializer(Sid, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, sta_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            Sid = Status.objects.get(sta_id=sta_id)
            Sid.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"Status with ID {sta_id} deleted successfully."}, status=status.HTTP_200_OK)
        except Status.DoesNotExist:
            return Response({"error": f"Status with ID {sta_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
class sidebar_View(APIView):
    def get(self, request, sid_id=None):
        if sid_id:
            try:
                sid_id = Sidebar.objects.get(sid_id=sid_id)
                serializer = SidebarSerializer(sid_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Status.DoesNotExist:
                return Response({"error": "Sidebar not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            sid_id = Sidebar.objects.all()
            serializer = SidebarSerializer(sid_id, many=True)
            return Response(serializer.data)



