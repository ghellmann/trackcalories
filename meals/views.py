from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from meals.controller import mealObject
import json

def index(request, meal_id='0'):
	if not request.is_ajax() and not settings.DEBUG:
		return render(request, '404.html')
	
	data = {}
	meal = mealObject()
	meal.set_authorization(request.META.get('HTTP_AUTHORIZATION',''))
	
	if request.method == 'POST':
		meal.set_meal_id(request.POST.get('meal_id', meal_id))
		meal.set_user_id(request.POST.get('user_id', ''))
		meal.set_meal_desc(request.POST.get('meal_desc', ''))
		meal.set_calories(request.POST.get('calories', ''))
		meal.set_meal_date(request.POST.get('meal_date', ''))
		meal.set_meal_time(request.POST.get('meal_time', ''))
		
		data = meal.create()
		
	elif request.method == 'GET':
		meal.set_meal_id(request.GET.get('meal_id', meal_id))
		meal.set_user_id(request.GET.get('user_id', ''))
		meal.set_meal_date_from(request.GET.get('meal_date_from', ''))
		meal.set_meal_date_to(request.GET.get('meal_date_to', ''))
		meal.set_meal_time_from(request.GET.get('meal_time_from', ''))
		meal.set_meal_time_to(request.GET.get('meal_time_to', ''))
		
		data = meal.retrieve()
		
	elif request.method == 'PUT':
		meal.set_meal_id(request.PUT.get('meal_id', meal_id))
		meal.set_user_id(request.PUT.get('user_id', ''))
		meal.set_meal_desc(request.PUT.get('meal_desc', ''))
		meal.set_calories(request.PUT.get('calories', ''))
		meal.set_meal_date(request.PUT.get('meal_date', ''))
		meal.set_meal_time(request.PUT.get('meal_time', ''))
		
		data = meal.update()
		
	elif request.method == 'DELETE':
		meal.set_meal_id(request.DELETE.get('meal_id', meal_id))
		meal.set_user_id(request.DELETE.get('user_id', ''))
		
		data = meal.delete()
		
	return HttpResponse(json.dumps(data), content_type = "application/json", status=meal.get_status())
