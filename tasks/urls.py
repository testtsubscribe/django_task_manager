from django.contrib import admin
from django.urls import path, include
from tasks.views import CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('tasks.urls')),
]
