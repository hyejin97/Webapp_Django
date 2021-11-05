from django.forms import ModelForm, ModelMultipleChoiceField, CharField, Textarea
from .models import Expression, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django import forms

class AddTagForm(ModelForm):
	class Meta:
		model = Tag
		fields = ['tagname']
		constraints = [
        	UniqueConstraint(fields=['tagname', 'user'], name='unique tagname per user')
    	]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class AddExpForm(ModelForm):
	userset = None

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		userset = Tag.objects.filter(user=user)
		self.fields['tags'].autocomplete = False
		self.fields['tags'].queryset = userset

	korean = CharField(max_length=500, widget=Textarea)
	english = CharField(max_length=500, widget=Textarea)
	english.widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1", 'rows': '3', 'placeholder': "Put an expression"})
	korean.widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1", 'rows': '3', 'placeholder': "Put the meaning of expression"})
	tags = ModelMultipleChoiceField(queryset=userset, required = False)

	class Meta:
		model = Expression
		fields = ['korean', 'english', 'tags']
