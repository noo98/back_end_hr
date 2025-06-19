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
from django.http import JsonResponse, Http404
from .models import Position, Salary, SubsidyPosition, FuelSubsidy, MobilePhoneSubsidy, OvertimeWork,monthly_payment,col_policy,income_tax
from .models import SystemUser,Fuel_payment
from .serializers import SystemUserSerializer,DocumentFormatSerializer,DocumentFormat_Serializer,fuel_paymentSerializer
from .serializers import activitySerializer,income_taxSerializer
from .models import Department,Document_format,document_general,job_mobility
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
from .serializers import (PersonalInformationSerializer, EducationSerializer, SpecializedEducationSerializer, AwardSerializer,col_policySerializer,
PoliticalTheoryEducationSerializer, ForeignLanguageSerializer, WorkExperienceSerializer, TrainingCourseSerializer,DisciplinaryActionSerializer,
FamilyMemberSerializer, EvaluationSerializer)
from .models import Document_Status
# from .serializers import Asset_typeSerializer,AssetSerializer
# from .models import Category
# from .serializers import categorySerializer
from .models import Overtime_history,colpolicy_history,fuel_payment_history
from .serializers import (get_Overtime_historyserializer,post_Overtime_historyserializer,post_colpolicy_historyserializer,get_colpolicy_historyserializer,get_fuel_payment_historyserializer,
post_fuel_payment_historyserializer)

import logging
from django.db import transaction 
from rest_framework.generics import get_object_or_404
from typing import Optional
logger = logging.getLogger(__name__)
# from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets
from .models import Position
from .serializers import PositionSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from decimal import Decimal   
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .models import FuelSubsidy
from .serializers import FuelSubsidySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SystemSetting
from .serializers import SystemSettingSerializer,get_OvertimeWorkSerializer



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
        Document = document_lcic.objects.all().order_by('-doc_id')
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

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
class UserView(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)

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
        # ສະແດງຂໍ້ມູນທັງໝົດ
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
        user = get_object_or_404(SystemUser, us_id=us_id)
        serializer = SystemUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle password hashing if 'password' is present
            password = request.data.get("password")
            if password:
                user.password = make_password(password)
                # Save other validated fields
                serializer.validated_data.pop('password', None)

            serializer.save()
            return Response({
                "message": "ແກ້ໄຂ ສຳເລັດ",
                "user": SystemUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, us_id):
        user = get_object_or_404(SystemUser, us_id=us_id)
        serializer = SystemUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle password hashing if 'password' is present
            password = request.data.get("password")
            if password:
                user.password = make_password(password)
                serializer.validated_data.pop('password', None)

            serializer.save()
            return Response({
                "message": "ແກ້ໄຂ ສຳເລັດ",
                "user": SystemUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class Employee_lcicView(APIView):
    # authentication_classes = [CustomJWTAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def get(self, request, emp_id: int = None):
        if emp_id:
            employee_instances = Employee_lcic.objects.filter(emp_id=emp_id)
        else:
            employee_instances = Employee_lcic.objects.all().order_by('pos_id')
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
        for item in dataset:
            item['emp_id'] = emp_id
            serializer = serializer_class(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
    
    def post(self, request):
        try:
            # ✅ รองรับทั้ง JSON และ FormData
            if request.content_type.startswith('multipart/form-data'):
                raw_data = request.POST.get('data', '{}')
                try:
                    json_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    return Response({"error": "Invalid JSON format."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                json_data = request.data

            pic_file = request.FILES.get('pic')

            # ✅ ตรวจสอบ Employee_lcic
            employee_data_list = json_data.get('Employee_lcic')
            if not isinstance(employee_data_list, list) or not employee_data_list:
                return Response({"error": "Invalid type or missing 'Employee_lcic' data."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                employee_data = employee_data_list[0]
                if pic_file:
                    employee_data['pic'] = pic_file

                # ✅ บันทึก employee
                employee_serializer = EmployeeSerializer(data=employee_data)
                employee_serializer.is_valid(raise_exception=True)
                employee_instance = employee_serializer.save()

                # ✅ จัดการข้อมูลที่เกี่ยวข้อง
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

                # ✅ บันทึกการประเมิน
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

    def patch(self, request, emp_id: int):
            logger.debug(f"Received PATCH request for emp_id: {emp_id}")

            try:
                # รองรับทั้ง JSON และ FormData
                if request.content_type.startswith('multipart/form-data'):
                    raw_data = request.POST.get('data', '{}')
                    try:
                        dataset = json.loads(raw_data)
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON format in 'data' field")
                        return Response({"error": "Invalid JSON format in 'data' field."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    dataset = request.data

                # ถ้า dataset เป็น dict เดี่ยว ให้แปลงเป็น list
                if isinstance(dataset, dict):
                    dataset = [dataset]
                elif not isinstance(dataset, list):
                    logger.error("Dataset is neither a dict nor a list")
                    return Response({"error": "Expected a list or a single data object."}, status=status.HTTP_400_BAD_REQUEST)

                with transaction.atomic():
                    # หา employee object
                    emp_instance = get_object_or_404(Employee_lcic, emp_id=emp_id)

                    for item in dataset:
                        # ดึงข้อมูล employee หลัก
                        employee_json = item.get('employee', {})

                        # แปลง employee_json ถ้าเป็น string
                        if isinstance(employee_json, str):
                            try:
                                employee_data = json.loads(employee_json)
                            except json.JSONDecodeError:
                                logger.error("Invalid JSON format in 'employee' data")
                                return Response({"error": "Invalid JSON format in 'employee' data."}, status=status.HTTP_400_BAD_REQUEST)
                        elif isinstance(employee_json, dict):
                            employee_data = employee_json
                        else:
                            employee_data = {}

                        # อัปเดตรูป (pic)
                        pic_updated = False
                        if 'pic' in request.FILES:
                            pic = request.FILES['pic']
                            if pic.size > 5 * 1024 * 1024:  # จำกัดขนาดไฟล์
                                logger.error("Image file too large")
                                return Response({"error": "Image file too large (max 5MB)."}, status=status.HTTP_400_BAD_REQUEST)
                            emp_instance.pic.save(pic.name, pic)
                            pic_updated = True
                            logger.info(f"Saved new image: {pic.name}")

                        # เซฟข้อมูล employee หลัก
                        if employee_data:
                            emp_serializer = EmployeeSerializer(emp_instance, data=employee_data, partial=True)
                            emp_serializer.is_valid(raise_exception=True)
                            emp_serializer.save()
                            logger.info(f"Updated employee data for emp_id: {emp_id}")

                        # ดึงข้อมูลตารางย่อย
                        related_data = {
                            'personal_information': item.get('personal_information', []),
                            'education': item.get('education', []),
                            'specialized_education': item.get('specialized_education', []),
                            'political_theory_education': item.get('political_theory_education', []),
                            'foreign_languages': item.get('foreign_languages', []),
                            'work_experiences': item.get('work_experiences', []),
                            'training_courses': item.get('training_courses', []),
                            'awards': item.get('awards', []),
                            'disciplinary_actions': item.get('disciplinary_actions', []),
                            'family_members': item.get('family_members', []),
                            'evaluation': item.get('evaluation', [])
                        }
                        logger.debug(f"Related data: {related_data}")

                        # ฟังก์ชันอัปเดตข้อมูลย่อย
                        def update_related_data(model_class, serializer_class, data_list, model_name):
                            if not data_list or not isinstance(data_list, list):
                                logger.debug(f"No data to update for {model_name}")
                                return
                            try:
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
                                    logger.debug(f"Saved {model_name} instance: {instance.id}")

                                # ลบ record ที่ไม่ได้ส่งมา
                                deleted_count = model_class.objects.filter(emp_id=emp_id).exclude(id__in=sent_ids).delete()[0]
                                logger.debug(f"Deleted {deleted_count} old {model_name} records")
                            except Exception as e:
                                logger.error(f"Error updating {model_name}: {str(e)}")
                                raise

                        # อัปเดตข้อมูลย่อย
                        update_related_data(PersonalInformation, PersonalInformationSerializer, related_data['personal_information'], 'PersonalInformation')
                        update_related_data(Education, EducationSerializer, related_data['education'], 'Education')
                        update_related_data(SpecializedEducation, SpecializedEducationSerializer, related_data['specialized_education'], 'SpecializedEducation')
                        update_related_data(PoliticalTheoryEducation, PoliticalTheoryEducationSerializer, related_data['political_theory_education'], 'PoliticalTheoryEducation')
                        update_related_data(ForeignLanguage, ForeignLanguageSerializer, related_data['foreign_languages'], 'ForeignLanguage')
                        update_related_data(WorkExperience, WorkExperienceSerializer, related_data['work_experiences'], 'WorkExperience')
                        update_related_data(TrainingCourse, TrainingCourseSerializer, related_data['training_courses'], 'TrainingCourse')
                        update_related_data(Award, AwardSerializer, related_data['awards'], 'Award')
                        update_related_data(DisciplinaryAction, DisciplinaryActionSerializer, related_data['disciplinary_actions'], 'DisciplinaryAction')
                        update_related_data(FamilyMember, FamilyMemberSerializer, related_data['family_members'], 'FamilyMember')
                        update_related_data(Evaluation, EvaluationSerializer, related_data['evaluation'], 'Evaluation')

                    return Response(
                        {"message": "ອັບເດດ ສຳເລັດ", "emp_id": emp_id},
                        status=status.HTTP_200_OK
                    )

            except ValidationError as e:
                logger.error(f"Validation error: {e.detail}")
                return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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

                        # ✅ อัปเดตการประเมิน
                        if evaluation_data:
                            evaluation_data['emp_id'] = emp_id
                            eval_id = evaluation_data.get('id')
                            if eval_id:
                                eval_instance = get_object_or_404(Evaluation, id=eval_id, emp_id=emp_id)
                                eval_serializer = EvaluationSerializer(eval_instance, data=evaluation_data, partial=True)
                            else:
                                eval_serializer = EvaluationSerializer(data=evaluation_data)
                            eval_serializer.is_valid(raise_exception=True)
                            eval_serializer.save()

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
        expired_docs = docs.filter(en_date__gt=today)
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
#             return Response(serializer.data, status=status.HTTP_200_OK)ຫຫ

#         return Response(
#             {"message": "No categories found matching your search query."},
#             status=status.HTTP_404_NOT_FOUND
#         )


from rest_framework import viewsets
from .models import (
    Position, Salary, SubsidyPosition, SubsidyYear,
    FuelSubsidy, AnnualPerformanceGrant, SpecialDayGrant,
    MobilePhoneSubsidy, OvertimeWork
)
from .serializers import (
    PositionSerializer, SalarySerializer, SubsidyPositionSerializer,get_FuelSubsidySerializer,
    SubsidyYearSerializer, FuelSubsidySerializer, AnnualPerformanceGrantSerializer, monthly_paymentSerializer1,
    SpecialDayGrantSerializer, MobilePhoneSubsidySerializer, OvertimeWorkSerializer ##,MonthlyPayment1Serializer
)

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('pos_id')
    serializer_class = PositionSerializer

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all().order_by('pos_id')
    serializer_class = SalarySerializer

class SubsidyPositionViewSet(viewsets.ModelViewSet):
    queryset = SubsidyPosition.objects.all().order_by('pos_id')
    serializer_class = SubsidyPositionSerializer

class SubsidyYearViewSet(viewsets.ModelViewSet):
    queryset = SubsidyYear.objects.all().order_by('sy_id')
    serializer_class = SubsidyYearSerializer

class AnnualPerformanceGrantViewSet(viewsets.ModelViewSet):
    queryset = AnnualPerformanceGrant.objects.all()
    serializer_class = AnnualPerformanceGrantSerializer

class SpecialDayGrantViewSet(viewsets.ModelViewSet):
    queryset = SpecialDayGrant.objects.all()
    serializer_class = SpecialDayGrantSerializer

class MobilePhoneSubsidyViewSet(viewsets.ModelViewSet):
    queryset = MobilePhoneSubsidy.objects.all()
    serializer_class = MobilePhoneSubsidySerializer

class income_taxViewSet(viewsets.ModelViewSet):
    queryset = income_tax.objects.all()
    serializer_class = income_taxSerializer

class ovtimeWorkView(APIView):
    def get(self, request, ot_id=None):
        try:
            if ot_id:
                overtime = OvertimeWork.objects.get(ot_id=ot_id)
                serializer = get_OvertimeWorkSerializer(overtime)
            else:
                overtime = OvertimeWork.objects.all().order_by('emp_id__pos_id_id')
                serializer = get_OvertimeWorkSerializer(overtime, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OvertimeWork.DoesNotExist:
            return Response({"error": "Overtime work not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = OvertimeWorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, ot_id=None):
        try:
            overtime = OvertimeWork.objects.get(ot_id=ot_id)
            serializer = get_OvertimeWorkSerializer(overtime, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OvertimeWork.DoesNotExist:
            return Response({"error": "Overtime work not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, ot_id=None):
        try:
            overtime = OvertimeWork.objects.get(ot_id=ot_id)
            serializer = get_OvertimeWorkSerializer(overtime, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OvertimeWork.DoesNotExist:
            return Response({"error": "Overtime work not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ot_id=None):
        try:
            overtime = OvertimeWork.objects.get(ot_id=ot_id)
            overtime.delete()
            return Response({"message": "Overtime work deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except OvertimeWork.DoesNotExist:
            return Response({"error": "Overtime work not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FuelSubsidyView(APIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    def get(self, request, fs_id=None):
        try:
            if fs_id:
                fuel_subsidy = FuelSubsidy.objects.get(fs_id=fs_id)
                serializer = get_FuelSubsidySerializer(fuel_subsidy)
            else:
                fuel_subsidies = FuelSubsidy.objects.all().order_by('pos_id')
                serializer = get_FuelSubsidySerializer(fuel_subsidies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FuelSubsidy.DoesNotExist:
            return Response({"error": "Fuel subsidy not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = FuelSubsidySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Fuel subsidy created successfully", "fuel_subsidy": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            setting = SystemSetting.objects.get(key='fuel_price')
        except SystemSetting.DoesNotExist:
            return Response({"error": "Setting not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SystemSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # ✅ ເຊັກກ່ອນວ່າ 'value' ຢູ່ໃນ validated_data ຫຼືບໍ່
            new_value = serializer.validated_data.get('value')
            if new_value is None:
                return Response({"error": "Missing 'value' in request."}, status=400)

            # ອັບເດດ total_fuel
            from .models import FuelSubsidy
            new_price = Decimal(new_value)
            for fs in FuelSubsidy.objects.all():
                if fs.fuel_subsidy is not None:
                    fs.total_fuel = Decimal(fs.fuel_subsidy) * new_price
                    fs.save(update_fields=['total_fuel'])

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, fs_id):
        fuel_subsidy = get_object_or_404(FuelSubsidy, fs_id=fs_id)
        serializer = FuelSubsidySerializer(fuel_subsidy, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "ແກ້ໄຂສຳເລັດ",
                "fuel_subsidy": FuelSubsidySerializer(fuel_subsidy).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fs_id):
        try:
            fuel_subsidy = FuelSubsidy.objects.get(fs_id=fs_id)
            fuel_subsidy.delete()
            return Response(
                {"message": f"Fuel subsidy with ID {fs_id} deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except FuelSubsidy.DoesNotExist:
            return Response(
                {"error": "Fuel subsidy not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class Fuel_pamentViewSet(viewsets.ModelViewSet):
    queryset = Fuel_payment.objects.all().order_by('emp_id__pos_id_id')
    serializer_class = fuel_paymentSerializer

def get_position_details(request, emp_id):

    try:
        employee = Employee_lcic.objects.get(emp_id=emp_id)
        pos = employee.pos_id
    except Employee_lcic.DoesNotExist:
        raise Http404("Employee not found")

    # ດຶງຂໍ້ມູນອື່ນໆທີ່ກ່ຽວຂ້ອງກັບ pos_id
    salary = Salary.objects.filter(pos_id=pos).first()
    subsidy_position = SubsidyPosition.objects.filter(pos_id=pos).first()
    fuel_subsidy = FuelSubsidy.objects.filter(pos_id=pos).first()

    return JsonResponse({
        'emp_id': employee.emp_id,
        'lao_name': employee.lao_name,
        'eng_name': employee.eng_name,
        'position': pos.name if pos else None,
        # Salary
        'sal_id': salary.sal_id if salary else None,
        'SalaryGrade': str(salary.SalaryGrade) if salary and salary.SalaryGrade else None,
        # SubsidyPosition
        'sp_id': subsidy_position.sp_id if subsidy_position else None,
        'grant': str(subsidy_position.grant) if subsidy_position and subsidy_position.grant else None,
        # FuelSubsidy
        'fs_id': fuel_subsidy.fs_id if fuel_subsidy else None,
        'update_date': str(fuel_subsidy.update_date) if fuel_subsidy and fuel_subsidy.update_date else None,
        'fuel_subsidy': str(fuel_subsidy.fuel_subsidy) if fuel_subsidy and fuel_subsidy.fuel_subsidy else None,
        'fuel_price_id': fuel_subsidy.fuel_price.id if fuel_subsidy and fuel_subsidy.fuel_price else None,
        'total_fuel': str(fuel_subsidy.total_fuel) if fuel_subsidy and fuel_subsidy.total_fuel else None,
    })

class monthly_paymentViewSet(viewsets.ModelViewSet):
    queryset = monthly_payment.objects.all()
    serializer_class = monthly_paymentSerializer1

class col_policyViewSet(viewsets.ModelViewSet):
    queryset = col_policy.objects.all()
    serializer_class = col_policySerializer
    
class UpdateAllJobMobilityAPIView(APIView):
    def put(self, request):
        data = request.data
        update_fields = {}

        if 'pos_id' in data:
            update_fields['pos_id'] = data['pos_id']
        if 'amount_per_day' in data:
            update_fields['amount_per_day'] = data['amount_per_day']
        if 'jm_policy' in data:
            update_fields['jm_policy'] = data['jm_policy']
        if 'number_of_days' in data:
            update_fields['number_of_days'] = data['number_of_days']

        update_fields['date'] = timezone.now().date()

        try:
            job_mobility.objects.all().update(**update_fields)
            return Response({"message": "Updated all job mobility records successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OvertimeWork
@api_view(['POST'])
def reset_all_overtimes(request):
    overtimes = OvertimeWork.objects.all()
    
    for ot in overtimes:
        ot.csd_evening = 0.00
        ot.csd_night = 0.00
        ot.hd_mor_after = 0.00
        ot.hd_evening = 0.00
        ot.hd_night = 0.00
        ot.total_ot = 0
        ot.save()
    
    return Response({"message": "All OT records reset successfully."}, status=status.HTTP_200_OK)

class Overtime_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                overtime_history = Overtime_history.objects.filter(emp_id=emp_id)
                serializer = get_Overtime_historyserializer(overtime_history, many=True)
            else:
                overtime_history = Overtime_history.objects.all()
                serializer = get_Overtime_historyserializer(overtime_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            try:
                # ແປວັນທີໃຫ້ເປັນ datetime object
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            # ດຶງຂໍ້ມູນຂອງ emp_id ຈາກຖານຂໍ້ມູນ
            existing_records = Overtime_history.objects.filter(emp_id=item['emp_id'])

            for record in existing_records:
                try:
                    record_date = datetime.strptime(record.date, '%Y-%m-%d')  # ແປຈາກ string ໃນ DB
                    if record_date.year == target_year and record_date.month == target_month:
                        duplicates.append({
                            'emp_id': item['emp_id'],
                            'month': target_month,
                            'year': target_year
                        })
                        break  # ບໍ່ຈໍາເປັນກວດຕື່ມຖ້າຊ້ຳແລ້ວ
                except ValueError:
                    continue  # ຂໍ້ມູນວັນທີບໍ່ຖືກ ຂ້າມໄປ

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ',
                # 'duplicates': duplicates
            }, status=status.HTTP_400_BAD_REQUEST)

        # validate ແລະ save
        serializer = post_Overtime_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class colpolicy_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                colpolicy= colpolicy_history.objects.filter(emp_id=emp_id)
                serializer = get_colpolicy_historyserializer(colpolicy, many=True)
            else:
                colpolicy= colpolicy_history.objects.all()
                serializer = get_colpolicy_historyserializer(colpolicy, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            try:
                # ແປວັນທີທີ່ສົ່ງມາໃຫ້ເປັນ datetime
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            # ດຶງທັງໝົດຂອງ emp_id ຈາກ DB
            records = colpolicy_history.objects.filter(emp_id=item['emp_id'])

            for record in records:
                try:
                    record_date = datetime.strptime(record.date, '%Y-%m-%d')
                    if record_date.month == target_month and record_date.year == target_year:
                        duplicates.append({
                            'emp_id': item['emp_id'],
                            'month': target_month,
                            'year': target_year
                        })
                        break  # ຂ້າມກວດຕໍ່ຖ້າພົບຊ້ຳ
                except:
                    continue  # ຂໍ້ມູນໃນ DB ບໍ່ຖືກຮູບແບບ

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ (ຕາມເດືອນ-ປີ)',
                # 'duplicates': duplicates
            }, status=status.HTTP_400_BAD_REQUEST)

        # validate ແລະ save
        serializer = post_colpolicy_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class fuel_payment_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                fuel_history = fuel_payment_history.objects.filter(emp_id=emp_id)
                serializer = get_fuel_payment_historyserializer(fuel_history, many=True)
            else:
                fuel_history = fuel_payment_history.objects.all()
                serializer = get_fuel_payment_historyserializer(fuel_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = fuel_payment_history.objects.filter(emp_id=item['emp_id'])

            for record in existing_records:
                try:
                    record_date = datetime.strptime(record.date, '%Y-%m-%d')
                    if record_date.month == target_month and record_date.year == target_year:
                        duplicates.append({
                            'emp_id': item['emp_id'],
                            'month': target_month,
                            'year': target_year
                        })
                        break
                except:
                    continue

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
                # 'duplicates': duplicates
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_fuel_payment_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)