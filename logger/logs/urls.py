from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import  settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import ProfileCreateView, ProfileDetailView, CreateFile, CreateProject,ProjectDetail, LogList, LogDetail, LogCreate

urlpatterns = [
    path('welcome',views.welcome,name='home'),
    path('',views.projects_page,name='project_page'),
    path('signup/',views.register,name='signup'),
    path('profile-create/',ProfileCreateView.as_view(),name='profile-create'),
    path('login/',auth_views.LoginView.as_view(template_name='logs/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logs/logout.html'),name='logout'),
    path('profile-detail/<int:pk>/',ProfileDetailView.as_view(),name='profile-detail'),
    path('profile-update/',views.profile_update,name='profile-update'),
    path('file/create',CreateFile.as_view(),name='create-file'),
    path('files/<str:name>',views.file_detail,name='file'),
    path('project-create/',CreateProject.as_view(),name='project-create'),
    path('project/<int:pk>/',views.project_detail,name='project-detail'),
    path('log-create/',LogCreate.as_view(),name='log-create'),
    path('log/list',LogList.as_view(),name='logs'),
    path('log/<int:pk>/',views.log_detail,name='log-detail')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)