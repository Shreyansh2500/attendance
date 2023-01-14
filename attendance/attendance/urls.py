"""attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from management import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('approval/<int:leaveId>/<int:status>/',views.decision,name="decision"),
    path('approval/',views.approval,name="approval"),
    path('',views.home,name="home"),
    path('record/',views.record,name="record"),
    path('request/',views.request,name="request"),
    path('history/',views.history,name="history"),

    #path('<int:year>/<str:month>/', views.home, name="home"),
    path('dashboard/',views.dashboard),
]