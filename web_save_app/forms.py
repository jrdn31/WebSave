from django import forms

from .models import Transaction, Goal

from django.contrib.auth.models import Group, User


class TransactionForm(forms.ModelForm):
	#form does not accept negative values.
	def __init__(self, *args, **kwargs):
		super(TransactionForm, self).__init__(*args, **kwargs)
		self.fields['amount'].widget.attrs['min'] = .01
		self.fields['amount'].decimal_places = 2

	category = 'save'
	class Meta:
		model = Transaction
		fields = ['note', 'amount', 'user_id']
		labels = {'note': 'Note:', 'amount':'Amount: $',
				 'user_id':'Select User:'}


class SaverForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(SaverForm, self).__init__(*args, **kwargs)
		self.fields['amount'].widget.attrs['max']= -.01
		self.fields['amount'].decimal_places = 2
	
	
	cat_choices = (('spend','Spend'),('give','Give'),('goal','Goal'))
	# active_goals= Goal.objects.filter(is_active = True)
	# goal_choices = Goal.objects.exclude(pk__in=active_goals)
	# goal_id=forms.ChoiceField(choices=goal_choices)
	category = forms.ChoiceField(choices=cat_choices)
	
	class Meta:
		model = Transaction
		fields = ['note', 'amount','user_id', 'goal_id', 'is_goal','category']
		labels = {'note': 'Note:', 'amount':'Amount: $', 'user_id':'Verify ID',
				  'goal_id':'Goal','is_goal?':'Is theis a goal?',
				  'Category':'category'}




class NewGoalForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NewGoalForm, self).__init__(*args, **kwargs)
		self.fields['goal_amount'].widget.attrs['max'] = -.01
		self.fields['goal_amount'].decimal_places = 2

	class Meta:
		model = Goal
		fields = ['name', 'goal_amount', 'user_id']
		labels = {'name': 'Goal Name:', 'goal_amount':'How much do you want to save?:', 'user_id': 'Verify your username:'}