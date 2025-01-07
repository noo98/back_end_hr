from django.urls import path
from .views import EmployeeListAPI
from .views import EmployeeDetailView,EmployeeCreateView,EmployeeDeleteView,EmployeeUpdateView
from .views import document_lcic_ListView,document_lcic_AddView,document_lcic_UpdateView,document_lcic_DeleteView
from .views import activityCreateView,activityListView,activityDeleteView,activityUpdateView
from .views import UserLogin,DepartmentListView,LoginView,LoginlistView,LoginaddView,DeleteUserView,UpdateUserView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),

    path('list/employees/', EmployeeListAPI.as_view(), name='employee-list'),
    path('detail/employee/<int:emp_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('add/employee/', EmployeeCreateView.as_view(), name='employee-create'),
    path('delete/employee/<int:emp_id>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('update/employee/<int:emp_id>/', EmployeeUpdateView.as_view(), name="update_employee"),

    path('list/document_lcic/', document_lcic_ListView.as_view(), name='document_lcic-list'),
    path('add/document_lcic/', document_lcic_AddView.as_view(), name='document_lcic-create'),
    path('update/document_lcic/<int:doc_id>/',document_lcic_UpdateView.as_view(), name='document_lcic-update'),
    path('delete/document_lcic/<int:doc_id>/',document_lcic_DeleteView.as_view(), name='document_lcic-delete'),

    path('list/activity/', activityListView.as_view(), name='activity-list'),
    path('add/activity/', activityCreateView.as_view(), name='activity-create'),
    path('delete/activity/<int:id>/',activityDeleteView.as_view(), name='activity-delete'),
    path('update/activity/<int:id>/',activityUpdateView.as_view(), name='activity-update'),

    path('list/departments/', DepartmentListView.as_view(), name='department-list'),

    path('list/login/', LoginlistView.as_view(), name='Loginl-list'),
    path('add/login/', LoginaddView.as_view(), name='Loginl-add'),
    path('update/login/<int:user_id>/', UpdateUserView.as_view(), name='update-user'),
    path('delete/login/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
]
