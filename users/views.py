from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from users.controller import userObject
import json

def index(request, user_id='0'):
	if not request.is_ajax() and not settings.DEBUG:
		return render(request, '404.html')
	
	data = {}
	user = userObject()
	user.set_authorization(request.META.get('HTTP_AUTHORIZATION',''))
	user.set_update_authorization(request.META.get('HTTP_UPDATE_AUTHORIZATION',''))
	
	if request.method == 'POST':
		user.set_user_id(request.POST.get('user_id', user_id))
		user.set_firstname(request.POST.get('firstname', ''))
		user.set_surname(request.POST.get('surname', ''))
		user.set_calories(request.POST.get('calories', '0'))
		
		data = user.create()
		
	elif request.method == 'GET':
		user.set_user_id(request.GET.get('user_id', user_id))
		
		data = user.retrieve()
		
	elif request.method == 'PUT':
		user.set_user_id(request.PUT.get('user_id', user_id))
		user.set_firstname(request.PUT.get('firstname', ''))
		user.set_surname(request.PUT.get('surname', ''))
		user.set_calories(request.PUT.get('calories', '0'))
		
		data = user.update()
		
	elif request.method == 'DELETE':
		user.set_user_id(request.DELETE.get('user_id', user_id))
		
		data = user.delete()
		
	return HttpResponse(json.dumps(data), content_type = "application/json", status=user.get_status())



