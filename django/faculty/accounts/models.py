from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class ProfileManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(ProfileManager, self).filter(approved=True)


class Profile(models.Model):
	DEP_CHOICE = (
		('Computer Science Engineering', 'Computer Science Engineering'),
		('Electronics and Communication Engineering', 'Electronics and Communication Engineering'),
	)

	user = models.ForeignKey(User,related_name='profile')
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	number = models.CharField(max_length=13, default='91-')
	designation = models.CharField(max_length=30, default='Professor')
	qualification = models.CharField(max_length=30, default='Phd.')
	department = models.CharField(max_length=50, choices=DEP_CHOICE, default='CSE')
	image = models.ImageField(upload_to='avatars/',
							height_field="height_field",
							width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	approved = models.BooleanField(default=False)

	objects = ProfileManager()

	class Meta:
		ordering = ['id']

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)