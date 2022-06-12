from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('edit_profile/<str:username>', views.editProfile, name='edit_profile'),
    path('new/project', views.new_project, name='new_project'),
    re_path(r'^project/(\d+)', views.get_project, name='project_results'),
    path('search/', views.search_projects, name='search_results'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/project/', views.ProjectList.as_view()),
    path('login/', auth_view.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    
   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns = format_suffix_patterns(urlpatterns)