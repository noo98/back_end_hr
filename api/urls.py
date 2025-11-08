from django.urls import path
from .views import UserView,LoginView, reset_all_saving_cooperatives, sum_MobilePhoneSubsidy_emp_History_view, sum_colpolicy_history_view, sum_evaluation_score_emp_history_view, sum_fuel_payment_history_view, sum_monthly_income_history_view, sum_salary_payment_history_view, sum_saving_cooperative_history_view, sum_specialday_emp_history_view, sum_total_Overtime_history_view, sum_uniform_history_view
from .views import Employee_lcicView,EmployeeInfoAPI,UpdateAllJobMobilityAPIView
from .views import document_lcic_ListView,document_lcic_AddView,document_lcic_UpdateView,document_lcic_deleteView
from .views import document_lcic_SearchView
from .views import DepartmentListView,DepartmentList_idView,document_general_View,DocumentFormatSearchView
from .views import Department_AddView,Department_UpdateView,Department_DeleteView,document_lcic_List_idView,document_general_SearchView
from .views import Document_format_ListView,Document_format_AddView,Document_format_UpdateView,Document_format_DeleteView,Document_format_idView
from .views import UpdateDocumentStatus,docstatus,AutoUpdateStatusDocAPIView,user_empView, UniformView
# from .views import AssetTypeView,AssetView,CategoryView,CategorySearchView
from django.conf import settings
from django.conf.urls.static import static
# from .views import update_view_status
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PositionViewSet
from .views import FuelSubsidyView
from .views import reset_all_overtimes
from .views import (Overtime_historyView, colpolicy_historyView, fuel_payment_historyView,saving_cooperative_historyView,specialday_emp_historyView, monthly_payment_historyView,
uniform_historyView,MobilePhoneSubsidy_empAPIView)

from .views import (
    PositionViewSet, SalaryViewSet, SubsidyPositionViewSet,Saving_cooperativeViewSet,SpecialDay_empViewSet,welfareViewSet,evaluation_scoreViewSet,
    SubsidyYearViewSet, FuelSubsidyView,col_policyViewSet,Fuel_pamentViewSet,job_mobilityViewSet,health_allowanceViewSet,
    SpecialDayGrantViewSet, MobilePhoneSubsidyViewSet,ovtimeWorkView,income_taxViewSet,SpecialDayViewSet,SpecialDayPositionFilterAPIView,evaluation_score_empAPIView,
    evaluation_score_emp_historyView,MobilePhoneSubsidy_emp_HistoryView, RoleListCreate, RoleRetrieveUpdateDestroy,RolePermissionListCreate, RolePermissionRetrieveUpdateDestroy,
    MenuListCreate, MenuRetrieveUpdateDestroy,MainMenuListCreate, MainMenuRetrieveUpdateDestroy,UserMenuDetail, Housing_loanRetrieveUpdateDestroy, Housing_loanListCreate,
    Housing_loan_historyRetrieveUpdateDestroy, Housing_loan_historyListCreate, import_housing_loan_excel, BankAccountUpdateDestroy, BankAccountListCreate, 
    Housing_loan_historyView, delete_all_history_by_month, status_monthly_payment_history_view,import_coopertive_excel
)
from .views import (payroll_monly)
router = DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'fuel_payment', Fuel_pamentViewSet)
router.register(r'sal', SalaryViewSet)
router.register(r'sp', SubsidyPositionViewSet)
router.register(r'sy', SubsidyYearViewSet)
router.register(r'sdg', SpecialDayGrantViewSet, basename='specialday-position')
router.register(r'sdg_emp', SpecialDay_empViewSet,basename='specialday-emp')
router.register(r'sd', SpecialDayViewSet, basename='specialday')
router.register(r'mps', MobilePhoneSubsidyViewSet)
router.register(r'col_policy', col_policyViewSet)
router.register(r'job_mobility', job_mobilityViewSet)
router.register(r'income_tax', income_taxViewSet)
router.register(r'sc', Saving_cooperativeViewSet)
router.register(r'welfare', welfareViewSet)
router.register(r'es', evaluation_scoreViewSet)
# router.register(r'ot', OvertimeWorkViewSet)
router.register(r'health_allowance', health_allowanceViewSet)
from .views import get_position_details
urlpatterns = [
    path('users/', UserView.as_view(), name='user-list-create'),
    path('users/<int:us_id>/', UserView.as_view(), name='user-update-delete'),
    path('users/<str:username>/', UserView.as_view(), name='username'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_emp/', user_empView.as_view(), name='user_emp-list'),
    path('user_emp/<int:us_id>/', user_empView.as_view(), name='user_emp-id'),
    path('users_menu/<int:pk>/', UserMenuDetail.as_view(), name='user-menus'),

    path('roles/', RoleListCreate.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroy.as_view(), name='role-detail'),

    path('bank_ac/', BankAccountListCreate.as_view(), name='BankAccount-list-create'),
    path('bank_ac/<int:pk>/', BankAccountUpdateDestroy.as_view(), name='BankAccount-detail'),
    
    # RolePermission URLs
    path('role-permissions/', RolePermissionListCreate.as_view(), name='rolepermission-list-create'),
    path('role-permissions/<int:pk>/', RolePermissionRetrieveUpdateDestroy.as_view(), name='rolepermission-detail'),
    
    # Menu URLs
    path('menu/', MenuListCreate.as_view(), name='menu-list-create'),
    path('menu/<int:pk>/', MenuRetrieveUpdateDestroy.as_view(), name='menu-detail'),
    
    # MainMenu URLs
    path('mainmenu/', MainMenuListCreate.as_view(), name='mainmenu-list-create'),
    path('mainmenu/<int:pk>/', MainMenuRetrieveUpdateDestroy.as_view(), name='mainmenu-detail'),


    path('employee/', Employee_lcicView.as_view(), name='employees-list-create'),
    path('employee/<int:emp_id>/', Employee_lcicView.as_view(), name='employees-update-delete'),

    path('api/employees/', EmployeeInfoAPI.as_view(), name='employee_info_api'),

    path('list/document_lcic/', document_lcic_ListView.as_view(), name='document_lcic-list'),
    path('list/document_lcic/<int:doc_id>/', document_lcic_List_idView.as_view(), name='document_list_id'),
    path('add/document_lcic/', document_lcic_AddView.as_view(), name='document_lcic-create'),
    path('update/document_lcic/<int:doc_id>/',document_lcic_UpdateView.as_view(), name='document_lcic-update'),
    path('delete/document_lcic/<int:doc_id>/',document_lcic_deleteView.as_view(), name='document_lcic-delete'),
    path('update_status/<int:doc_id>/', UpdateDocumentStatus.as_view(), name='update-document-status'),
    path('search/document_lcic/', document_lcic_SearchView.as_view(), name='search-document'),
  

    path('list/departments/', DepartmentListView.as_view(), name='department-list'),
    path('list/departments/<int:id>/', DepartmentList_idView.as_view(), name='departments-list_id'),
    path('add/departments/', Department_AddView.as_view(), name='departments-add'),
    path('update/departments/<int:id>/', Department_UpdateView.as_view(), name='update-departments'),
    path('delete/departments/<int:id>/', Department_DeleteView.as_view(), name='delete-departments'),

    path('list/Document_format/', Document_format_ListView.as_view(), name='Document_format-list'),
    path('list/Document_format/<int:dmf_id>/', Document_format_idView.as_view(), name='Document_format-list_id'),
    path('add/Document_format/', Document_format_AddView.as_view(), name='Document_format-add'),
    path('update/Document_format/<int:dmf_id>/', Document_format_UpdateView.as_view(), name='update-Document_format'),
    path('delete/Document_format/<int:dmf_id>/', Document_format_DeleteView.as_view(), name='delete-Document_format'),    
    path('search/Document_format/', DocumentFormatSearchView.as_view(), name='search-document'),

    path('document_general/', document_general_View.as_view(), name='document_general-list-create'),
    path('document_general/<int:docg_id>/', document_general_View.as_view(), name='document_general-update-delete'),
    path('search/document_general/', document_general_SearchView.as_view(), name='search-document_general'),
    path('auto-update-status/', AutoUpdateStatusDocAPIView.as_view(), name='auto_update_status_doc'),

    # path('personal/', PersonalEducationCreateView.as_view(), name='personal-education-create'),
    # path('personal/<int:per_id>/', PersonalEducationCreateView.as_view(), name='personal-update-delete'),

    path('update_doc_status/', docstatus.as_view(), name='update-document-status'),

   

    # path('asset_types/', AssetTypeView.as_view()),
    # path('asset_types/<int:ast_id>/', AssetTypeView.as_view()),

    # path('assets/', AssetView.as_view()),
    # path('assets/<int:as_id>/', AssetView.as_view()),
    
    # path('category/', CategoryView.as_view()),
    # path('category/<int:cat_id>/', CategoryView.as_view()),
    # path('category/search/', CategorySearchView.as_view(), name='category-search'),

    path('', include(router.urls)),

    # path('fuel-price/', FuelPriceView.as_view(), name='fuel-price'),

    path('mps_emp/',MobilePhoneSubsidy_empAPIView.as_view(), name='mobile-phone-subsidy-emp-list'),
    path('mps_emp/<int:emp_id>/', MobilePhoneSubsidy_empAPIView.as_view(), name='mobile-phone-subsidy-emp-detail'),

    path('fuel/', FuelSubsidyView.as_view(), name='fuel_subsidy_list'),
    path('fuel/<int:fs_id>/', FuelSubsidyView.as_view(), name='fuel_subsidy_detail'),

    path('emp_sal/<int:emp_id>', get_position_details, name='employee-position-details'),

    path('ot/', ovtimeWorkView.as_view(), name='monthly-payment-list-create'),
    path('ot/<int:ot_id>/', ovtimeWorkView.as_view(), name='monthly-payment-update-delete'),
    path('reset_all_ot/', reset_all_overtimes, name='reset-all-overtimes'),
    path('reset_all_sc/', reset_all_saving_cooperatives, name='reset-all-saving'),

    path('mon_ly/', payroll_monly.as_view(), name='monthly-payment-list-create'),
    path('mon_ly/<int:emp_id>/', payroll_monly.as_view(), name='monthly-payment-update-delete'),
    path('sal_increase/<int:emp_id>/', payroll_monly.as_view(), name='salary-increase'),

    path('uniform/', UniformView.as_view()),
    path('uniform/<int:uni_id>/', UniformView.as_view()),

    path('es_emp/', evaluation_score_empAPIView.as_view()),
    path('es_emp/<int:emp_id>/', evaluation_score_empAPIView.as_view()),
    path('es_emp/<int:ese_id>/', evaluation_score_empAPIView.as_view()),

    #History

    path('ot_history/', Overtime_historyView.as_view(), name='overtime-history-list'),
    path('ot_history/<int:emp_id>/', Overtime_historyView.as_view(), name='overtime-history-detail'),
    path('ot_history/delete_month/<str:year_month>/', Overtime_historyView.as_view()),

    path('col_history/', colpolicy_historyView.as_view(), name='col_policy-history-list'),
    path('col_history/<int:emp_id>/', colpolicy_historyView.as_view(), name='col_policy-history-detail'),
    path('col_history/delete_month/<str:year_month>/', colpolicy_historyView.as_view()),
    path('job_update_all/', UpdateAllJobMobilityAPIView.as_view(), name='update_all_job_mobility'),

    path('hous_loan/', Housing_loanListCreate.as_view(), name='Hous_loan-list-create'),
    path('hous_loan/<int:pk>/', Housing_loanRetrieveUpdateDestroy.as_view(), name='Hous_loan-detail'),

    path('hous_loan_history/', Housing_loan_historyListCreate.as_view(), name='Hous_loan-list-create'),
    path('hous_loan_history/<int:pk>/', Housing_loan_historyRetrieveUpdateDestroy.as_view(), name='Hous_loan-detail'),
    path('hous_loan_history/delete_month/<str:year_month>/', Housing_loan_historyView.as_view()),
    path('hous_loan_excel/', import_housing_loan_excel, name='import-housing-loan-excel'),
    path('sc_excel/', import_coopertive_excel, name='import-coopertive-excel'),

    path('fuel_history/', fuel_payment_historyView.as_view(), name='fuel_subsidy_history_list'),
    path('fuel_history/<int:emp_id>/', fuel_payment_historyView.as_view(), name='fuel_subsidy_history_detail'),
    path('fuel_history/delete_month/<str:year_month>/', fuel_payment_historyView.as_view()),

    path('sc_history/', saving_cooperative_historyView.as_view(), name='saving_cooperative_history_list'),
    path('sc_history/<int:emp_id>/', saving_cooperative_historyView.as_view(), name='saving_cooperative_history_detail'),
    path('sc_history/delete_month/<str:year_month>/', saving_cooperative_historyView.as_view()),


    path('mps_emp_history/', MobilePhoneSubsidy_emp_HistoryView.as_view(), name='mobile_phone_subsidy_emp_history_list'),
    path('mps_emp_history/<int:emp_id>/', MobilePhoneSubsidy_emp_HistoryView.as_view(), name='mobile_phone_subsidy_emp_history_detail'),
    path('mps_emp_history/delete_month/<str:year_month>/', MobilePhoneSubsidy_emp_HistoryView.as_view()),

    path('sdg_emp_history/', specialday_emp_historyView.as_view(), name='specialday_emp_history_list'),
    path('sdg_emp_history/<int:emp_id>/', specialday_emp_historyView.as_view(), name='specialday_emp_history_detail'),
    path('sdg_emp_history/delete_month/<str:year_month>/', specialday_emp_historyView.as_view()),

    path('uniform_history/', uniform_historyView.as_view(), name='uniform_history_list'),
    path('uniform_history/<int:emp_id>/', uniform_historyView.as_view(), name='uniform_history_detail'),
    path('uniform_history/delete_month/<str:year_month>/', uniform_historyView.as_view()),
 
    path('es_emp_history/', evaluation_score_emp_historyView.as_view(), name='uniform_history_list'),
    path('es_emp_history/<int:emp_id>/', evaluation_score_emp_historyView.as_view(), name='uniform_history_detail'),
    path('es_emp_history/delete_month/<str:year_month>/', evaluation_score_emp_historyView.as_view()),

    path('mon_ly_history/', monthly_payment_historyView.as_view(), name='monthly_payment_history_list'),
    path('mon_ly_history/<int:emp_id>/', monthly_payment_historyView.as_view(), name='monthly_payment_history_detail'),
    path('mon_ly_history/delete_month/<str:year_month>/', monthly_payment_historyView.as_view()),
    path('history/delete_all/<str:year_month>/', delete_all_history_by_month, name='delete_all_history'),
    path('status_monthly_payment/', status_monthly_payment_history_view.as_view(), name='status-monthly-payment'),

    path('sdg_filter/', SpecialDayPositionFilterAPIView.as_view(), name='specialday-filter'),

    # path('status_ot/', CheckOvertimeHistoryView.as_view(), name='specialday-filter'),

    # sum total ot current month

    path('sum_ot/', sum_total_Overtime_history_view.as_view(), name='total-sum'),
    path('sum_colpolicy/', sum_colpolicy_history_view.as_view(), name='total-sum'),
    path('sum_fuel/', sum_fuel_payment_history_view.as_view(), name='total-sum'),
    path('sum_specialday/', sum_specialday_emp_history_view.as_view(), name='total-sum'),
    path('sum_Mobile/', sum_MobilePhoneSubsidy_emp_History_view.as_view(), name='total-sum'),
    path('sum_saving/', sum_saving_cooperative_history_view.as_view(), name='total-sum'),
    path('sum_uniform/', sum_uniform_history_view.as_view(), name='total-sum'),
    path('sum_score/', sum_evaluation_score_emp_history_view.as_view(), name='total-sum'),
    path('salary_payment/', sum_salary_payment_history_view.as_view(), name='total-sum'),
    path('monthly_income/', sum_monthly_income_history_view.as_view(), name='total-sum'),


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)