from django.urls import path

from . import views


app_name = 'vuln'
urlpatterns = [
    path('', views.index, name='index'),
    path('scans/', views.scan_start, name='scan_start'),
    path('scani/', views.scan_work, name='scan_work'),
    path('scane/<str:task_id>', views.scan_end, name='scan_end'),
    path('vuln_info/', views.vuln_info, name='vuln_info'),
    path('check/session_test/', views.session_test, name='session_test'),
    path('check/url_access/', views.url_access, name='url_access'),
]