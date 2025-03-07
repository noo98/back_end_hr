from django.forms import ValidationError
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
        serializer = document_lcic_addSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
             
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
<<<<<<< HEAD
    
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

    def get(self, request, us_id=None, username=None):
        try:
            if us_id:
                user = SystemUser.objects.get(us_id=us_id)
            elif username:
                user = SystemUser.objects.get(username=username)
            else:
                users = SystemUser.objects.all()
                serializer = SystemUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            serializer = SystemUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SystemUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        user = get_object_or_404(SystemUser, us_id=us_id)  # Replaces try-except for DoesNotExist
        data = request.data
        updated = False  # Track if we made changes

        # Update username if provided
        username = data.get("username")
        if username:
            user.username = username
            updated = True

        # Update password securely if provided
        password = data.get("password")
        if password:
            user.password = make_password(password)  # Hash before saving
            updated = True

        if updated:  # Save only if changes were made
            user.save()
            serializer = SystemUserSerializer(user)
            return Response(
                {"message": "User updated successfully", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "No changes detected"},
                status=status.HTTP_400_BAD_REQUEST,
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

class document_general_SearchView(APIView):
    def get(self, request):
        search_query = request.query_params.get('subject', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        department = request.query_params.get('department', None)
        department_id = request.query_params.get('department_id', None)
        doc_type = request.query_params.get('doc_type', None)
        format_name = request.query_params.get('format', None)

        documents = document_general.objects.all()

        if search_query:
            documents = documents.filter(subject__icontains=search_query)
        if department:
            documents = documents.filter(department__name__icontains=department)
        if department_id:
            documents = documents.filter(department__id=department_id)
        if doc_type:
            documents = documents.filter(doc_type__icontains=doc_type)
        if format_name:
            documents = documents.filter(format__name__icontains=format_name)

        # Handle date range filtering only if insert_date is a DateField
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__gte=start_date)
            except ValueError:
                return Response({"message": "Invalid start_date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__lte=end_date)
            except ValueError:
                return Response({"message": "Invalid end_date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if documents.exists():
            serializer = document_general_Serializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "No documents found matching your search query."}, status=status.HTTP_404_NOT_FOUND)


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

    def put(self, request, docg_id):
        try:
            doc = document_general.objects.get(docg_id=docg_id)
        except document_general.DoesNotExist:
            return Response({"error": f"document_general with ID {docg_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = document_general_Serializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, docg_id):
        try:
            # ຄົ້ນຫາ Employee ດ້ວຍ emp_id
            doc = document_general.objects.get(docg_id=docg_id)
            doc.delete()  # ລຶບຂໍ້ມູນຈາກ Database
            return Response({"message": f"document_general with ID {docg_id} deleted successfully."}, status=status.HTTP_200_OK)
        except document_general.DoesNotExist:
            return Response({"error": f"document_general with ID {docg_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        

from .models import (PersonalInformation, Education,SpecializedEducation, PoliticalTheoryEducation, ForeignLanguage, WorkExperience, 
                     TrainingCourse, Award, DisciplinaryAction, FamilyMember, Evaluation)
from .serializers import (PersonalInformationSerializer, EducationSerializer, SpecializedEducationSerializer, AwardSerializer,
                          PoliticalTheoryEducationSerializer, ForeignLanguageSerializer, WorkExperienceSerializer, TrainingCourseSerializer,DisciplinaryActionSerializer,
                          FamilyMemberSerializer, EvaluationSerializer)
import logging
from django.db import transaction 
from rest_framework.generics import get_object_or_404
from typing import Optional
from django.db import transaction
logger = logging.getLogger(__name__)
class PersonalEducationCreateView(APIView):
    def get(self, request, per_id: Optional[int] = None):
        if per_id:
            personal_instances = PersonalInformation.objects.filter(per_id=per_id)
        else:
            personal_instances = PersonalInformation.objects.all()
        response_data = []
        for personal_instance in personal_instances:
            per_id = personal_instance.per_id
            education_instances = Education.objects.filter(per_id=per_id)
            specialized_instances = SpecializedEducation.objects.filter(per_id=per_id)
            political_instances = PoliticalTheoryEducation.objects.filter(per_id=per_id)
            language_instances = ForeignLanguage.objects.filter(per_id=per_id)
            work_instances = WorkExperience.objects.filter(per_id=per_id)
            training_instances = TrainingCourse.objects.filter(per_id=per_id)
            award_instances = Award.objects.filter(per_id=per_id)
            disciplinary_instances = DisciplinaryAction.objects.filter(per_id=per_id)
            family_instances = FamilyMember.objects.filter(per_id=per_id)
            evaluation_instance = Evaluation.objects.filter(per_id=per_id).first()
            response_data.append({
                "personal_information": PersonalInformationSerializer(personal_instance).data,
                "education": EducationSerializer(education_instances, many=True).data,
                "specialized_education": SpecializedEducationSerializer(specialized_instances, many=True).data,
                "political_theory_education": PoliticalTheoryEducationSerializer(political_instances, many=True).data,
                "foreign_languages": ForeignLanguageSerializer(language_instances, many=True).data,
                "work_experiences": WorkExperienceSerializer(work_instances, many=True).data,
                "training_courses": TrainingCourseSerializer(training_instances, many=True).data,
                "awards": AwardSerializer(award_instances, many=True).data,
                "disciplinary_actions": DisciplinaryActionSerializer(disciplinary_instances, many=True).data,
                "family_members": FamilyMemberSerializer(family_instances, many=True).data,
                "evaluation": EvaluationSerializer(evaluation_instance).data if evaluation_instance else None
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
    def save_related_data(self, serializer_class, dataset, per_id):
        try:
            for item in dataset:
                item["per_id"] = per_id
            serializer = serializer_class(data=dataset, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"Error saving {serializer_class.__name__}: {e}")
            raise e

    def post(self, request):
        data = request.data or {}

        personal_data_list = data.get('PersonalInformation', [])
        if not personal_data_list:
            return Response({"error": "ຂໍ້ມູນບໍ່ຖືກຮູບແບບ"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                personal_data = personal_data_list[0]
                personal_serializer = PersonalInformationSerializer(data=personal_data)
                personal_serializer.is_valid(raise_exception=True)
                personal_instance = personal_serializer.save()

                related_data_map = {
                    FamilyMemberSerializer: data.get('FamilyMember', []),
                    EducationSerializer: data.get('Education', []),
                    SpecializedEducationSerializer: data.get('SpecializedEducation', []),
                    PoliticalTheoryEducationSerializer: data.get('PoliticalTheoryEducation', []),
                    ForeignLanguageSerializer: data.get('ForeignLanguage', []),
                    WorkExperienceSerializer: data.get('WorkExperience', []),
                    TrainingCourseSerializer: data.get('TrainingCourse', []),
                    AwardSerializer: data.get('Award', []),
                    DisciplinaryActionSerializer: data.get('DisciplinaryAction', [])
                }

                for serializer_class, dataset in related_data_map.items():
                    self.save_related_data(serializer_class, dataset, personal_instance.per_id)

                evaluation_list = data.get('Evaluation', [])
                if evaluation_list:
                    evaluation_data = evaluation_list[0]
                    evaluation_data["per_id"] = personal_instance.per_id
                    evaluation_serializer = EvaluationSerializer(data=evaluation_data)
                    evaluation_serializer.is_valid(raise_exception=True)
                    evaluation_serializer.save()

            return Response({
                "message": "ບັນທຶກສຳເລັດ",
                "per_id": personal_instance.per_id,
                "name": personal_instance.full_name
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in post method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, per_id: int):
        data = request.data
        personal_data = data.get('personal_information', {})
        family_data = data.get('family_members', [])
        evaluation_data = data.get('evaluation', {})
        education_data = data.get('education', [])
        specialized_data = data.get('specialized_education', [])
        political_data = data.get('political_theory_education', [])
        language_data = data.get('foreign_languages', [])
        work_data = data.get('work_experiences', [])
        training_data = data.get('training_courses', [])
        award_data = data.get('awards', [])
        disciplinary_data = data.get('disciplinary_actions', [])

        personal_instance = get_object_or_404(PersonalInformation, per_id=per_id)

        try:
            with transaction.atomic():
                # 1. Update Personal Information
                personal_serializer = PersonalInformationSerializer(personal_instance, data=personal_data, partial=True)
                personal_serializer.is_valid(raise_exception=True)
                personal_serializer.save()

                # 2. Update Related Many-to-Many Data (Using Bulk Operations)
                def update_related_data(model_class, serializer_class, dataset):
                    existing_items = {obj.id: obj for obj in model_class.objects.filter(per_id=per_id)}
                    new_items = []
                    for item in dataset:
                        item["per_id"] = per_id
                        if "id" in item and item["id"] in existing_items:
                            serializer = serializer_class(existing_items[item["id"]], data=item, partial=True)
                        else:
                            serializer = serializer_class(data=item)
                        serializer.is_valid(raise_exception=True)
                        new_items.append(serializer)
                    model_class.objects.bulk_create(
                        [serializer.save() for serializer in new_items], ignore_conflicts=True
                    )

                update_related_data(FamilyMember, FamilyMemberSerializer, family_data)
                update_related_data(Education, EducationSerializer, education_data)
                update_related_data(SpecializedEducation, SpecializedEducationSerializer, specialized_data)
                update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, political_data)
                update_related_data(ForeignLanguage, ForeignLanguageSerializer, language_data)
                update_related_data(WorkExperience, WorkExperienceSerializer, work_data)
                update_related_data(TrainingCourse, TrainingCourseSerializer, training_data)
                update_related_data(Award, AwardSerializer, award_data)
                update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, disciplinary_data)

                # 3. Update Evaluation (If exists)
                if evaluation_data:
                    evaluation_instance, _ = Evaluation.objects.update_or_create(per_id=per_id, defaults=evaluation_data)

            return Response({
                "message": "ອັບເດດສຳເລັດ",
                "per_id": per_id,
                "name": personal_instance.full_name
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, per_id: int):
        personal_instance = get_object_or_404(PersonalInformation, per_id=per_id)
        try:
            with transaction.atomic():
                # ລຶບຂໍ້ມູນທີ່ມີຄວາມສຳພັນກັນ
                FamilyMember.objects.filter(per_id=per_id).delete()
                Education.objects.filter(per_id=per_id).delete()
                SpecializedEducation.objects.filter(per_id=per_id).delete()
                PoliticalTheoryEducation.objects.filter(per_id=per_id).delete()
                ForeignLanguage.objects.filter(per_id=per_id).delete()
                WorkExperience.objects.filter(per_id=per_id).delete()
                TrainingCourse.objects.filter(per_id=per_id).delete()
                Award.objects.filter(per_id=per_id).delete()
                DisciplinaryAction.objects.filter(per_id=per_id).delete()
                Evaluation.objects.filter(per_id=per_id).delete()

                # ລຶບຂໍ້ມູນຫຼັກ
                personal_instance.delete()

            return Response({"message": "ລຶບສຳເລັດ"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def delete(self, request):
    #     try:
    #         with transaction.atomic():
    #             # ລຶບທຸກຕາຕະລາງທີ່ກ່ຽວຂ້ອງ
    #             FamilyMember.objects.all().delete()
    #             Education.objects.all().delete()
    #             SpecializedEducation.objects.all().delete()
    #             PoliticalTheoryEducation.objects.all().delete()
    #             ForeignLanguage.objects.all().delete()
    #             WorkExperience.objects.all().delete()
    #             TrainingCourse.objects.all().delete()
    #             Award.objects.all().delete()
    #             DisciplinaryAction.objects.all().delete()
    #             Evaluation.objects.all().delete()
    #             PersonalInformation.objects.all().delete()

    #         return Response({"message": "ລຶບຂໍ້ມູນທັງໝົດສຳເລັດ"}, status=status.HTTP_204_NO_CONTENT)

    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


from .serializers import UpdateDocSerializer
from django.shortcuts import get_object_or_404

class UpdateDocumentStatus(APIView):
    def patch(self, request, doc_id):
        document = get_object_or_404(document_lcic, doc_id=doc_id)

        if not request.data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateDocSerializer(document, data=request.data, partial=True)

        if serializer.is_valid():
            if not any(request.data.values()):
                return Response({"error": "No changes detected"}, status=status.HTTP_400_BAD_REQUEST)

            new_status_values = request.data.get("status")
            if new_status_values:
                document.status.set(new_status_values)  # อัปเดต ManyToManyField

            # **ดึง department จาก SystemUser และกำหนดให้ document**
            user = request.user  # ใช้ request.user แทน us_id
            if user and hasattr(user, 'department'):
                document.department = user.department

            serializer.save()
            return Response(
                {"message": "Status updated successfully", "data": serializer.data}, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db import IntegrityError
from .models import Document_Status
from .serializers import DocStatusSerializer
class docstatus(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = Document_Status.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = DocStatusSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
            # ສະແດງຂໍ້ມູນ request ທີ່ໄດ້ຮັບ
            print("Request Data:", request.data)

            doc_id = request.data.get("doc_id")
            us_id = request.data.get("us_id")

            if not doc_id or not us_id:
                return Response({"error": "doc_id ແລະ us_id ຕ້ອງມີຄ່າ"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # ໃຊ້ update_or_create ເພື່ອປ່ຽນແປງຂໍ້ມູນຖ້າມີຢູ່ແລ້ວ
                document_status, created = Document_Status.objects.update_or_create(
                    doc_id_id=doc_id,  # ForeignKey ຕ້ອງໃຊ້ _id
                    us_id_id=us_id,
                )

                serializer = DocStatusSerializer(document_status)
                if created:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)  # ຖືກສ້າງໃໝ່
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK)  # ຖືກອັບເດດ

            except IntegrityError:
                return Response(
                    {"error": "ບໍ່ສາມາດບັນທຶກຂໍ້ມູນໄດ້"},
                    status=status.HTTP_400_BAD_REQUEST)
    

=======
    
>>>>>>> 9a6b161918926eb85e146bbbf084c8c402fe1d19
