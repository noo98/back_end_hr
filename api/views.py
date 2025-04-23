from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Employee_lcic,document_lcic
from .serializers import EmployeeSerializer  # ສ້າງ Serializer ກ່ອນ
from .models import activity
from .models import SystemUser
from .serializers import SystemUserSerializer,DocumentFormatSerializer,DocumentFormat_Serializer
from .serializers import activitySerializer
from .models import Department,Document_format,document_general
from .serializers import DepartmentSerializer,document_lcicSerializer,DocumentLcic_AddSerializer,document_general_Serializer,StatusSerializer,SidebarSerializer
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
from django.utils import timezone
from .models import (PersonalInformation, Education,SpecializedEducation, PoliticalTheoryEducation, ForeignLanguage, WorkExperience, 
TrainingCourse, Award, DisciplinaryAction, FamilyMember, Evaluation)
from .serializers import (PersonalInformationSerializer, EducationSerializer, SpecializedEducationSerializer, AwardSerializer,
PoliticalTheoryEducationSerializer, ForeignLanguageSerializer, WorkExperienceSerializer, TrainingCourseSerializer,DisciplinaryActionSerializer,
FamilyMemberSerializer, EvaluationSerializer)
from .models import Document_Status
# from .serializers import Asset_typeSerializer,AssetSerializer
# from .models import Category
# from .serializers import categorySerializer
import logging
from django.db import transaction 
from rest_framework.generics import get_object_or_404
from typing import Optional
logger = logging.getLogger(__name__)
# from django.views.decorators.csrf import csrf_exempt
import json

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


class document_lcic_ListView(APIView):
    def get(self, request):
        # ດຶງຂໍ້ມູນທັງໝົດ
        Document = document_lcic.objects.all()
        # ແປງຂໍ້ມູນໃຊ້ Serializer
        serializer = document_lcicSerializer(Document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class document_lcic_List_idView(APIView):
    def get(self, request, doc_id):
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
        # ເຊັກວ່າຂໍ້ມູນທີ່ຮັບເປັນ list ຫຼື object ດຽວ
        if isinstance(request.data, list):
            serializer = DocumentLcic_AddSerializer(data=request.data, many=True)
        else:
            serializer = DocumentLcic_AddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer = DocumentLcic_AddSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             

class document_lcic_deleteView(APIView):
    def delete(self, request, doc_id):
        try:
            document = document_lcic.objects.get(doc_id=doc_id)
            if document.file:  # ສັນດານເວລາຂຽນ Model ໄຟລ໌ຈະມີຊື່ field ວ່າ file_field
                file_path = os.path.join(settings.MEDIA_ROOT, document.file .name)
                if os.path.exists(file_path):
                    os.remove(file_path)
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
        data = request.data
        # ກວດສອບວ່າຂໍ້ມູນເປັນ List ຫຼື Single Object
        is_many = isinstance(data, list)
        serializer = DepartmentSerializer(data=data, many=is_many)
        if serializer.is_valid():
            serializer.save()
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
        serializer = DocumentFormatSerializer(Document, many=True)
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
            serializer = DocumentFormatSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Document_format.DoesNotExist:
            return Response({"error": "Document_format not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
class Document_format_AddView(APIView):
    def post(self, request):
        # ປະມວນຜົນຂໍ້ມູນທີ່ສົ່ງມາຜ່ານ Serializer
        serializer = DocumentFormat_Serializer(data=request.data)
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
        serializer = DocumentFormatSerializer(document, data=request.data, partial=True)  # partial=True ສຳລັບອັບເດດບາງສ່ວນ
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
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(
#                 {"error": "ຈຳເປັນຕ້ອງມີຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             user = SystemUser.objects.get(username=username)
#         except SystemUser.DoesNotExist:
#             return Response(
#                 {"error": "ຊື່ຜູ້ໃຊ້ ຫຼື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         if check_password(password, user.password):
#             refresh = RefreshToken.for_user(user)
#             refresh["user_id"] = user.us_id
#             refresh["username"] = user.username

#             return Response(
#                 {
#                     "message": "ການລ໋ອກອິນສຳເລັດ",
#                     "user": user.username,
#                     "access_token": str(refresh.access_token),
#                     "refresh_token": str(refresh),
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"error": "ຊື່ຜູ້ໃຊ້ ຫຼື ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
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
        search_query = request.query_params.get("subject", None)
        start_date = request.query_params.get("start_date", None)

        
        end_date = request.query_params.get("end_date", None)
        department = request.query_params.get("department", None)
        department_id = request.query_params.get("department_id", None)
        doc_type = request.query_params.get("doc_type", None)
        format_name = request.query_params.get("format", None)
        status_doc = request.query_params.get("status_doc", None)  # ເພີ່ມ filter ສະຖານະເອກະສານ

        # ເລີ່ມຕົ້ນ Query ສໍາລັບຄົ້ນຫາ
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
        if status_doc:
            documents = documents.filter(status_doc=status_doc)

        # Handle date range filtering only if insert_date is a DateField
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__gte=start_date)
            except ValueError:
                return Response(
                    {"message": "Invalid start_date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                documents = documents.filter(insert_date__lte=end_date)
            except ValueError:
                return Response(
                    {"message": "Invalid end_date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if documents.exists():
            serializer = document_general_Serializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "No documents found matching your search query."},
            status=status.HTTP_404_NOT_FOUND,
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
            doc = document_general.objects.all().order_by('-docg_id')  # ສະແດງຈາກ ID ສູງຫາຕ່ຳ
            serializer = document_general_Serializer(doc, many=True)
            return Response(serializer.data)
        
        
    def post(self, request):
            doc_number = request.data.get("doc_number")  # ດຶງ doc_number ຈາກ request
            existing_doc = document_general.objects.filter(doc_number=doc_number).first()
            if existing_doc:
                return Response(status=status.HTTP_301_MOVED_PERMANENTLY)
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
        


from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile


class Employee_lcicView(APIView):
    def get(self, request, emp_id: int = None):
        if emp_id:
            employee_instances = Employee_lcic.objects.filter(emp_id=emp_id)
        else:
            employee_instances = Employee_lcic.objects.all()
        response_data = []
        for employee in employee_instances:
            emp_id = employee.emp_id

            personal_instances = PersonalInformation.objects.filter(emp_id=emp_id)
            education_instances = Education.objects.filter(emp_id=emp_id)
            specialized_instances = SpecializedEducation.objects.filter(emp_id=emp_id)
            political_instances = PoliticalTheoryEducation.objects.filter(emp_id=emp_id)
            language_instances = ForeignLanguage.objects.filter(emp_id=emp_id)
            work_instances = WorkExperience.objects.filter(emp_id=emp_id)
            training_instances = TrainingCourse.objects.filter(emp_id=emp_id)
            award_instances = Award.objects.filter(emp_id=emp_id)
            disciplinary_instances = DisciplinaryAction.objects.filter(emp_id=emp_id)
            family_instances = FamilyMember.objects.filter(emp_id=emp_id)
            evaluation_instance = Evaluation.objects.filter(emp_id=emp_id).first()

            response_data.append({
                "employee": EmployeeSerializer(employee).data,
                "personal_information": PersonalInformationSerializer(personal_instances, many=True).data,
                "education": EducationSerializer(education_instances, many=True).data,
                "specialized_education": SpecializedEducationSerializer(specialized_instances, many=True).data,
                "political_theory_education": PoliticalTheoryEducationSerializer(political_instances, many=True).data,
                "foreign_languages": ForeignLanguageSerializer(language_instances, many=True).data,
                "work_experiences": WorkExperienceSerializer(work_instances, many=True).data,
                "training_courses": TrainingCourseSerializer(training_instances, many=True).data,
                "awards": AwardSerializer(award_instances, many=True).data,
                "disciplinary_actions": DisciplinaryActionSerializer(disciplinary_instances, many=True).data,
                "family_members": FamilyMemberSerializer(family_instances, many=True).data,
                "evaluation": EvaluationSerializer(evaluation_instance).data if evaluation_instance else None,
            })
        return Response(response_data, status=status.HTTP_200_OK)

    def save_related_data(self, serializer_class, dataset, emp_id):
        try:
            for item in dataset:
                item["emp_id"] = emp_id
            serializer = serializer_class(data=dataset, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"Error saving {serializer_class._name_}: {e}")
            raise e

    def post(self, request):
        try:
            # Get JSON data from 'data' field (sent as multipart/form-data)
            json_data = json.loads(request.POST.get('data', '{}'))
            pic_file = request.FILES.get('pic')  # Get the uploaded file

            # Validate that Employee_lcic exists
            employee_data_list = json_data.get('Employee_lcic', [])
            if not employee_data_list:
                return Response({"error": "ບໍ່ມີຂໍ້ມູນ Employee_lcic"}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                employee_data = employee_data_list[0]
                if pic_file:
                    employee_data['pic'] = pic_file  # Add the file to employee data
                employee_serializer = EmployeeSerializer(data=employee_data)
                employee_serializer.is_valid(raise_exception=True)
                employee_instance = employee_serializer.save()
                related_data_map = {
                    PersonalInformationSerializer: json_data.get('PersonalInformation', []),
                    FamilyMemberSerializer: json_data.get('FamilyMember', []),
                    EducationSerializer: json_data.get('Education', []),
                    SpecializedEducationSerializer: json_data.get('SpecializedEducation', []),
                    PoliticalTheoryEducationSerializer: json_data.get('PoliticalTheoryEducation', []),
                    ForeignLanguageSerializer: json_data.get('ForeignLanguage', []),
                    WorkExperienceSerializer: json_data.get('WorkExperience', []),
                    TrainingCourseSerializer: json_data.get('TrainingCourse', []),
                    AwardSerializer: json_data.get('Award', []),
                    DisciplinaryActionSerializer: json_data.get('DisciplinaryAction', [])
                }
                for serializer_class, dataset in related_data_map.items():
                    self.save_related_data(serializer_class, dataset, employee_instance.emp_id)
                evaluation_list = json_data.get('Evaluation', [])
                if evaluation_list:
                    evaluation_data = evaluation_list[0]
                    evaluation_data["emp_id"] = employee_instance.emp_id
                    evaluation_serializer = EvaluationSerializer(data=evaluation_data)
                    evaluation_serializer.is_valid(raise_exception=True)
                    evaluation_serializer.save()
            return Response({
                "success": True,
                "message": "ບັນທຶກສຳເລັດ",
                "emp_id": employee_instance.emp_id,
                "name": employee_instance.lao_name
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in post method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, emp_id: int):
            dataset = request.data

            # ✅ รองรับทั้ง object เดียว และ list
            if isinstance(dataset, dict):
                dataset = [dataset]
            elif not isinstance(dataset, list):
                return Response({"error": "Expected a list or a single data object."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    for item in dataset:
                        # ✅ ดึงและแปลง employee เป็น dictionary
                        employee_json = item.get('employee')
                        if employee_json is None:
                            return Response({"error": "Missing 'employee' data."}, status=status.HTTP_400_BAD_REQUEST)

                        # รองรับทั้ง string และ dict
                        if isinstance(employee_json, str):
                            try:
                                employee_data = json.loads(employee_json)
                            except json.JSONDecodeError:
                                return Response({"error": "Invalid JSON format in 'employee' data."}, status=status.HTTP_400_BAD_REQUEST)
                        elif isinstance(employee_json, dict):
                            employee_data = employee_json
                        else:
                            return Response({"error": "Invalid type for 'employee' data."}, status=status.HTTP_400_BAD_REQUEST)

                        if not employee_data:
                            return Response({"error": "Empty 'employee' data."}, status=status.HTTP_400_BAD_REQUEST)

                        # 📌 ดึงข้อมูลย่อย
                        personal_data = item.get('personal_information', [])
                        education_data = item.get('education', [])
                        specialized_data = item.get('specialized_education', [])
                        political_data = item.get('political_theory_education', [])
                        language_data = item.get('foreign_languages', [])
                        work_data = item.get('work_experiences', [])
                        training_data = item.get('training_courses', [])
                        award_data = item.get('awards', [])
                        disciplinary_data = item.get('disciplinary_actions', [])
                        family_data = item.get('family_members', [])
                        evaluation_data = item.get('evaluation', [])

                        # ✅ ดึง instance
                        emp_instance = get_object_or_404(Employee_lcic, emp_id=emp_id)

                        # ✅ ตรวจสอบและจัดการรูปภาพ
                        if 'pic' in request.FILES:
                            pic = request.FILES['pic']
                            if pic.size > 5 * 1024 * 1024:
                                return Response({"error": "Image file too large (max 15MB)."}, status=status.HTTP_400_BAD_REQUEST)
                            # if pic.content_type not in ['image/jpeg', 'image/png']:
                            #     return Response({"error": "Unsupported image format (only JPEG/PNG allowed)."}, status=status.HTTP_400_BAD_REQUEST)
                            employee_data['pic'] = pic
                        elif employee_data.get('pic') in ['', None, 'null', u'null']:
                            if emp_instance.pic:
                                emp_instance.pic.delete(save=False)
                            employee_data['pic'] = None
                        else:
                            employee_data.pop('pic', None)

                        # ✅ อัปเดตข้อมูล employee
                        emp_serializer = EmployeeSerializer(emp_instance, data=employee_data, partial=True)
                        emp_serializer.is_valid(raise_exception=True)
                        emp_serializer.save()

                        # ✅ ฟังก์ชันอัปเดตข้อมูลย่อย
                        def update_related_data(model_class, serializer_class, data_list):
                            existing_objs = {obj.id: obj for obj in model_class.objects.filter(emp_id=emp_id)}
                            sent_ids = []

                            for entry in data_list:
                                entry['emp_id'] = emp_id
                                obj_id = entry.get('id')
                                if obj_id and obj_id in existing_objs:
                                    serializer = serializer_class(existing_objs[obj_id], data=entry, partial=True)
                                else:
                                    serializer = serializer_class(data=entry)
                                serializer.is_valid(raise_exception=True)
                                instance = serializer.save()
                                sent_ids.append(instance.id)

                            model_class.objects.filter(emp_id=emp_id).exclude(id__in=sent_ids).delete()

                        # ✅ เรียกอัปเดตตารางย่อย
                        update_related_data(PersonalInformation, PersonalInformationSerializer, personal_data)
                        update_related_data(Education, EducationSerializer, education_data)
                        update_related_data(SpecializedEducation, SpecializedEducationSerializer, specialized_data)
                        update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, political_data)
                        update_related_data(ForeignLanguage, ForeignLanguageSerializer, language_data)
                        update_related_data(WorkExperience, WorkExperienceSerializer, work_data)
                        update_related_data(TrainingCourse, TrainingCourseSerializer, training_data)
                        update_related_data(Award, AwardSerializer, award_data)
                        update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, disciplinary_data)
                        update_related_data(FamilyMember, FamilyMemberSerializer, family_data)
                        update_related_data(Evaluation, EvaluationSerializer, evaluation_data)

                        # # ✅ อัปเดตการประเมิน
                        # if evaluation_data:
                        #     evaluation_data['emp_id'] = emp_id
                        #     eval_id = evaluation_data.get('id')
                        #     if eval_id:
                        #         eval_instance = get_object_or_404(Evaluation, id=eval_id, emp_id=emp_id)
                        #         eval_serializer = EvaluationSerializer(eval_instance, data=evaluation_data, partial=True)
                        #     else:
                        #         eval_serializer = EvaluationSerializer(data=evaluation_data)
                        #     eval_serializer.is_valid(raise_exception=True)
                        #     eval_serializer.save()

                return Response({"message": "ອັບເດດສຳເລັດ", "emp_id": emp_id}, status=status.HTTP_200_OK)

            except ValidationError as e:
                return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, emp_id):
        try:
            employee_instance = Employee_lcic.objects.get(emp_id=emp_id)
            related_data_map = {
                PersonalInformation: PersonalInformation.objects.filter(emp_id=emp_id),
                FamilyMember: FamilyMember.objects.filter(emp_id=emp_id),
                Education: Education.objects.filter(emp_id=emp_id),
                SpecializedEducation: SpecializedEducation.objects.filter(emp_id=emp_id),
                PoliticalTheoryEducation: PoliticalTheoryEducation.objects.filter(emp_id=emp_id),
                ForeignLanguage: ForeignLanguage.objects.filter(emp_id=emp_id),
                WorkExperience: WorkExperience.objects.filter(emp_id=emp_id),
                TrainingCourse: TrainingCourse.objects.filter(emp_id=emp_id),
                Award: Award.objects.filter(emp_id=emp_id),
                DisciplinaryAction: DisciplinaryAction.objects.filter(emp_id=emp_id),
                Evaluation: Evaluation.objects.filter(emp_id=emp_id)
            }

            for model, queryset in related_data_map.items():
                queryset.delete()

            employee_instance.delete()

            return Response({
                "message": "ລົບສຳເລັດ",
                "emp_id": emp_id
            }, status=status.HTTP_204_NO_CONTENT)

        except Employee_lcic.DoesNotExist:
            return Response({"error": "ພົບບໍ່ຫາພະນັກງານທີ່ມີ emp_id ນີ້"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in delete method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    #             # ລຶບທຸກຕາຕະລາງທີ່ກ່ຽວຂ້ອງ       
    # def delete(self, request):
    #     try:
    #         with transaction.atomic():
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
    #             Employee_lcic.objects.all().delete()

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


class DocumentFormatSearchView(APIView):
    def get(self, request):
        department_name = request.query_params.get('department')
        department_id = request.query_params.get('department_id')
        documents = Document_format.objects.all()
        # Apply filters according to actual field names
        if department_name:
            documents = documents.filter(Department__name__icontains=department_name)
        if department_id:
            documents = documents.filter(Department_id=department_id)
        if not documents.exists():
            return Response(
                {"message": "No documents found matching your search query."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DocumentFormatSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AutoUpdateStatusDocAPIView(APIView):
    def post(self, request, format=None):
        today = timezone.now().date()
        docs = document_general.objects.filter(status_doc='1').exclude(en_date__isnull=True)
        expired_docs = docs.filter(en_date__lte=today)
        updated_count = expired_docs.update(status_doc='0')
        serializer = document_general_Serializer(expired_docs, many=True)
        return Response({
            "message": f"Updated {updated_count} documents (status 1 ➡️ 0)",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



from .serializers import User_emp_Serializer
class user_empView(APIView):
    def get(self, request, us_id=None, username=None):
        try:
            if us_id:
                user = SystemUser.objects.get(us_id=us_id)
            else:
                users = SystemUser.objects.all()
                serializer = User_emp_Serializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer = User_emp_Serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SystemUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class AssetTypeView(APIView):

#     def get(self, request, ast_id=None):
#         if ast_id:
#             try:
#                 asset = Asset_type.objects.get(ast_id=ast_id)
#                 serializer = Asset_typeSerializer(asset)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Asset_type.DoesNotExist:
#                 return Response({"error": "Asset_type not found"}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             assets = Asset_type.objects.all()
#             serializer = Asset_typeSerializer(assets, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = Asset_typeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, ast_id):
#         try:
#             asset = Asset_type.objects.get(ast_id=ast_id)
#         except Asset_type.DoesNotExist:
#             return Response(
#                 {"error": f"Asset_type with ID {ast_id} not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = Asset_typeSerializer(asset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, ast_id):
#         try:
#             asset = Asset_type.objects.get(ast_id=ast_id)
#             asset.delete()
#             return Response(
#                 {"message": f"Asset_type with ID {ast_id} deleted successfully."},
#                 status=status.HTTP_200_OK
#             )
#         except Asset_type.DoesNotExist:
#             return Response(
#                 {"error": f"Asset_type with ID {ast_id} not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )


# class CategoryView(APIView):  
#     def get(self, request, cat_id=None):
#         if cat_id:
#             try:
#                 asset = Category.objects.get(cat_id=cat_id)
#                 serializer = categorySerializer(asset)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Category.DoesNotExist:
#                 return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             assets = Category.objects.all()
#             serializer = categorySerializer(assets, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = categorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, cat_id):
#         try:
#             asset = Category.objects.get(cat_id=cat_id)
#         except Category.DoesNotExist:
#             return Response(
#                 {"error": f"Category with ID {cat_id} not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = categorySerializer(asset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, cat_id):
#         try:
#             asset = Category.objects.get(cat_id=cat_id)
#             asset.delete()
#             return Response(
#                 {"message": f"Category with ID {cat_id} deleted successfully."},
#                 status=status.HTTP_200_OK
#             )
#         except Category.DoesNotExist:
#             return Response(
#                 {"error": f"Category with ID {cat_id} not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )


# class AssetView(APIView):
#     def get(self, request, as_id=None):
#         if as_id:
#             try:
#                 asset = Asset.objects.get(as_id=as_id)
#                 serializer = AssetSerializer(asset)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Asset.DoesNotExist:
#                 return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             assets = Asset.objects.all()
#             serializer = AssetSerializer(assets, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = AssetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, as_id):
#         try:
#             asset = Asset.objects.get(as_id=as_id)
#         except Asset.DoesNotExist:
#             return Response({"error": f"Asset with ID {as_id} not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = AssetSerializer(asset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, as_id):
#         try:
#             asset = Asset.objects.get(as_id=as_id)
#             asset.delete()
#             return Response({"message": f"Asset with ID {as_id} deleted successfully."}, status=status.HTTP_200_OK)
#         except Asset.DoesNotExist:
#             return Response({"error": f"Asset with ID {as_id} not found."}, status=status.HTTP_404_NOT_FOUND)

# class CategorySearchView(APIView):
#     def get(self, request):
#         cat_num = request.query_params.get("cat_num")
#         cat_name = request.query_params.get("cat_name")
#         ast_id = request.query_params.get("ast_id")

#         categories = Category.objects.all()

#         if cat_num:
#             categories = categories.filter(cat_num__icontains=cat_num)
#         if cat_name:
#             categories = categories.filter(cat_name__icontains=cat_name)
#         if ast_id:
#             categories = categories.filter(ast_id=ast_id)

#         if categories.exists():
#             serializer = categorySerializer(categories, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(
#             {"message": "No categories found matching your search query."},
#             status=status.HTTP_404_NOT_FOUND
#         )