from django.urls import path
from . import views

app_name	= 'ie'
urlpatterns = [
	path('upload/',			views.upload,		name='upload'  ),
	path('download/log/',	views.download_log,	name='download_log')
]
