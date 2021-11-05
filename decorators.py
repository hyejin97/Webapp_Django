from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	'''
	logged users see their dashboard as the main page
	'''
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('dashboard')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


# def allowed_users(allowed_roles=[]):
# 	'''user role-based permission'''
# 	def decorator(view_func):
# 		def wrapper_func(request, *args, **kwargs):
# 			group = None

# 			if request.user.groups.exists():
# 				group = request.user.groups.all()[0].name

# 			if group in allowed_roles:
# 				return view_func(request, *args, **kwargs)
# 			else:
# 				return HttpResponse('Permission denied')
# 		return wrapper_func
# 	return decorator

