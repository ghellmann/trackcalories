import re
from users.models import user
from django.conf import settings
import base64

class userObject(object):
	def __init__(self):
		self.user_id = ''
		self.username = ''
		self.password = ''
		self.update_username = ''
		self.update_password = ''
		self.firstname = ''
		self.surname = ''
		self.calories = ''
		self.authorization = ''
		self.update_authorization = ''
		self.status = 404
		
	def __repr__(self):
		return "< class users.controller.userObject() >"
	
	def __str__(self):
		return "< class users.controller.userObject() >"
	
	def set_user_id(self, user_id):
		try:
			self.user_id = int(user_id)
		except:
			self.user_id = 0
	
	def set_authorization(self, authorization):
		self.authorization = base64.b64decode(authorization).split(':')
		
		if len(self.authorization) == 2:
			self.username = self.authorization[0]
			self.password = self.authorization[1]
	
	def set_update_authorization(self, authorization):
		self.authorization = base64.b64decode(authorization).split(':')
		
		if len(self.authorization) == 2:
			self.update_username = self.authorization[0]
			self.update_password = self.authorization[1]
	
	def set_firstname(self, firstname):
		self.firstname = firstname.capitalize().strip()
	
	def set_surname(self, surname):
		self.surname = surname.capitalize().strip()
	
	def set_calories(self, calories):
		try:
			self.calories = int(calories)
		except:
			self.calories = 0
	
	def get_status(self):
		return self.status
	
	def _validate_username(self):
		data = {}
		
		if not re.match(r'^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$', self.username):
			self.status = 422
			data['message'] = 'An invalid email address has been entered'
			
		return data
		
	def _validate_update_username(self):
		data = {}
		
		if not re.match(r'^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$', self.update_username):
			self.status = 422
			data['message'] = 'An invalid email address has been entered'
			
		return data
		
	def _validate_password(self):
		data = {}
		
		if len(self.password) < 6:
			self.status = 422
			data['message'] = 'A password less than 6 characters has been entered'
			
		return data
		
	def _validate_update_password(self):
		data = {}
		
		if len(self.update_password) < 6:
			self.status = 422
			data['message'] = 'A password less than 6 characters has been entered'
			
		return data
		
	def _validate_firstname(self):
		data = {}
		
		if len(self.firstname) < 1:
			self.status = 422
			data['message'] = 'A firstname has not been entered'
			
		return data
		
	def _validate_surname(self):
		data = {}
		
		if len(self.surname) < 1:
			self.status = 422
			data['message'] = 'A surname has not been entered'
			
		return data
		
	def _validate_calories(self):
		data = {}
		
		if self.calories < 1:
			self.status = 422
			data['message'] = 'Calories has not been entered'
			
		return data
	
	def create(self):
		data = {}
		
		try:
			data = self._validate_username()
			
			if len(data) == 0:
				data = self._validate_password()
			
			if len(data) == 0:
				data = self._validate_firstname()
			
			if len(data) == 0:
				data = self._validate_surname()
			
			if len(data) == 0:
				data = self._validate_calories()
			
			if len(data) == 0:
				new_user = user.objects.filter(username=self.username, active=True)
				
				if len(new_user) > 0:
					self.status = 409
					data['message'] = 'Username already exists'
				else:
					new_user = user()
					new_user.username = self.username
					new_user.password = self.password
					new_user.firstname = self.firstname
					new_user.surname = self.surname
					new_user.calories = self.calories
					new_user.save()
					
					self.status = 201
					data['message'] = 'User successfully created'
					data['data'] = new_user.get_fields()
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
	
	def retrieve(self):
		data = {}
		userCollection = {}
		
		try:
			if self.user_id > 0 and len(self.username) > 0 and len(self.password) > 0:
				new_user = user.objects.filter(pk=self.user_id, username=self.username, password=self.password, active=True)
				self.status = 404
				data['message'] = 'Cannot find user'
			elif len(self.username) > 0 and len(self.password) > 0:
				new_user = user.objects.filter(username=self.username, password=self.password, active=True)
				self.status = 404
				data['message'] = 'Incorrect username or password'
			elif self.user_id > 0 and settings.DEBUG:
				new_user = user.objects.filter(pk=self.user_id, active=True)
				self.status = 404
				data['message'] = 'Cannot find user'
			elif settings.DEBUG:
				new_user = user.objects.filter(active=True)
				self.status = 404
				data['message'] = 'Cannot find user'
			else:
				self.status = 404
				data['message'] = 'Cannot find user'
			
			if len(new_user) > 0:
				self.status = 200
				
				for i in xrange(len(new_user)):
					userCollection['user_'+str(i)] = new_user[i].get_fields()
				
				data['message'] = 'User(s) successfully retrieved'
				data['data'] = userCollection
				
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
	
	def update(self):
		data = {}
		
		try:
			data = self._validate_update_username()
			
			if len(data) == 0:
				data = self._validate_update_password()
			
			if len(data) == 0:
				data = self._validate_firstname()
			
			if len(data) == 0:
				data = self._validate_surname()
			
			if len(data) == 0:
				data = self._validate_calories()
			
			if len(data) == 0:
				check_user = user.objects.filter(username=self.update_username, active=True)
				
				if len(check_user) > 0:
					if str(check_user[0].id) != str(self.user_id):
						self.status = 409
						data['message'] = 'Username already exists for another user'
						
						return data
				
				new_user = user.objects.filter(pk=self.user_id, username=self.username, password=self.password, active=True)
				
				if len(new_user) == 0:
					self.status = 404
					data['message'] = 'Cannot find user'
				else:
					new_user[0].username = self.update_username
					new_user[0].password = self.update_password
					new_user[0].firstname = self.firstname
					new_user[0].surname = self.surname
					new_user[0].calories = self.calories
					new_user[0].save()
					
					self.status = 200
					data['message'] = 'User successfully updated'
					data['data'] = new_user[0].get_fields()
		
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
	
	def delete(self):
		data = {}
		
		try:
			new_user = user.objects.filter(pk=self.user_id, username=self.username, password=self.password)
			
			if len(new_user) == 0:
				self.status = 404
				data['message'] = 'Cannot find user'
			else:
				# soft delete
				new_user[0].active = False
				new_user[0].save()
				
				# hard delete
				#new_user[0].delete();
				
				self.status = 200
				data['message'] = 'User successfully deleted'
		
		except:
			self.status = 500
			data['message'] = 'An internal server error occured'
		
		return data
	