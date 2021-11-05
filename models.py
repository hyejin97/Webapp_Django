from django.db import models
from django.contrib.auth.models import User
# build database
# Create your models here.

class Tag(models.Model):
	tagname = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.tagname

	class Meta:
		unique_together = ("user", "tagname")

class Expression(models.Model):
	'''korean - english - explanation in korean(nuance) - example - tags'''
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	korean = models.CharField(max_length=500) #null=True : null will not cause an error
	english = models.CharField(max_length=500)
	date_created = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.english

