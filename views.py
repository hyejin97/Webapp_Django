from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import AddTagForm, AddExpForm, CreateUserForm
from .decorators import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db import IntegrityError
import json, time

# Create your views here.
@unauthenticated_user
def home(request):
	return render(request, 'myenglishmate/index.html')


@login_required(login_url='login')
def dashboard(request):
	totalnum = Expression.objects.filter(user=request.user).count()
	now = datetime.today()
	completed = Expression.objects.filter(user=request.user, completed=True).count()
	completed_pct = 0
	if totalnum != 0:
		completed_pct = int(completed / totalnum * 100)

	data_points = []
	labels = []
	for i in range(7):
		date = datetime.today() - timedelta(days=i)
		js_date = int(time.mktime(date.timetuple())) * 1000
		recent_data = Expression.objects.filter(date_created__year=date.year, date_created__month=date.month, date_created__day=date.day).all().count()
		labels.append(js_date)
		data_points.append(recent_data)
		
	context = {'username': request.user.username, 'total': totalnum, 'completed': completed_pct, 'labels': labels, 'data_points':data_points}
	return render(request, 'myenglishmate/dashboard.html', context)


@login_required(login_url='login')
def create(request):
	if request.method == 'POST':
		if 'english' in request.POST and 'korean' in request.POST:
			form = AddExpForm(request.user, request.POST)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.user = request.user
				obj.save()
			
		elif 'tagname' in request.POST:
			form = AddTagForm(request.POST)
			if form.is_valid():
				try:
					obj = form.save(commit=False)
					obj.user = request.user
					obj.save()
				except IntegrityError as e:
					if 'UNIQUE constraint' in str(e.args):
						redirect('addnew')

	expform = AddExpForm(request.user)
	context = {'form': expform}
	
	return render(request, 'myenglishmate/add.html', context)


@login_required(login_url='login')
def edit(request, pk):
	exp = Expression.objects.filter(user=request.user).get(id=pk)
	form = AddExpForm(request.user, instance=exp)

	if request.method == 'POST':
		form = AddExpForm(request.user, request.POST, instance=exp) #take exp instance and save that as the instance
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()

		return redirect('dashboard')

	context = {'form': form, 'item':exp}
	return render(request, 'myenglishmate/edit.html', context)


@login_required(login_url='login')
def delete(request, pk):
	exp = Expression.objects.filter(user=request.user).get(id=pk)
	if request.method == 'POST':
		exp.delete()
		return redirect('dashboard')


@login_required(login_url='login')
def search(request):
	if request.method == 'POST':
		query = request.POST.get('kor_or_eng', None)
		if query:
			eng = Expression.objects.filter(user=request.user, english__contains=query)
			kor = Expression.objects.filter(user=request.user, korean__contains=query)
			if eng:
				context = {'results' : eng}
			elif kor:
				context = {'results' : kor}
			else:
				context = {'results' : 'NOTFOUND'}
			return render(request, 'myenglishmate/search.html', context)

	results = Expression.objects.filter(user=request.user).all()
	context = {'results' : results}
	return render(request, 'myenglishmate/search.html', context)


@login_required(login_url='login')
def quiz(request):
	data = Expression.objects.filter(user=request.user)
	errormsg = None
	if len(data) == 0:
		errormsg = "no expression added to the database yet"

	include_all = 1
	if request.method == 'POST':
		query = request.POST.get("completedonly", None)
		if query == 'true':
			include_all = 0
		return redirect('startquiz', 0, 0, include_all)

	context = {'error' : errormsg}
	return render(request, 'myenglishmate/quiz.html', context)


@login_required(login_url='login')
def start_quiz(request, i, is_flipped, include_all):
	uncompleted_data = Expression.objects.filter(user=request.user, completed=False)
	data = Expression.objects.filter(user=request.user)

	if include_all == 1: #mode1 : "include all" 
		#error handling
		errormsg = None
		if i == len(data): #if reached end
			errormsg = "Congrats! You finished the quiz.\n (Remaining incomplete expressions : " + str(len(uncompleted_data)) + ")"
			context = {'error' : errormsg}
			return render(request, 'myenglishmate/startquiz.html', context)

		#don't show prev button on the first card
		underzero = False
		if i <= 0:
			underzero = True

		#update checkbox(whether completed)
		if request.method == 'POST':
			query = request.POST.get("completed", None)
			print(query)
			if query is None:
				Expression.objects.filter(user=request.user, pk=data[i].pk).update(completed = False)
			else:
				Expression.objects.filter(user=request.user, pk=data[i].pk).update(completed = True)

		curr_data = Expression.objects.filter(user=request.user)[i]
		context = {'error' : errormsg, 'data' : curr_data, 'index' : i, 'underzero' : underzero, 'is_flipped' : is_flipped, 'include_all' : include_all}
		return render(request, 'myenglishmate/startquiz.html', context)

	else: #mode2 : only include incomplete data

		#error handling
		errormsg = None
		if len(uncompleted_data) == 0:
			errormsg = "Congrats! You completed learning all the registered expressions"
			context = {'error' : errormsg}
			return render(request, 'myenglishmate/startquiz.html', context)
		else:
			if i == len(data):
				errormsg = "Congrats! You finished the quiz.\n (Remaining incomplete expressions : " + str(len(uncompleted_data)) + ")"
				context = {'error' : errormsg}
				return render(request, 'myenglishmate/startquiz.html', context)

			underzero = False
			if i <= 0:
				underzero = True

			#only uncompleted mode -> don't show completed data
			if data[i].completed:
				return redirect('increment', i, is_flipped, include_all)
			else:
				if request.method == 'POST':
					query = request.POST.get("completed", None)
					if query is None:
						Expression.objects.filter(user=request.user, pk=data[i].pk).update(completed = False)
					else:
						Expression.objects.filter(user=request.user, pk=data[i].pk).update(completed = True)

				curr_data = Expression.objects.filter(user=request.user)[i]
				context = {'error' : errormsg, 'data' : curr_data, 'index' : i, 'underzero' : underzero, 'is_flipped' : is_flipped, 'include_all' : include_all}
				return render(request, 'myenglishmate/startquiz.html', context)




def flipcard(request, i, is_flipped, include_all):
	if is_flipped == 1:
		is_flipped = 0
	else:
		is_flipped = 1

	return redirect('startquiz', i, is_flipped, include_all)

def increment(request, i, is_flipped, include_all):
	i = i + 1
	is_flipped = 0
	return redirect('startquiz', i, is_flipped, include_all)

def decrement(request, i, is_flipped, include_all):			
	i = i - 1
	is_flipped = 0
	return redirect('startquiz', i, is_flipped, include_all)

@unauthenticated_user
def do_login(request):
	if request.method == "POST":
		user_name = request.POST.get('username', None)
		user_pw = request.POST.get('password', None)
			
		user = authenticate(request, username=user_name, password=user_pw)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			print(user_name, user_pw)
			messages.info(request, 'Username or password is incorrect')

	context = {}
	return render(request, 'myenglishmate/login.html', context)


@login_required(login_url='login')
def logout_user(request):
	logout(request)
	return redirect('login')


@unauthenticated_user
def register(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('login')

	context = {'form':form}		
	return render(request, 'myenglishmate/register.html', context)