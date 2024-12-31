from django.urls import path, include
from .views import EmployeeListAPI
from .views import EmployeeDetailView,EmployeeCreateView,EmployeeDeleteView,EmployeeUpdateView
from .views import Document_outListView,Document_outCreateView,Document_outDeleteView,Document_outUpdateView
from .views import DocumentEntryListView,DocumentEntryCreateView,DocumentEntryDeleteView,DocumentEntryUpdateView
from .views import activityCreateView,activityListView,activityDeleteView,activityUpdateView
from .views import UserLogin,DepartmentListView
from .views import DocumentEntryList
from rest_framework.routers import DefaultRouter
from .views import DocumentEntryViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'document_entries', DocumentEntryViewSet)

urlpatterns = [

    path('login/', UserLogin.as_view(), name='user_login'),

    path('api/', include(router.urls)),
    path('list/employees/', EmployeeListAPI.as_view(), name='employee-list'),
    path('detail/employee/<int:emp_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('add/employee/', EmployeeCreateView.as_view(), name='employee-create'),
    path('delete/employee/<int:emp_id>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('update/employee/<int:emp_id>/', EmployeeUpdateView.as_view(), name="update_employee"),

    path('list/Document_out/', Document_outListView.as_view(), name='Document_out-list'),
    path('add/document_out/', Document_outCreateView.as_view(), name='Document_out-create'),
    path('delete/document_out/<int:id>/',Document_outDeleteView.as_view(), name='Document_out-delete'),
    path('update/document_out/<int:id>/',Document_outUpdateView.as_view(), name='Document_out-update'),

    path('list/DocumentEntry/', DocumentEntryListView.as_view(), name='DocumentEntry-list'),
    path('add/DocumentEntry/', DocumentEntryCreateView.as_view(), name='DocumentEntry-create'),
    path('delete/DocumentEntry/<int:id>/',DocumentEntryDeleteView.as_view(), name='DocumentEntry-delete'),
    path('update/DocumentEntry/<int:id>/',DocumentEntryUpdateView.as_view(), name='DocumentEntry-update'),

    path('list/activity/', activityListView.as_view(), name='activity-list'),
    path('add/activity/', activityCreateView.as_view(), name='activity-create'),
    path('delete/activity/<int:id>/',activityDeleteView.as_view(), name='activity-delete'),
    path('update/activity/<int:id>/',activityUpdateView.as_view(), name='activity-update'),

    path('list/departments/', DepartmentListView.as_view(), name='department-list'),

    path('api/document-entries/', DocumentEntryList.as_view(), name='document-entry-list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)