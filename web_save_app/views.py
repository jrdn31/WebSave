from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum


from .models import Transaction, Goal
from .forms import TransactionForm,NewGoalForm, SaverForm
# Create your views here.





	
def logout(request):
	"""Logs user out of website"""
	logout(request)

def check_group(user_var):
	"""pass in user to find their group"""
	user = user_var
	if user.groups.filter(name='Banker').exists():
		return "banker"
	else:
		return "saver"

def index(request):
	"""Home page for web_save_app"""
	user_var = request.user
	group=check_group(user_var)
	context = {'group':group}
	return render(request,'web_save_app/index.html',context)

@login_required
def landing(request):
	"""Displays links based on user group."""
	
	if request.user.groups.filter(name='Banker').exists():
	 	return redirect('web_save_app:banker')
	else:
	 	return redirect('web_save_app:saver')

def none_equals_0(check_value):
	"""checks for non decimal values"""
	if check_value is None:
		return 0
	else:
		return check_value

def account_balance(user):
	user_transactions = Transaction.objects.filter(user_id= user)
	_total_saved = list(user_transactions.filter(category='save').aggregate(Sum('amount')).values())[0]
	_total_given = list(user_transactions.filter(category='give').aggregate(Sum('amount')).values())[0]
	_total_spent = list(user_transactions.filter(category='spend').aggregate(Sum('amount')).values())[0]
	_total_goal = list(user_transactions.filter(category='goal').aggregate(Sum('amount')).values())[0]
	total_saved = none_equals_0(_total_saved)
	total_given = none_equals_0(_total_given)
	total_spent = none_equals_0(_total_spent)
	total_goal = none_equals_0(_total_goal)

	account_balance = total_saved+total_given-total_spent-total_goal
	return account_balance

@login_required
def saver(request):
	"""Saver's saving and goal information lives here"""

	#collect transaction data for user and total

	user_transactions = Transaction.objects.filter(user_id=request.user)
	_total_saved = list(user_transactions.filter(category='save').aggregate(Sum('amount')).values())[0]
	_total_given = list(user_transactions.filter(category='give').aggregate(Sum('amount')).values())[0]
	_total_spent = list(user_transactions.filter(category='spend').aggregate(Sum('amount')).values())[0]
	_total_goal = list(user_transactions.filter(category='goal').aggregate(Sum('amount')).values())[0]
	total_saved = none_equals_0(_total_saved)
	total_given = none_equals_0(_total_given)
	total_spent = none_equals_0(_total_spent)
	total_goal = none_equals_0(_total_goal)

	account_balance = total_saved+total_given+total_spent+total_goal

	goal_list = Goal.objects.filter(user_id = request.user)
	goal_transactions = Transaction.objects.filter(user_id =request.user).filter(category = 'goal')
	goal_summary = {}
	goal_amount_list = {}
	for goal in goal_list:
		total = list(goal_transactions.filter(goal_id=goal.id).aggregate(Sum('amount')).values())[0]
		if total != None:
			goal_summary.update({goal.name:total})
			goal_amount_list.update({goal.name:goal.goal_amount})			
		else:
			goal_summary.update({goal.name: 0})
			goal_amount_list.update({goal.name: 0})	


	context= {'total_saved': total_saved, 'total_given':total_given, 'total_spent': total_spent,
	 'account_balance':account_balance, 'total_goal':total_goal, 'goal_summary':goal_summary, 'goal_amount_list':goal_amount_list,}
	return render(request, 'web_save_app/saver.html',context)

@login_required
def saver_summary(request):
	"""saver view web page"""
	transactions = Transaction.objects.filter(user_id=request.user).order_by('-date_added')
	context = {'transactions': transactions}
	return render(request, 'web_save_app/saver_summary.html', context)

@login_required
def banker(request):
	"""banker view web page"""
	user_balance={}
	saver=User.objects.filter(groups = 2)
	#Create a table for user balances
	for user in saver:
		user_balance.update({user.username:account_balance(user.id)})

	

	transactions = Transaction.objects.order_by('user_id','date_added')
	context = {'transactions': transactions, 'user_balance':user_balance, 'saver':saver}
	return render(request, 'web_save_app/banker.html', context)

@login_required
def saver_info(request,user_id):
	"""view individual saver data"""
	user = User.objects.get(id=user_id)
	transactions = Transaction.objects.filter(user_id=user).order_by('-date_added')
	
	context = {'transactions': transactions, 'user':user}
	return render(request, 'web_save_app/saver_info.html', context)


@login_required
def new_transaction(request):
	"""add Transaction entry using form"""

	if request.method != 'POST':
		#No data submtited; create a blank form.
		form = TransactionForm()
	else:
		#POST data submitted; process data.
		form = TransactionForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('web_save_app:banker')
	#Display a blank or invalid form.
	context={'form':form}
	return render(request,'web_save_app/new_transaction.html',context)

@login_required
def edit_transaction(request, transaction_id):
	"""edit Transaction entry using form"""
	transaction = Transaction.objects.get(id=transaction_id)

	if request.method != 'POST':
		#No data submtited; prefill form with data from requested transaction
		form = TransactionForm(instance=transaction)
	else:
		#POST data submitted; process data.
		form = TransactionForm(instance=transaction,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('web_save_app:banker')
	#Display a blank or invalid form.
	context={'form':form}
	return render(request,'web_save_app/new_transaction.html',context)

@login_required
def saver_transaction(request):
	"""add User Transaction entry using form"""

	if request.method != 'POST':
		#No data submtited; create a blank form.
		form = SaverForm()
	else:
		#POST data submitted; process data.
		form = SaverForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('web_save_app:saver')
	#Display a blank or invalid form.
	context={'form':form}
	return render(request,'web_save_app/saver_transaction.html',context)


@login_required	
def new_goal(request):
	"""add Transaction entry using form"""
	goals=Goal.objects.filter(user_id=request.user).filter(is_active = True)

	if request.method != 'POST':
		#No data submtited; create a blank form.
		form = NewGoalForm()
		# Display active goals
		
	else:
		#POST data submitted; process data.
		form = NewGoalForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('web_save_app:saver')
	#Display a blank or invalid form.
	context={'goals':goals,'form':form}
	return render(request,'web_save_app/new_goal.html',context)

@login_required	
def edit_goal(request, goal_id):
	"""add Transaction entry using form"""
	goal = Goal.objects.filter(id=goal_id)

	if request.method != 'POST':
		#No data submtited; create a blank form.
		form = NewGoalForm(instance=goal)
		# Display active goals
		
	else:
		#POST data submitted; process data.
		form = NewGoalForm(instance=goal,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('web_save_app:new_goal')
	#Display a blank or invalid form.
	context={'form':form}
	return render(request,'web_save_app/new_goal.html',context)

