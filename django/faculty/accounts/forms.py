
from django import forms
from django.forms import ModelForm
from .models import Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import re, os
from PIL import Image


class UserProfileForm(ModelForm):
	image = forms.ImageField(label='upload a image',
							required=True,widget=forms.FileInput)
	# fields that will hold on to the cropped image
	class Meta:
		model = Profile
		fields = ['image','first_name',
				'last_name','email',
				'number','designation','qualification',
				'department']

	def __init__(self,*args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(UserProfileForm,self).clean()
		first_name = self.cleaned_data.get('first_name')
		email = self.cleaned_data.get('email')


		try:
			validate_email(email)
		except:
			raise forms.ValidationError('Not a valid email address!')

		if Profile.objects.filter(first_name = first_name).exists():
			raise forms.ValidationError('Profile with that firstname already'
									' exists!')

	def save(self,user, commit=True):
		profile = super(UserProfileForm,self).save(commit=False)
		profile.user = user
		profile.save()
		cleaned_data = super(UserProfileForm,self).clean()

		image = self.cleaned_data.get('image')

		new_image = Image.open(settings.MEDIA_ROOT+'avatars/'+image.name)
		cropped_image = new_image
		resized_image = cropped_image.resize((600, 400), Image.ANTIALIAS)
		# remove the old image before saving new one
		resized_image.save(settings.MEDIA_ROOT+'avatars/'+image.name)
		return profile

class EditProfilepicForm(forms.ModelForm):
	image = forms.ImageField(label='Choose a new image',
							 required=True, widget=forms.FileInput)

	class Meta:
		model = Profile
		fields = ['image']

	def __init__(self,*args, **kwargs):
		super(EditProfilepicForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(EditProfilepicForm, self).clean()

	def save(self,user, commit=True):
		profile = super(EditProfilepicForm,self).save(commit=False)
		profile.user = user
		profile.save()
		cleaned_data = super(EditProfilepicForm,self).clean()

		image = self.cleaned_data.get('image')

		new_image = Image.open(settings.MEDIA_ROOT+'avatars/'+image.name)
		cropped_image = new_image
		resized_image = cropped_image.resize((600, 400), Image.ANTIALIAS)
		# remove the old image before saving new one
		resized_image.save(settings.MEDIA_ROOT+'avatars/'+image.name)
		return profile

class EditProfileForm(forms.ModelForm):

	# fields that will hold on to the cropped image
	class Meta:
		model = Profile
		fields = ['first_name',
				  'last_name', 'email',
				  'number', 'designation', 'qualification',
				  'department']

	def __init__(self,*args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(EditProfileForm,self).clean()
		email = self.cleaned_data.get('email')
		bio = self.cleaned_data.get('bio')


		try:
			validate_email(email)
		except:
			raise forms.ValidationError('Not a valid email address!')


	def save(self,user, commit=True):
		profile = super(EditProfileForm,self).save(commit=False)
		profile.user = user
		profile.save()
		return profile




#check if a string has upper and lower case
def check_upper_and_lower(mystring):
	"""this method check to see if the
	passed in string has upper and lowercase
	characters"""

	upper = []
	lower = []
	upper = [l for l  in mystring if l.isupper()]
	lower = [l for l in mystring if l.islower()]
	if not upper:
		raise ValidationError('Password must contain upper and lower case!')

def has_numbers(mystring):
	"""this method checks to see if the passed in string has
	numbers in it """

	if not any(i.isdigit() for i in mystring):
		raise ValidationError('password must contain one or more numbers!')

def no_special_chracters(mystring):
	"""this method checks to see if the passed in string has special
	characters in it """

	if "@" in mystring or "#" in mystring or "$" in mystring:
		pass
	else:
		raise ValidationError('password must contain special characters')


class ChangePasswordForm(forms.Form):

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(ChangePasswordForm,self).__init__(*args,**kwargs)

	current_password = forms.CharField(label='current password', max_length= 20 ,
	 									widget= forms.PasswordInput)
	new_password = forms.CharField(label='new password',
										widget= forms.PasswordInput(
											attrs={'id':'new_password'}
											),
										validators=[check_upper_and_lower,
										has_numbers,no_special_chracters],
										help_text='password must be 14 charcters'
										' or more, contain upper and lower case,'
										' should not contain your username or'
										' full name and contain special characters'
										' like @ # $ ')
	confirm_password = forms.CharField(label='confirm password', max_length= 20 ,
	 									widget= forms.PasswordInput)

	def clean_current_password(self):
		current_password = self.cleaned_data['current_password']
		if not self.user.check_password(current_password):
			raise forms.ValidationError('Your current password is incorrect!')
		return current_password

	def clean_confirm_password(self):
		confirm_password = self.cleaned_data['confirm_password']
		new_password = self.cleaned_data.get('new_password')
		if new_password != confirm_password:
			raise forms.ValidationError('Your new password does not match the confirm')
		return confirm_password

	def clean_new_password(self):
		current_password = self.cleaned_data.get('current_password')
		new_password = self.cleaned_data.get('new_password')
		#if len(new_password)< 14:
		#	raise forms.ValidationError("Password should be "
		#								"14 charcters or more")
		if re.search(r'\b{}\b'.format(self.user.username),new_password):
			raise forms.ValidationError('Your password cannot contain your username!')
		if re.search(r'\b{}\b'.format(self.user.profile.get().first_name),new_password):
			raise forms.ValidationError("Your password cannot contain your firstname")
		if current_password== new_password:
			raise forms.ValidationError('Your new password cannot be the same as'
										' as the old one!')
		return new_password