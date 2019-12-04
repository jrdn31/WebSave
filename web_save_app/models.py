from django.db import models
from django.contrib.auth.models import User, Group
from model_utils import Choices
# Create your models here.

class Goal(models.Model):
	"""A class that holds goal information"""
	name = models.CharField(max_length=80)
	date_added = models.DateTimeField(auto_now_add=True)
	user_id = models.ForeignKey(User,on_delete = models.CASCADE)
	goal_amount = models.DecimalField(max_digits = 10, decimal_places = 2)
	is_active = models.BooleanField(default = True)
	#determines which goals belong to which saver
	
	#When called Goal returns name
	def __str__(self): return self.name


	def Goal_Met(self, amount):
		if self.goal_amount >= amount:
			return True
		else:
			return False
			# Return excess?


class Transaction(models.Model):
	"""A class that stores and organizes individual transactions"""

	cat_choices = Choices('save','spend','give','goal')


	amount = models.DecimalField(max_digits = 10, decimal_places= 2)
	note = models.CharField(max_length=80)
	date_added = models.DateTimeField(auto_now_add=True)
	user_id = models.ForeignKey(User,on_delete = models.CASCADE)
	is_goal = models.BooleanField(default = False)
	goal_id = models.ForeignKey(Goal,on_delete= models.CASCADE, blank= True, null= True)
	category = models.CharField(max_length=20, choices = cat_choices, default = cat_choices.save)




