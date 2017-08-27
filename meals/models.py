from django.db import models

class meal(models.Model):
	user = models.ForeignKey('users.user')
	meal = models.CharField(max_length=255)
	calories = models.IntegerField(default=0)
	meal_date = models.DateField()
	meal_time = models.TimeField()
	active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.calories

	def get_fields(self):
		retData = {}
		retData['meal_id'] = str(self._get_pk_val())
		retData['user_id'] = str(self.user_id)
		retData['meal_desc'] = str(self.meal)
		retData['calories'] = str(self.calories)
		retData['meal_date'] = str(self.meal_date)
		retData['meal_time'] = str(self.meal_time)[:-3]
		retData['active'] = str(self.active)
		retData['date_created'] = str(self.date_created)
		retData['date_modified'] = str(self.date_modified)
		
		return retData
