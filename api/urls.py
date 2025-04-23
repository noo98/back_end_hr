from django.urls import path
from .views import UserView,LoginView
from .views import Employee_lcicView,EmployeeInfoAPI
from .views import document_lcic_ListView,document_lcic_AddView,document_lcic_UpdateView,document_lcic_deleteView
from .views import activityCreateView,activityListView,activityDeleteView,activityUpdateView,document_lcic_SearchView
from .views import DepartmentListView,DepartmentList_idView,document_general_View,permission_lcic_View,DocumentFormatSearchView
from .views import Department_AddView,Department_UpdateView,Department_DeleteView,document_lcic_List_idView,document_general_SearchView
from .views import Document_format_ListView,Document_format_AddView,Document_format_UpdateView,Document_format_DeleteView,Document_format_idView
from .views import sidebar_View,UpdateDocumentStatus,docstatus,AutoUpdateStatusDocAPIView,user_empView
# from .views import AssetTypeView,AssetView,CategoryView,CategorySearchView
from django.conf import settings
from django.conf.urls.static import static
from .views import update_view_status


urlpatterns = [
    path('users/', UserView.as_view(), name='user-list-create'),
    path('users/<int:us_id>/', UserView.as_view(), name='user-update-delete'),
    path('users/<str:username>/', UserView.as_view(), name='username'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_emp/', user_empView.as_view(), name='user_emp-list'),

    path('permission/', permission_lcic_View.as_view(), name='permission-list-create'),
    path('permission/<int:sta_id>/', permission_lcic_View.as_view(), name='permission-update-delete'),

    path('sidebar/', sidebar_View.as_view(), name='sidebar-list'),

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
  
    
    path('list/activity/', activityListView.as_view(), name='activity-list'),
    path('add/activity/', activityCreateView.as_view(), name='activity-create'),
    path('delete/activity/<int:id>/',activityDeleteView.as_view(), name='activity-delete'),
    path('update/activity/<int:id>/',activityUpdateView.as_view(), name='activity-update'),

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

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)