from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('login/', views.login, name='login'),
    path('token/', views.token, name='token'),
    path('graphcall/', views.graphcall, name='graphcall'),
]