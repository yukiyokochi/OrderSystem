from django.urls import path
from .views import MenuList, MenuDetail
from . import views

app_name = 'ec'

urlpatterns = [
    path('', MenuList.as_view(), name='menu_list'),
    path('detail/<int:pk>/', MenuDetail.as_view(), name='menu_detail'),
    path('location-register/', views.location_register, name='location_register'),
]
