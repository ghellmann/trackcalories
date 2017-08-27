from django.db import models
import base64

class user(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	firstname = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)
	calories = models.IntegerField(default=0)
	active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.username
	
	def get_fields(self):
		retData = {}
		retData['user_id'] = str(self._get_pk_val())
		retData['authorization'] = base64.b64encode(str(self.username) + ':' + str(self.password))
		retData['firstname'] = str(self.firstname)
		retData['surname'] = str(self.surname)
		retData['calories'] = str(self.calories)
		retData['active'] = str(self.active)
		retData['date_created'] = str(self.date_created)
		retData['date_modified'] = str(self.date_modified)
		
		try:
			retData['initials'] = str(self.firstname).upper()[0] + str(self.surname).upper()[0]
		except:
			retData['initials'] = ''
			
		return retData
	
