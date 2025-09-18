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
from .models import SystemUser,Fuel_payment,Saving_cooperative,welfare,evaluation_score
from .serializers import SystemUserSerializer,DocumentFormatSerializer,DocumentFormat_Serializer,fuel_paymentSerializer,Specialday_empserialiser,welfareSerializer,evaluation_scoreSerializer
from .serializers import activitySerializer,income_taxSerializer,Saving_cooperativeSerializer,monthly_paymentSerializer,Specialday_PositionSerializer,evaluation_score_empSerializer
from .models import Department,Document_format,document_general,job_mobility,SpecialDay_Position,evaluation_score_emp
from .serializers import DepartmentSerializer,document_lcicSerializer,DocumentLcic_AddSerializer,document_general_Serializer,StatusSerializer,SidebarSerializer
from .models import uniform
from .serializers import uniformSerializer,get_uniformSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OvertimeWork
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
from .models import Overtime_history,colpolicy_history,fuel_payment_history,monthly_payment_history,MobilePhoneSubsidy_emp_History
from .serializers import (get_Overtime_historyserializer,post_Overtime_historyserializer,post_colpolicy_historyserializer,get_colpolicy_historyserializer,get_fuel_payment_historyserializer,
post_fuel_payment_historyserializer,get_monthly_payment_historyserializer,post_monthly_payment_historyserializer,get_uniform_historyserializer,post_uniform_historyserializer,evaluation_score_emp_history,
get_evaluation_score_emp_historyserializer,post_evaluation_score_emp_historyserializer,post_MobilePhoneSubsidy_emp_Historyserializer,get_MobilePhoneSubsidy_emp_Historyserializer)
from rest_framework import viewsets
from .models import (
    Position, Salary, SubsidyPosition, SubsidyYear,
    FuelSubsidy, AnnualPerformanceGrant, SpecialDayGrant,
    MobilePhoneSubsidy, OvertimeWork,uniform_history
)
from .serializers import (
    PositionSerializer, SalarySerializer, SubsidyPositionSerializer,get_FuelSubsidySerializer,
    SubsidyYearSerializer, FuelSubsidySerializer, AnnualPerformanceGrantSerializer,
    SpecialDayGrantSerializer, MobilePhoneSubsidySerializer, OvertimeWorkSerializer ##,MonthlyPayment1Serializer
)
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
from django.db import IntegrityError
from .models import Document_Status
from .serializers import DocStatusSerializer
from .serializers import job_mobilitySerializer
from .serializers import health_allowanceSerializer
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from datetime import date as dt_date
from .models import specialday_emp_history
from .serializers import (
    post_specialday_emp_historyserializer,
    get_specialday_emp_historyserializer
)
from .models import saving_cooperative_history
from .serializers import post_saving_cooperative_historyserializer ,get_saving_cooperative_historyserializer
from rest_framework import generics
from .models import Role, RolePermission, Menu, MainMenu
from .serializers import RoleSerializer, RolePermissionSerializer, MenuSerializer, MainMenuSerializer, UserMenuSerializer

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
            if document.file:  
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
                users = SystemUser.objects.all().order_by('Employee__pos_id__pos_id')
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
            data = request.data.copy()  # copy เพื่อแก้ไขได้
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
        data = request.data.copy()

        # Remove username from update data to prevent modification
        if 'username' in data:
            data.pop('username')

        serializer = SystemUserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            password = data.get("password")
            if password:
                user.password = make_password(password)
                # Remove password so serializer.save() doesn't overwrite
                serializer.validated_data.pop('password', None)

            serializer.save()
            return Response({
                "message": "ແກ້ໄຂ ສຳເລັດ",
                "user": SystemUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, us_id):
        user = get_object_or_404(SystemUser, us_id=us_id)
        data = request.data.copy()

        # Remove username from update data to prevent modification
        if 'username' in data:
            data.pop('username')

        serializer = SystemUserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            password = data.get("password")
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
        
# Role CRUD
class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# RolePermission CRUD
class RolePermissionListCreate(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

class RolePermissionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

# Menu CRUD
class MenuListCreate(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

# MainMenu CRUD
class MainMenuListCreate(generics.ListCreateAPIView):
    queryset = MainMenu.objects.all()
    serializer_class = MainMenuSerializer

class MainMenuRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MainMenu.objects.all()
    serializer_class = MainMenuSerializer

# User Menu View
class UserMenuDetail(generics.RetrieveAPIView):
    serializer_class = UserMenuSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return SystemUser.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            # ດຶງ user ແລະ role_id
            user = SystemUser.objects.get(pk=user_id)
            role_id = user.role_id_id  # ດຶງ role_id ຈາກ user

            # ດຶງ menu_ids ທີ່ກ່ຽວຂ້ອງກັບ role_id ຜ່ານ RolePermission
            role_permissions = RolePermission.objects.filter(role_id=role_id).values('menu_id')
            menu_ids = [rp['menu_id'] for rp in role_permissions]

            # ດຶງ menus ທີ່ກ່ຽວຂ້ອງກັບ menu_ids
            menus = Menu.objects.filter(menu_id__in=menu_ids).select_related('main_id')

            # ສ້າງ dictionary ເພື່ອກຸ່ມ menus ຕາມ main_id
            main_menu_dict = {}
            for menu in menus:
                main_id = menu.main_id.main_id
                if main_id not in main_menu_dict:
                    main_menu_dict[main_id] = {
                        'main_id': main_id,
                        'main_name': menu.main_id.main_name,
                        'icon': menu.main_id.icon,
                        'children': []
                    }
                main_menu_dict[main_id]['children'].append({
                    'menu_id': menu.menu_id,
                    'menu_name': menu.menu_name,
                    'url': menu.url,
                    'icon': menu.icon
                })

            # ແປງ dictionary ເປັນລາຍການ
            filtered_menus = list(main_menu_dict.values())

            # ຈັດລຽງ children ຕາມ menu_id (ຖ້າຕ້ອງການ)
            for main_menu in filtered_menus:
                main_menu['children'] = sorted(main_menu['children'], key=lambda x: x['menu_id'])

            logger.info(f"Retrieved menus for user_id: {user_id}, role_id: {role_id}")
            return Response(filtered_menus, status=status.HTTP_200_OK)

        except SystemUser.DoesNotExist:
            logger.error(f"User not found: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error for user_id {user_id}: {str(e)}")
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        documents = document_lcic.objects.all().order_by('-doc_id')

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
        documents = document_general.objects.all().order_by('-docg_id')  # ສະແດງຈາກ ID ສູງຫາຕ່ຳ

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
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
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


class docstatus(APIView):
    def get(self, request):
        documents = Document_Status.objects.all()
        serializer = DocStatusSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        doc_id = request.data.get("doc_id")
        us_id = request.data.get("us_id")

        if not doc_id or not us_id:
            return Response({"success": False, "error": "doc_id ແລະ us_id ຕ້ອງມີຄ່າ"}, status=400)

        try:
            doc_status, created = Document_Status.objects.update_or_create(
                doc_id_id=doc_id,
                us_id_id=us_id,
                defaults={"Doc_status": "viewed", "timestamp": timezone.now()}
            )
            serializer = DocStatusSerializer(doc_status)
            return Response({
                "success": True,
                "message": "Created" if created else "Updated",
                **serializer.data
            }, status=201 if created else 200)

        except IntegrityError:
            return Response({"success": False, "error": "ຂໍ້ມູນຜິດພາດ"}, status=400)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)
        
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

class SpecialDayViewSet(viewsets.ModelViewSet):
    queryset = SpecialDayGrant.objects.all().order_by('sdg_id')
    serializer_class = SpecialDayGrantSerializer
class SpecialDayGrantViewSet(viewsets.ModelViewSet):
    queryset = SpecialDay_Position.objects.all().order_by('special_day','pos_id')
    serializer_class = Specialday_PositionSerializer
class SpecialDay_empViewSet(viewsets.ModelViewSet):
    queryset = Employee_lcic.objects.all().order_by('pos_id')
    serializer_class = Specialday_empserialiser
class SpecialDayPositionFilterAPIView(APIView):
    def get(self, request):
        sdg_id = request.query_params.get('sdg_id')
        special_day = request.query_params.get('special_day')  # occasion_name
        pos_name = request.query_params.get('pos_name')
        pos_id = request.query_params.get('pos_id')
        min_grant = request.query_params.get('min_grant')

        queryset = SpecialDay_Position.objects.select_related('special_day', 'pos_id').all().order_by('special_day', 'pos_id')

        if sdg_id:
            queryset = queryset.filter(special_day__sdg_id=sdg_id)

        if special_day:
            queryset = queryset.filter(special_day__occasion_name__icontains=special_day)

        if pos_name:
            queryset = queryset.filter(pos_id__name__icontains=pos_name)

        if pos_id:
            queryset = queryset.filter(pos_id=pos_id)

        if min_grant:
            try:
                min_grant = float(min_grant)
                queryset = queryset.filter(grant__gte=min_grant)
            except ValueError:
                return Response({'error': 'Invalid grant value'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = Specialday_PositionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MobilePhoneSubsidyViewSet(viewsets.ModelViewSet):
    queryset = MobilePhoneSubsidy.objects.all().order_by('pos_id')
    serializer_class = MobilePhoneSubsidySerializer
class MobilePhoneSubsidy_empAPIView(APIView):
    def get(self, request, emp_id=None):
        if emp_id:
            try:
                emp = Employee_lcic.objects.select_related('pos_id').get(emp_id=emp_id)
            except Employee_lcic.DoesNotExist:
                return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

            subsidy = MobilePhoneSubsidy.objects.filter(pos_id=emp.pos_id).first()

            if not subsidy:
                return Response({"detail": "No mobile phone subsidy found for this position."}, status=status.HTTP_204_NO_CONTENT)

            result = {
                "date": date.today(),
                "emp_id": emp.emp_id,
                "lao_name": emp.lao_name,
                "pos_id": emp.pos_id.pos_id,
                "pos_name": emp.pos_id.name,
                "mb_id": subsidy.mb_id,
                "grant": subsidy.grant
            }
            return Response(result, status=status.HTTP_200_OK)

        # ຖ້າບໍ່ສົ່ງ emp_id → ໂຊພະນັກງານທັງໝົດທີ່ມີ subsidy ຂອງ pos_id
        employees = Employee_lcic.objects.select_related('pos_id').all().order_by('pos_id')
        data = []

        for emp in employees:
            subsidy = MobilePhoneSubsidy.objects.filter(pos_id=emp.pos_id).first()
            if subsidy:
                data.append({
                    "date": date.today(),
                    "emp_id": emp.emp_id,
                    "lao_name": emp.lao_name,
                    "pos_id": emp.pos_id.pos_id,
                    "pos_name": emp.pos_id.name,
                    "mb_id": subsidy.mb_id,
                    "grant": subsidy.grant
                })

        return Response(data, status=status.HTTP_200_OK)
    
class income_taxViewSet(viewsets.ModelViewSet):
    queryset = income_tax.objects.all().order_by('tax_id')
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
                "fuel_subsidy": get_FuelSubsidySerializer(fuel_subsidy).data
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

class Saving_cooperativeViewSet(viewsets.ModelViewSet):
    queryset = Saving_cooperative.objects.all().order_by('emp_id')
    serializer_class = Saving_cooperativeSerializer

class health_allowanceViewSet(viewsets.ModelViewSet):
    queryset = monthly_payment.objects.all().order_by('emp_id')
    serializer_class = health_allowanceSerializer

class col_policyViewSet(viewsets.ModelViewSet):
    queryset = col_policy.objects.all()
    serializer_class = col_policySerializer

class job_mobilityViewSet(viewsets.ModelViewSet):
    queryset = job_mobility.objects.all().order_by('pos_id')
    serializer_class = job_mobilitySerializer

class welfareViewSet(viewsets.ModelViewSet):
    queryset = welfare.objects.all().order_by('emp_id')
    serializer_class = welfareSerializer

class evaluation_scoreViewSet(viewsets.ModelViewSet):
    queryset = evaluation_score.objects.all().order_by('es_id')
    serializer_class = evaluation_scoreSerializer
class evaluation_score_empAPIView(APIView):
    def get(self, request, emp_id=None):
        if emp_id:
            items = evaluation_score_emp.objects.filter(emp_id=emp_id)
        else:
            items = evaluation_score_emp.objects.all().order_by('emp_id__pos_id')

        results = []
        for obj in items:
            serializer = evaluation_score_empSerializer(obj)
            data = serializer.data

            # Add extra fields manually
            emp = obj.emp_id
            pos = emp.pos_id if emp else None
            salary_record = Salary.objects.filter(pos_id=pos).first()
            salary = salary_record.SalaryGrade if salary_record else 0
            today = date.today()
            try:
                calclate_str = obj.es_id.calclate if obj.es_id else 0
                total_amount = Decimal(calclate_str) * Decimal(salary)
                today = dt_date.today()
            except Exception:
                total_amount = None

            # Combine and append to result
            data.update({
                "date": today,
                "emp_name": emp.lao_name if emp else "",
                "pos_id": pos.pos_id if pos else None,
                "pos_name": pos.name if pos else "",
                "salary": salary,
                "es_type": obj.es_id.es_type if obj.es_id else "",
                "calclate": obj.es_id.calclate if obj.es_id else "",
                "total_amount": total_amount
            })
            results.append(data)

        return Response(results, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = evaluation_score_empSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, emp_id=None):
        try:
            item = evaluation_score_emp.objects.filter(emp_id=emp_id).first()
            if not item:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Error retrieving data'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = evaluation_score_empSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, emp_id=None):
        items = evaluation_score_emp.objects.filter(emp_id=emp_id)
        if not items.exists():
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        items.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)
    
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

class UniformView(APIView):
    def get(self, request, uni_id=None):
        try:
            if uni_id:
                data = uniform.objects.select_related('uniform_price', 'emp_id__pos_id').get(uni_id=uni_id)
                if not data.uniform_price or not data.emp_id:
                    return Response({'error': 'Incomplete data'}, status=status.HTTP_400_BAD_REQUEST)

                # ແປເປັນ Decimal ປ້ອງກັນ error
                formal_suit = Decimal(data.uniform_price.formal_suit or 0)
                emp_uniform = Decimal(data.uniform_price.emp_uniform or 0)
                amount_uni = Decimal(data.amount_uni or 0)
                amount_sui = Decimal(data.amount_sui or 0)

                total_amount = (emp_uniform * amount_uni) + (formal_suit * amount_sui)

                result = {
                    "uni_id": data.uni_id,
                    "date": data.date or date.today(),
                    "emp_id": data.emp_id.emp_id,
                    "emp_name": data.emp_id.lao_name,
                    "pos_id": data.emp_id.pos_id.pos_id if data.emp_id.pos_id else None,
                    "pos_name": data.emp_id.pos_id.name if data.emp_id.pos_id else "",
                    "formal_suit": str(formal_suit),
                    "amount_sui": float(amount_sui),
                    "emp_uniform": str(emp_uniform),
                    "amount_uni": float(amount_uni),
                    "total_amount": float(total_amount)
                }
                return Response(result, status=status.HTTP_200_OK)

            else:
                all_data = uniform.objects.select_related('uniform_price', 'emp_id__pos_id').all().order_by("emp_id__pos_id")
                results = []
                for data in all_data:
                    if not data.uniform_price or not data.emp_id:
                        continue  # ຂ້າມລາຍການທີ່ຂໍ້ມູນບໍ່ຄົບ

                    formal_suit = Decimal(data.uniform_price.formal_suit or 0)
                    emp_uniform = Decimal(data.uniform_price.emp_uniform or 0)
                    amount_uni = Decimal(data.amount_uni or 0)
                    amount_sui = Decimal(data.amount_sui or 0)

                    total_amount = (emp_uniform * amount_uni) + (formal_suit * amount_sui)

                    results.append({
                        "uni_id": data.uni_id,
                        "date": data.date or date.today(),
                        "emp_id": data.emp_id.emp_id,
                        "emp_name": data.emp_id.lao_name,
                        "pos_id": data.emp_id.pos_id.pos_id if data.emp_id.pos_id else None,
                        "pos_name": data.emp_id.pos_id.name if data.emp_id.pos_id else "",
                        "formal_suit": str(formal_suit),
                        "amount_sui": float(amount_sui),
                        "emp_uniform": str(emp_uniform),
                        "amount_uni": float(amount_uni),
                        "total_amount": float(total_amount)
                    })
                return Response(results, status=status.HTTP_200_OK)

        except uniform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        emp_id = request.data.get('emp_id')

        # ກວດສອບວ່າ emp_id ມີ uniform ຢູ່ແລ້ວບໍ່
        if uniform.objects.filter(emp_id=emp_id).exists():
            return Response(
                {'error': 'ພະນັກງານຄົນນີ້ມີ uniform ຢູ່ແລ້ວ'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ຖ້າບໍ່ຊໍ້າ ກໍ່ສ້າງໃໝ່
        serializer = uniformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, uni_id):
        try:
            instance = uniform.objects.get(uni_id=uni_id)
        except uniform.DoesNotExist:
            return Response({'error': 'Uniform not found'}, status=status.HTTP_404_NOT_FOUND)

        # อัปเดต uniform หลัก
        serializer = uniformSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 👉 Handle update uniform_price
            uniform_price_instance = instance.uniform_price
            if uniform_price_instance:
                formal_suit = request.data.get("formal_suit")
                emp_uniform = request.data.get("emp_uniform")
                amount_sui = request.data.get("amount_sui")
                amount_uni = request.data.get("amount_uni")
                if formal_suit is not None:
                    uniform_price_instance.formal_suit = formal_suit
                if emp_uniform is not None:
                    uniform_price_instance.emp_uniform = emp_uniform
                if amount_sui is not None:
                    uniform_price_instance.amount_sui = amount_sui
                if amount_uni is not None:
                    uniform_price_instance.amount_uni = amount_uni
                uniform_price_instance.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, uni_id):
        try:
            instance = uniform.objects.get(uni_id=uni_id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except uniform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

#
#history....................................................................................................
#

@api_view(['POST'])
def reset_all_overtimes(request):
    overtimes = OvertimeWork.objects.all()  
    for ot in overtimes:
        ot.date = date.today()
        ot.csd_evening = None
        ot.csd_night = None
        ot.hd_mor_after = None
        ot.hd_evening = None
        ot.hd_night = None
        ot.total_ot = None
        ot.save()
    return Response({"message": "All OT records reset successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_all_saving_cooperatives(request):
    try:
        cooperatives = Saving_cooperative.objects.all()
        for sc in cooperatives:
            sc.loan_amount = 0
            sc.interest = 0
            sc.deposit = 0
            sc.Loan_deduction_194 = 0
            sc.date = date.today()
            sc.save()

        return Response({"message": "All Saving Cooperative records reset successfully."}, 
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({
                    'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"
                }, status=status.HTTP_400_BAD_REQUEST)
            # ກວດວ່າ emp_id ມີຂໍ້ມູນໃນເດືອນ/ປີນັ້ນແລ້ວບໍ່
            already_exists = Overtime_history.objects.filter(
                emp_id=item['emp_id'],
                date__year=target_year,
                date__month=target_month
            ).exists()
            if already_exists:
                duplicates.append(target_month)
        if duplicates:
            duplicate_months = sorted(set(duplicates))
            months_str = ", ".join(str(m) for m in duplicate_months)
            return Response({
                'error': f'ມີການຄິດໄລ່ໃນເດືອນ {months_str} ນີ້ແລ້ວ!!'
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
            # เอาเดือน/ปี ปัจจุบันมาใช้แทน date_insert ที่ request ส่งมา
            now = timezone.now()
            target_month = now.month
            target_year = now.year

            # ดึง records ของ emp_id
            records = colpolicy_history.objects.filter(emp_id=item['emp_id'])

            for record in records:
                # record.date_insert เป็น datetime อยู่แล้ว ไม่ต้อง strptime
                if record.date_insert.month == target_month and record.date_insert.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break  # ข้ามถ้าพบซ้ำแล้ว

        if duplicates:
            duplicate_months = sorted(set(d['month'] for d in duplicates))
            months_str = ", ".join(str(m) for m in duplicate_months)
            return Response({
                'error': f'ມີການຄິດໄລ່ໃນເດືອນ {months_str} ນີ້ແລ້ວ!!'
            }, status=status.HTTP_400_BAD_REQUEST)

        # validate และ save
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
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = fuel_payment_history.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                record_date = record.date
                if record_date.month == target_month and record_date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            duplicate_months = sorted(set(d['month'] for d in duplicates))
            months_str = ", ".join(str(m) for m in duplicate_months)
            return Response({
                'error': f'ມີການຄິດໄລ່ໃນເດືອນ {months_str} ນີ້ແລ້ວ!!',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_fuel_payment_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class specialday_emp_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                records = specialday_emp_history.objects.filter(emp_id=emp_id)
            else:
                records = specialday_emp_history.objects.all()
            serializer = get_specialday_emp_historyserializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            emp_id = item.get('emp_id')
            sdg_id = item.get('sdg_id')
            date_str = item.get('date')

            if not emp_id or not sdg_id or not date_str:
                return Response({'error': f"ຂໍ້ມູນຂາດ: {item}"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {date_str}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = specialday_emp_history.objects.filter(emp_id=emp_id, sdg_id=sdg_id)
            for record in existing_records:
                record_date = record.date
                if record_date.month == target_month and record_date.year == target_year:
                    duplicates.append({
                        'emp_id': emp_id,
                        'sdg_id': sdg_id,
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            duplicate_months = sorted(set(d['year'] for d in duplicates))
            months_str = ", ".join(str(m) for m in duplicate_months)
            return Response({
                'error': f'ມີການຄິດໄລ່ໃນເດືອນ {months_str} ນີ້ແລ້ວ!!',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_specialday_emp_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MobilePhoneSubsidy_emp_HistoryView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                records = MobilePhoneSubsidy_emp_History.objects.filter(emp_id=emp_id)
            else:
                records = MobilePhoneSubsidy_emp_History.objects.all().order_by('pos_id')
            serializer = get_MobilePhoneSubsidy_emp_Historyserializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data

        # ✅ check if data is list
        if not isinstance(data, list):
            return Response({'error': 'ຮູບແບບຂໍ້ມູນທີ່ສົ່ງມາຕ້ອງເປັນ List'}, status=status.HTTP_400_BAD_REQUEST)

        duplicates = []

        for item in data:
            # ✅ check if item is a dict
            if not isinstance(item, dict):
                return Response({'error': f"ຂໍ້ມູນຂາດຮູບແບບທີ່ຖືກຕ້ອງ: {item}"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ validate 'date' key
            if 'date' not in item:
                return Response({'error': f"ຂາດຂໍ້ມູນ 'date' ໃນຂໍ້ມູນ: {item}"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ check for duplicate (same emp_id + month + year)
            existing_records = MobilePhoneSubsidy_emp_History.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                if record.date.month == target_month and record.date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
                'duplicates': duplicates
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ save data if all valid
        serializer = post_MobilePhoneSubsidy_emp_Historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class saving_cooperative_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                records = saving_cooperative_history.objects.filter(emp_id=emp_id)
            else:
                records = saving_cooperative_history.objects.all()
            serializer = get_saving_cooperative_historyserializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = saving_cooperative_history.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                record_date = record.date
                if record_date.month == target_month and record_date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_saving_cooperative_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class monthly_paymentView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                monthly = monthly_payment.objects.filter(emp_id=emp_id)
                serializer = monthly_paymentSerializer(monthly, many=True)
            else:
                monthly = monthly_payment.objects.all()
                serializer = monthly_paymentSerializer(monthly, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class monthly_payment_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                monthly = monthly_payment_history.objects.filter(emp_id=emp_id)
                serializer = get_monthly_payment_historyserializer(monthly, many=True)
            else:
                monthly = monthly_payment_history.objects.all()
                serializer = get_monthly_payment_historyserializer(monthly, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data

        if not isinstance(data, list):
            return Response({'error': 'ຂໍ້ມູນທີ່ສົ່ງມາຕ້ອງແມ່ນ list'}, status=status.HTTP_400_BAD_REQUEST)

        duplicates = []

        for item in data:
            if not isinstance(item, dict):
                return Response({'error': 'ແຕ່ລະລາຍການຂອງຂໍ້ມູນຕ້ອງແມ່ນ object'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except (ValueError, KeyError):
                return Response({'error': f"ຂໍ້ມູນວັນທີບໍ່ຖືກຕ້ອງ: {item.get('date', 'N/A')}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = monthly_payment_history.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                if record.date.month == target_month and record.date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_monthly_payment_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class uniform_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                uniforms = uniform_history.objects.filter(emp_id=emp_id)
                serializer = get_uniform_historyserializer(uniforms, many=True)
            else:
                uniforms = uniform_history.objects.all()
                serializer = get_uniform_historyserializer(uniforms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data

        if not isinstance(data, list):
            return Response({'error': 'ຮູບແບບຂໍ້ມູນບໍ່ຖືກຕ້ອງ, ຄວນເປັນ List ຂອງ Dictionary'}, status=status.HTTP_400_BAD_REQUEST)

        duplicates = []

        for item in data:
            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except (ValueError, KeyError) as e:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ ຫຼື ບໍ່ມີ key 'date': {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = uniform_history.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                record_date = record.date
                if record_date.month == target_month and record_date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
            }, status=status.HTTP_40_BAD_REQUEST)

        serializer = post_uniform_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class evaluation_score_emp_historyView(APIView):
    def get(self, request, emp_id=None):
        try:
            if emp_id:
                uniforms = evaluation_score_emp_history.objects.filter(emp_id=emp_id)
                serializer = get_evaluation_score_emp_historyserializer(uniforms, many=True)
            else:
                uniforms = evaluation_score_emp_history.objects.all()
                serializer = get_evaluation_score_emp_historyserializer(uniforms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        duplicates = []

        for item in data:
            try:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                target_month = date_obj.month
                target_year = date_obj.year
            except ValueError:
                return Response({'error': f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {item['date']}"}, status=status.HTTP_400_BAD_REQUEST)

            existing_records = evaluation_score_emp_history.objects.filter(emp_id=item['emp_id'])
            for record in existing_records:
                record_date = record.date
                if record_date.month == target_month and record_date.year == target_year:
                    duplicates.append({
                        'emp_id': item['emp_id'],
                        'month': target_month,
                        'year': target_year
                    })
                    break

        if duplicates:
            return Response({
                'error': 'ມີຂໍ້ມູນຊ້ຳກັນໃນຖານຂໍ້ມູນ ເດືອນນີ້ໄດ້ບັນທຶກແລ້ວ!!',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = post_evaluation_score_emp_historyserializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class test_monly(APIView):
    @staticmethod
    def get_age(emp):
        if not emp or not emp.emp_id:
            return 0
        return (
            Employee_lcic.objects
            .filter(emp_id=emp.emp_id)
            .values_list("age_entry", flat=True)
            .first()
        )
    def get_1_5(self, emp):
        age = int(self.get_age(emp))
        if age <= 0:
            return 0
        y1 = SubsidyYear.objects.filter(sy_id=1).first()
        return y1.y_subsidy * 5 if y1 else 0
        
    def get_6_15(self, emp):
        age = int(self.get_age(emp))
        if age <= 5:
            return 0 
        age_6_15 = age - 5
        y2 = SubsidyYear.objects.filter(sy_id=2).first()
        if age_6_15 > 15:
            return y2.y_subsidy * 10
        else:
            return y2.y_subsidy * age_6_15

    def get_16_25(self, emp):
        age = int(self.get_age(emp))
        if age <= 15:
            return 0 
        age_16_25 = age - 15
        y3 = SubsidyYear.objects.filter(sy_id=3).first()
        if age_16_25 > 10:
            return y3.y_subsidy * 10
        else:
            return y3.y_subsidy * age_16_25
        
    def get_26(self, emp):
        age = int(self.get_age(emp))
        if age <= 25:
            return 0 
        age_26 = age - 25
        y4 = SubsidyYear.objects.filter(sy_id=4).first()
        if age_26 > 10:
            return y4.y_subsidy * 10
        else:
            return y4.y_subsidy * age_26
        
    def get_overtime_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            Overtime_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_ot", flat=True)
            .first()
        ) or 0
    def get_fuel_payment_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            fuel_payment_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_fuel", flat=True)
            .first()
        ) or 0
    def get_colpolicy_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            colpolicy_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_payment", flat=True)
            .first()
        ) or 0
    def get_specialday_emp_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            specialday_emp_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("grant", flat=True)
            .first()
        ) or 0
    def get_uniform_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            uniform_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_amount", flat=True)
            .first()
        ) or 0

    def get_sving_cooperative_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            saving_cooperative_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_Saving", flat=True)
            .first()
        ) or 0
        
    def get_MobilePhoneSubsidy_emp_History(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            MobilePhoneSubsidy_emp_History.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("grant", flat=True)
            .first()
        ) or 0
    
    def get_evaluation_score_emp_history(self, emp):
        if not emp or not emp.emp_id:
            return 0
        now = timezone.now()
        return (
            evaluation_score_emp_history.objects
            .filter(
                emp_id=emp.emp_id,
                date__year=now.year,
                date__month=now.month
            )
            .values_list("total_amount", flat=True)
            .first()
        ) or 0
    
    def get_exempt(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
        if income > 130000.00:
            t1 = income_tax.objects.filter(tax_id=1).first()
            return t1.calculation_base if t1 else Decimal('0')
    def get_tax_5(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
        if Decimal('1300000.00') < income <= Decimal('5000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            return (income - t1.calculation_base) * t2.tariff if t2 else Decimal('0')
        if income > Decimal('5000000.00'):
            t2 = income_tax.objects.filter(tax_id=2).first()
            return (t2.calculation_base * t2.tariff) if t2 else Decimal('0')
    def get_tax_10(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
        if Decimal('5000000.00') < income <= Decimal('15000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            return (income - (t1.calculation_base + t2.calculation_base)) * t3.tariff if t3 else Decimal('0')
        if income > Decimal('15000000.00'):
            t3 = income_tax.objects.filter(tax_id=3).first()
            return (t3.calculation_base * t3.tariff) if t3 else Decimal('0')

    def get_tax_15(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
        if Decimal('15000000.00') < income <= Decimal('25000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            t4 = income_tax.objects.filter(tax_id=4).first()
            return (income - (t1.calculation_base + t2.calculation_base + t3.calculation_base)) * t4.tariff if t4 else Decimal('0')
        if income > Decimal('25000000.00'):
            t4 = income_tax.objects.filter(tax_id=4).first()
            return (t4.calculation_base * t4.tariff) if t4 else Decimal('0')

    def get_tax_20(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
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

    def get_tax_25(self, emp):
        income = getattr(emp, "income_before_tax", Decimal(0))
        if income > Decimal('65000000.00'):
            t1 = income_tax.objects.filter(tax_id=1).first()
            t2 = income_tax.objects.filter(tax_id=2).first()
            t3 = income_tax.objects.filter(tax_id=3).first()
            t4 = income_tax.objects.filter(tax_id=4).first()
            t5 = income_tax.objects.filter(tax_id=5).first()
            t6 = income_tax.objects.filter(tax_id=6).first()
            return (income - (t1.calculation_base + t2.calculation_base + t3.calculation_base + t4.calculation_base + t5.calculation_base)) * t6.tariff if t6 else Decimal('0')

    def get(self, request, emp_id=None):
        try:
            base_queryset = Employee_lcic.objects.select_related("pos_id").prefetch_related(
                Prefetch(
                    "monthly_payment_set",
                    queryset=monthly_payment.objects.order_by("-date"),
                    to_attr="payments",
                )
            )
            if emp_id:
                employees = base_queryset.filter(emp_id=emp_id).order_by("pos_id")
            else:
                employees = base_queryset.order_by("pos_id")
            pos_ids = employees.values_list("pos_id", flat=True)
            salary_map = {s.pos_id_id: s for s in Salary.objects.filter(pos_id__in=pos_ids)}
            subsidy_pos_map = {s.pos_id_id: s for s in SubsidyPosition.objects.filter(pos_id__in=pos_ids)}
            welfare_map = {w.emp_id_id: w for w in welfare.objects.filter(emp_id__in=employees.values_list("emp_id", flat=True))}
            today = date.today()
            current_month = today.month
            current_year = today.year
            saving_map = {
                s.emp_id: s
                for s in saving_cooperative_history.objects.filter(
                    emp_id__in=employees.values_list("emp_id", flat=True),
                    date__month=current_month,
                    date__year=current_year
                )
            }
            data = []
            for emp in employees:
                today = dt_date.today()
                latest_payment = emp.payments[0] if emp.payments else None
                pos_id = emp.pos_id_id
                position = emp.pos_id.name if emp.pos_id else None
                age = self.get_age(emp)
                get_1_5 = self.get_1_5(emp)
                get_6_15 = self.get_6_15(emp)
                get_16_25 = self.get_16_25(emp)
                get_26 = self.get_26(emp)
                year_subsidy_total = get_1_5 + get_6_15 + get_16_25 + get_26
                salary = salary_map.get(pos_id).SalaryGrade if pos_id in salary_map else Decimal(0)
                wf_emp = welfare_map.get(emp.emp_id).from_emp if emp.emp_id in welfare_map else 0
                wf_cpn = welfare_map.get(emp.emp_id).from_company if emp.emp_id in welfare_map else 0
                position_subsidy = subsidy_pos_map.get(pos_id).grant if pos_id in subsidy_pos_map else 0
                ot = self.get_overtime_history(emp)
                basic_income = (salary + position_subsidy + year_subsidy_total + ot) - wf_emp
                fuel = self.get_fuel_payment_history(emp)
                regular_income = Decimal(basic_income) + Decimal(fuel)
                colpolicy = self.get_colpolicy_history(emp)
                specialday = self.get_specialday_emp_history(emp)
                uniform = self.get_uniform_history(emp)
                MobilePhoneSubsidy = self.get_MobilePhoneSubsidy_emp_History(emp)
                evaluation_score = self.get_evaluation_score_emp_history(emp)
                other_income = (Decimal(self.get_colpolicy_history(emp)) 
                                + Decimal(self.get_specialday_emp_history(emp)) 
                                + Decimal(self.get_uniform_history(emp)) 
                                + Decimal(self.get_MobilePhoneSubsidy_emp_History(emp)) 
                                + Decimal(self.get_evaluation_score_emp_history(emp)))
                income_before_tax = Decimal(regular_income) + Decimal(other_income)
                emp.income_before_tax = income_before_tax
                exempt = self.get_exempt(emp)
                tax_5 = self.get_tax_5(emp)
                tax_10 = self.get_tax_10(emp)
                tax_15 = self.get_tax_15(emp)
                tax_20 = self.get_tax_20(emp)
                tax_25 = self.get_tax_25(emp)
                total_tax = sum([Decimal(t or 0) for t in [tax_5, tax_10, tax_15, tax_20, tax_25]])

                income_after_tax = basic_income - total_tax

                child = latest_payment.child if latest_payment else 0
                child_subsidy = latest_payment.child_Subsidy if latest_payment else 0
                child_subsidy_total = Decimal(child_subsidy) * Decimal(child) if child else Decimal(0)
                health_subsidy = latest_payment.health_Subsidy if latest_payment else 0

                saving = saving_map.get(emp.emp_id)
                loan = saving.loan_amount if saving else 0
                interest = saving.interest if saving else 0
                deposit = saving.deposit if saving else 0
                loan_194 = saving.Loan_deduction_194 if saving else 0
                saving_total = saving.total_Saving if saving else 0

                salary_payment = Decimal(income_after_tax) + Decimal(child_subsidy_total) + Decimal(health_subsidy) - Decimal(saving_total) + Decimal(loan_194)
                monthly_income = Decimal(fuel) + Decimal(other_income) + Decimal(salary_payment)

                data.append({
                    "date": today,
                    "emp_id": emp.emp_id,
                    "lao_name": emp.lao_name,
                    "pos_id": pos_id,
                    "position": position,
                    "salary": salary,
                    "wf_emp": wf_emp,
                    "wf_cpn": wf_cpn,
                    "position_subsidy": position_subsidy,
                    "age": age,
                    "get_1_5": get_1_5,
                    "get_6_15": get_6_15,
                    "get_16_25": get_16_25,
                    "get_26": get_26,
                    "year_subsidy_total": year_subsidy_total,
                    "ot": ot,
                    "basic_income": basic_income,
                    "fuel": fuel,
                    "regular_income": regular_income,
                    "colpolicy": colpolicy,
                    "specialday": specialday,
                    "uniform": uniform,
                    "MobilePhoneSubsidy": MobilePhoneSubsidy,
                    "evaluation_score": evaluation_score,
                    "other_income": other_income,
                    "income_before_tax": income_before_tax,
                    "exempt": exempt,
                    "tax_5": tax_5,
                    "tax_10": tax_10,
                    "tax_15": tax_15,
                    "tax_20": tax_20,
                    "tax_25": tax_25,
                    "total_tax": total_tax,
                    "income_after_tax": income_after_tax,
                    "child": child,
                    "child_subsidy": child_subsidy,
                    "child_subsidy_total": child_subsidy_total,
                    "health_subsidy": health_subsidy,
                    "loan": loan,
                    "interest": interest,
                    "deposit": deposit,
                    "loan_194": loan_194,
                    "saving_total": saving_total,
                    "salary_payment": salary_payment,
                    "monthly_income": monthly_income,
                })

            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)