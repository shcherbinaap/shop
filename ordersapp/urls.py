from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
	path('', ordersapp.OrderList.as_view(), name='orders'),
	path('order_create/', ordersapp.OrderCreate.as_view(), name='order_create'),
	path('update/<pk>/', ordersapp.OrderUpdate.as_view(), name='order_update'),
	path('delete/<pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
	path('detail/<pk>/', ordersapp.OrderDetail.as_view(), name='order_detail'),
	path('forming/<pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),



]