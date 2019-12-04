"""Define URLS for web_save_app"""
from django.urls import path, include

from . import views

app_name = 'web_save_app'

urlpatterns= [
#	Home Page
	path('', views.index, name='index'),
	#URLS for Login/Logout
	path('', include('django.contrib.auth.urls')),

	#Saver Page
	path('saver/',views.saver,name='saver'),

	#Banker page
	path('banker/',views.banker,name='banker'),

	#Banker Transaction page
	path('new_transaction/',views.new_transaction,name='new_transaction'),

	#Saver page to add Goal
	path('new_goal/',views.new_goal,name='new_goal'),

	#Saver page to view summary
	path('saver_summary/',views.saver_summary, name='saver_summary'),
	#Saver Transaction page
	path('saver_transaction/',views.saver_transaction, name='saver_transaction'),

	#Landing page to redirect user based on group
	path('landing/',views.landing, name='landing'),

	#Saver view for each saver
	path('saver_info/<int:user_id>/',views.saver_info, name='saver_info'),

	#Page for editing transactions
	path('edit_transaction/<int:transaction_id>/',views.edit_transaction, name = 'edit_transaction'),
	
	#Page for editing goals
	path('edit_goal/<int:goal_id>/',views.edit_goal, name = 'edit_goal'),
]