from django.urls import path

# import views
from test_app import views

app_name = 'test_app'

urlpatterns = [
    path('list_orders', views.ListOrders.as_view(), name='list_orders'),
    path('detail_order/<int:pk>/', views.DetailOrder.as_view(), name='detail_order'),
    ]
