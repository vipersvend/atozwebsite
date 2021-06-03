from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'home'),
    path('allservices/', views.all_services,name = 'allservices'),
    path('login/', views.login,name = 'login'),

    path('register/', views.register,name = 'register'),
    path('new_service/', views.new_service,name = 'new_service'),
    path('new_provider/', views.new_provider, name = 'new_provider'),
    path('logout/', views.logout_view, name = 'logout'),
    path('serviceproviders/', views.serviceproviders, name = 'serviceproviders'),
    path('service/<str:service_id>', views.service, name = 'service'),
     
]