from django.urls import path
from . import views

app_name	= 'cclog'
urlpatterns = [
	path('log/',					views.log,			name ='log'	  ),
	path('',						views.logs,			name ='logs'  ),
	path('update/',					views.update,		name ='update'),
	path('update-save/<int:pk>',	views.update_save,	name ='update_save'),
	path('reopen/<int:pk>',			views.reopen,		name ='reopen' ),

	path('updatelink/',				views.updatelink,		name ='updatelink'),
]
