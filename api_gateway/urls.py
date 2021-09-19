from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.hello_world, name='index'),
    path('api/account/', views.AccountCreateVIew.as_view(), name='account'),
    path('api/orders/', views.OrdersView.as_view(), name='orders'),
    path('api/orders/<str:pk>/', views.OrderDetailView.as_view(), name='order_detail'),


]
