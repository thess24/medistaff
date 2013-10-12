from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User, AbstractUser
from django import forms
import datetime
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm



class System(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500)

	def __unicode__(self):
		return unicode(self.name)

class Hospital(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500)
	system = models.ForeignKey(System)

	def __unicode__(self):
		return unicode(self.name)

class Unit(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500)
	system = models.ForeignKey(System)
	hospital = models.ForeignKey(Hospital)
	fullslug = models.SlugField(max_length=500)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return unicode(self.name) 

class Workday(models.Model):
	name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	start = models.DateTimeField()
	end = models.DateTimeField()
	hours = models.DecimalField(max_digits=10,decimal_places=2)
	system = models.ForeignKey(System)
	hospital = models.ForeignKey(Hospital)
	unit = models.ForeignKey(Unit)
	position = models.CharField(max_length=500)
	manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='workday_manager')
	accepted = models.BooleanField()
	openmarket = models.BooleanField()
	description = models.TextField(blank=True)


	def hoursworked(self):
		return self.end-self.start

	def __unicode__(self):
		return unicode(self.name)

class HoursAvailable(models.Model):
	worker = models.ForeignKey(settings.AUTH_USER_MODEL)
	start = models.DateTimeField()
	end = models.DateTimeField()


##################		

# user model extension -- basically userprofile is the new user
class UserProfile(AbstractUser):
	mobile = models.CharField(max_length=10, blank=True, null=True)
	jobtype = models.CharField(max_length=100)
	position = models.CharField(max_length=100)
	wage = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
	homehospital = models.ForeignKey(Hospital,null=True)
	homeunit = models.ForeignKey(Unit,null=True)
	homesystem = models.ForeignKey(System,null=True)
	about = models.TextField(blank=True)

	recievemail = models.BooleanField()
	recievetext = models.BooleanField()
	# add other settings as booleans and add to settings html file

	def __unicode__(self):
		return self.last_name + ", " + self.first_name

##################		

class CensusInfo(models.Model):
	hospital = models.ForeignKey(Hospital)
	unit = models.ForeignKey(Unit)
	system = models.ForeignKey(System)
	census = models.IntegerField()
	time = models.DateTimeField()

	def __unicode__(self):
		return unicode(self.hospital)

class BudgetInfo(models.Model):
	hospital = models.ForeignKey(Hospital)
	unit = models.ForeignKey(Unit)
	system = models.ForeignKey(System)
	budget = models.IntegerField()
	date = models.DateField()

	def __unicode__(self):
		return unicode(self.hospital)


# FORMS

class WorkdayForm(ModelForm):
	class Meta:
		model=Workday
		fields=['name', 'start', 'end']

	def clean(self):
		cleaned_data = super(WorkdayForm, self).clean()
		start = cleaned_data.get("start")
		end = cleaned_data.get("end")
		if end < start: raise forms.ValidationError("You cant't get off work before you start!")
		if end == start: raise forms.ValidationError("You need to work at least a little!")
		return cleaned_data

	def __init__(self, unit, *args, **kwargs):
		super (WorkdayForm,self).__init__(*args,**kwargs)
		self.fields['name'].queryset = UserProfile.objects.filter(groups__name=unit.fullslug)

class AddOpenShiftForm(ModelForm):
	class Meta:
		model = Workday
		fields = ['start', 'end']

class HospitalForm(ModelForm):
	class Meta:
		model=Hospital
		fields=['name']

class UnitForm(ModelForm):
	class Meta:
		model=Unit
		fields=['name']

class BudgetForm(ModelForm):
	class Meta:
		model=BudgetInfo
		fields=['unit', 'budget', 'date']

class CensusForm(ModelForm):
	class Meta:
		model=CensusInfo
		fields=['unit' ,'census', 'time']

class UnitCensusForm(ModelForm):
	class Meta:
		model=CensusInfo
		fields=['census', 'time']

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['first_name','last_name','email','mobile','jobtype','homehospital','homeunit','about']

class OpenShiftForm(ModelForm):
	class Meta:
		model=Workday
		fields= []

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    position = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100)
    companySize = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    email = forms.EmailField()

class DateFilterForm(forms.Form):
	filterstart = forms.DateTimeField()
	filterend = forms.DateTimeField()


