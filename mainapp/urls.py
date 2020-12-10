from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
	path('', mainapp.products, name='products'),
	path('pk', mainapp.products, name='products'),
]
