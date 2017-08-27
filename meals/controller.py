from meals.models import meal
from users.models import user
from django.conf import settings
import datetime
import base64

class mealObject(object):
	def __init__(self):
		self.username = ''
		self.password = ''
		self.meal_id = ''
		self.user_id = ''
		self.meal_desc = ''
		self.calories = ''
		self.meal_date = ''
		self.meal_date_from = ''
		self.meal_date_to = ''
		self.meal_time = ''
		self.meal_time_from = ''
		self.meal_time_to = ''
		self.status = 404
		
	def __repr__(self):
		return "< class meals.controller.mealObject() >"
	
	def __str__(self):
		return "< class meals.controller.mealObject() >"
	
	def set_authorization(self, authorization):
		self.authorization = base64.b64decode(authorization).split(':')
		
		if len(self.authorization) == 2:
			self.username = self.authorization[0]
			self.password = self.authorization[1]
	
	def set_meal_id(self, meal_id):
		try:
			self.meal_id = int(meal_id)
		except:
			self.meal_id = 0
	
	def set_user_id(self, user_id):
		try:
			self.user_id = int(user_id)
		except:
			self.user_id = 0
	
	def set_meal_desc(self, meal_desc):
		self.meal_desc = meal_desc.capitalize().strip()
	
	def set_calories(self, calories):
		try:
			self.calories = int(calories)
		except:
			self.calories = 0
	
	def set_meal_date(self, meal_date):
		self.meal_date = meal_date.replace('/','-')

	def set_meal_date_from(self, meal_date_from):
		self.meal_date_from = meal_date_from.replace('/','-')
		
	def set_meal_date_to(self, meal_date_to):
		self.meal_date_to = meal_date_to.replace('/','-')
		
	def set_meal_time(self, meal_time):
		self.meal_time = meal_time
		
	def set_meal_time_from(self, meal_time_from):
		self.meal_time_from = meal_time_from
		
	def set_meal_time_to(self, meal_time_to):
		self.meal_time_to = meal_time_to
		
	def get_status(self):
		return self.status
	
	def _validate_user_id(self):
		data = {}
		
		if self.user_id < 1:
			self.status = 422
			data['message'] = 'User has not been entered'
			
		return data
	
	def _validate_meal_desc(self):
		data = {}
		
		if len(self.meal_desc) < 1:
			self.status = 422
			data['message'] = 'A meal description has not been entered'
			
		return data
	
	def _validate_calories(self):
		data = {}
		
		if self.calories < 1:
			self.status = 422
			data['message'] = 'Calories has not been entered'
			
		return data
	
	def _validate_meal_date(self):
		data = {}
		
		try:
			datetime.datetime.strptime(self.meal_date, '%Y-%m-%d')
		except ValueError:
			self.status = 422
			data['message'] = 'Meal date has not been entered or is not in the format YYYY-MM-DD'
			
		return data
	
	def _validate_meal_date_from_to(self):
		data = {}
		
		if len(self.meal_date_from) == 0 or len(self.meal_date_to) == 0:
			self.status = 422
			data['message'] = 'Both Meal date from and Meal date to needs to be captured'
			
		if len(data) == 0:
			try:
				datetime.datetime.strptime(self.meal_date_from, '%Y-%m-%d')
			except ValueError:
				self.status = 422
				data['message'] = 'Meal date from is not in the format YYYY-MM-DD'
		
		if len(data) == 0:
			try:
				datetime.datetime.strptime(self.meal_date_to, '%Y-%m-%d')
			except ValueError:
				self.status = 422
				data['message'] = 'Meal date to is not in the format YYYY-MM-DD'
				
			return data
				
		return data
		
	def _validate_meal_time(self):
		data = {}
		
		try:
			datetime.datetime.strptime(self.meal_time, '%H:%M')
		except ValueError:
			self.status = 422
			data['message'] = 'Meal time has not been entered or is not in the format HH:MM'
			
		return data
	
	def _validate_meal_time_from_to(self):
		data = {}
		
		if len(self.meal_time_from) == 0 or len(self.meal_time_to) == 0:
			self.status = 422
			data['message'] = 'Both Meal time from and Meal time to needs to be captured'
			
		if len(data) == 0:
			try:
				datetime.datetime.strptime(self.meal_time_from, '%H:%M')
			except ValueError:
				self.status = 422
				data['message'] = 'Meal time from is not in the format HH:MM'
		
		if len(data) == 0:
			try:
				datetime.datetime.strptime(self.meal_time_to, '%H:%M')
			except ValueError:
				self.status = 422
				data['message'] = 'Meal time to is not in the format HH:MM'
				
		return data
	
	def _validate_user(self):
		data = {}
		new_user = user.objects.filter(pk=self.user_id, username=self.username, password=self.password, active=True)
		
		if len(new_user) == 0:
			self.status = 401
			data['message'] = 'Authentication Falied'
		
		return data
	
	def create(self):
		data = {}
		
		try:
			data = self._validate_user()
			
			if len(data) == 0:
				data = self._validate_meal_desc()
			
			if len(data) == 0:
				data = self._validate_calories()
			
			if len(data) == 0:
				data = self._validate_meal_date()
			
			if len(data) == 0:
				data = self._validate_meal_time()
			
			if len(data) == 0:
				new_meal = meal()
				new_meal.user_id = self.user_id	
				new_meal.meal = self.meal_desc
				new_meal.calories = self.calories
				new_meal.meal_date = self.meal_date
				new_meal.meal_time = self.meal_time
				new_meal.save()
				
				self.status = 201
				data['data'] = new_meal.get_fields()
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
		
	def retrieve(self):
		data = {}
		mealCollection = {}
		
		try:
			if not settings.DEBUG:
				data = self._validate_user()
			
			if len(data) == 0 and (len(self.meal_date_from) > 0 or len(self.meal_date_to) > 0):
				data = self._validate_meal_date_from_to()
				
			if len(data) == 0 and (len(self.meal_time_from) > 0 or len(self.meal_time_to) > 0):
				data = self._validate_meal_time_from_to()
			
			if len(data) == 0:
				if self.meal_id > 0:
					new_meal = meal.objects.filter(pk=self.meal_id, active=True).order_by('user', 'active', '-meal_date', '-meal_time', 'calories', '-date_modified')
					self.status = 404
					data['message'] = 'Cannot find meal'
				elif self.user_id > 0:
					new_meal = meal.objects.filter(user_id=self.user_id, active=True).order_by('user', 'active', '-meal_date', '-meal_time', 'calories', '-date_modified')
					self.status = 404
					data['message'] = 'Cannot find meals'
				else:
					new_meal = meal.objects.filter(active=True).order_by('user', 'active', '-meal_date', '-meal_time', 'calories', '-date_modified')
				
				if len(self.meal_date_from) > 0:
					new_meal = new_meal.filter(meal_date__range=[self.meal_date_from, self.meal_date_to]).order_by('user', 'active', '-meal_date', '-meal_time', 'calories', '-date_modified')
					
				if len(self.meal_time_from) > 0:
					new_meal = new_meal.filter(meal_time__range=[self.meal_time_from, self.meal_time_to]).order_by('user', 'active', '-meal_date', '-meal_time', 'calories', '-date_modified')
				
				if len(new_meal) > 0:
					self.status = 200
					
					for i in xrange(len(new_meal)):
						mealCollection['meal_'+str(i)] = new_meal[i].get_fields()
					
					data['message'] = 'Meal(s) successfully retrieved'
					data['data'] = mealCollection

		except:
			self.status = 500
			data['message'] = 'An internal server error occured'

		return data
	
	def update(self):
		data = {}
		
		try:
			data = self._validate_user()
			
			if len(data) == 0:
				data = self._validate_user_id()
			
			if len(data) == 0:
				self._validate_meal_desc()
			
			if len(data) == 0:
				self._validate_calories()
				
			if len(data) == 0:
				self._validate_meal_date()
				
			if len(data) == 0:
				self._validate_meal_time()
				
			if len(data) == 0:
				new_meal = meal.objects.filter(pk=self.meal_id, active=True)
				
				if len(new_meal) == 0:
					self.status = 404
					data['message'] = 'Cannot find meal'
				else:
					new_meal[0].user_id = self.user_id
					new_meal[0].meal = self.meal_desc
					new_meal[0].calories = self.calories
					new_meal[0].meal_date = self.meal_date
					new_meal[0].meal_time = self.meal_time
					new_meal[0].save()
					
					self.status = 200
					data['message'] = 'Meal successfully updated'
					data['data'] = new_meal[0].get_fields()
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
		
	def delete(self):
		data = {}
		
		try:
			data = self._validate_user()
			
			if len(data) == 0:
				new_meal = meal.objects.filter(pk=self.meal_id)
				
				if len(new_meal) == 0:
					self.status = 404
					data['message'] = 'Cannot find meal'
				else:
					# soft delete
					new_meal[0].active = False
					new_meal[0].save()
					
					# hard delete
					#new_meal[0].delete();
					
					self.status = 200
					data['message'] = 'Meal successfully deleted'
		
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'

		return data
		
	