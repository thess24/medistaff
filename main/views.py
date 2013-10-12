# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.utils import timezone  #for dates on submit
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from main.models import ContactForm, Workday, System, Hospital, Unit, WorkdayForm, HospitalForm, UnitForm, BudgetForm, CensusForm, UnitCensusForm, BudgetInfo, CensusInfo, UserProfile, UserProfileForm, OpenShiftForm, DateFilterForm, AddOpenShiftForm
from django.db.models import Avg, Count, Sum, Max
import datetime
from django.template.defaultfilters import slugify
from postman.api import pm_write

# advocate-healthcare-advocate-christ-medical-center-palliative-care
# https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_absolute_url


# TESTS
def profilecomplete(user):
	# returns true if profile filled out--used in decorator
	if not user.homehospital: return False
	if not user.homeunit: return False
	if not user.jobtype: return False
	if not user.mobile: return False
	if not user.first_name: return False
	if not user.last_name: return False
	return True



def correctsystem(request, systempass):
	system = System.objects.get(slug__iexact=systempass)
	if not str(system.name) == str(request.user.homesystem): raise Http404
	# instead of 404 redirect to error page that explains
	pass

def startercontext(request):
	# gets units, hospitals and system and returns context
	sysslug = slugify(request.user.homesystem)
	system = System.objects.get(slug__iexact=sysslug)
	allhospitals = Hospital.objects.filter(system=system)
	allunits = Unit.objects.filter(system=system)
	context= {'allhospitals':allhospitals, 'allunits':allunits, 'system':system}
	return system, context


# VIEWS 
def index(request):
	if request.user:
		userinfo = UserProfile.objects.get(id=request.user.id)
		context = { 'userinfo':userinfo }
	else: context = {}
	return render(request, 'main/index.html', context)

def about(request):
	if request.user:
		userinfo = UserProfile.objects.get(id=request.user.id)
		context = { 'userinfo':userinfo }
	else: context = {}
	return render(request, 'main/about.html', context)

def benefits(request):
	if request.user:
		userinfo = UserProfile.objects.get(id=request.user.id)
		context = { 'userinfo':userinfo }
	else: context = {}
	return render(request, 'main/benefits.html', context)

def contact(request):
	form = ContactForm()
	if request.user:
		userinfo = UserProfile.objects.get(id=request.user.id)
		context = { 'userinfo':userinfo, 'form':form }
	else: context = {'form':form }

	return render(request, 'main/contact.html', context)

def home(request, systempass):
	
	workday = Workday.objects.filter(system__slug__iexact=systempass, name=request.user)  #might not be unique if by name...should do by id

	context = {'workday':workday}

	return render(request, 'main/home.html', context)

def profile(request, systempass, username):
	# system, context = startercontext(request)
	units = Unit.objects.filter(system__slug__iexact=systempass)
	groups = request.user.groups.values_list('name',flat=True)
	userdata = get_object_or_404(UserProfile, username= username)

	if request.method =='POST':
		if 'userforminfo' in request.POST:
			changeform = UserProfileForm(request.POST, instance=userdata)
			if changeform.is_valid():
				instance = changeform.save(commit=False)
				instance.save()

				# adds you to homeunit group on form update
				groupname = instance.homeunit.fullslug
				g = Group.objects.get(name=groupname)
				g.userprofile_set.add(request.user)
	else:
		changeform = UserProfileForm(instance= userdata) 
	context = {'units':units, 'groups':groups, 'userdata': userdata, 'changeform': changeform}
	# context.update(contextadd)
	return render(request, 'main/profile.html', context)


def settings(request, systempass):
	# system, context = startercontext(request)
	units = Unit.objects.filter(system__slug__iexact=systempass)
	groups = request.user.groups.values_list('name',flat=True)
	userdata = UserProfile.objects.get(id=request.user.id)

	if request.method =='POST':
		if 'groupsubscribe' in request.POST:
			changeform = UserProfileForm(instance= userdata)
			groupname = request.POST['group']
			g = Group.objects.get(name=groupname)
			if request.user in g.userprofile_set.all(): # userprofile_set bc of userprofile instead of user
				g.userprofile_set.remove(request.user)
			else: g.userprofile_set.add(request.user)

		elif 'userforminfo' in request.POST:
			changeform = UserProfileForm(request.POST, instance=userdata)
			if changeform.is_valid():
				instance = changeform.save(commit=False)
				instance.save()

				# adds you to homeunit group on form update
				groupname = instance.homeunit.fullslug
				g = Group.objects.get(name=groupname)
				g.userprofile_set.add(request.user)
	else:
		changeform = UserProfileForm(instance= userdata) 
	context = {'units':units, 'groups':groups, 'userdata': userdata, 'changeform': changeform}
	# context.update(contextadd)
	return render(request, 'main/settings.html', context)

def systemsettings(request, systempass):
	system, context = startercontext(request)
	return render(request, 'main/systemsettings.html', context)

def openshift(request, systempass):
	# system, context = startercontext(request)
	workday = Workday.objects.filter(system__slug__iexact=systempass, openmarket=True)

	if request.method =='POST':
		if 'grab' in request.POST:
			workdayid = request.POST['id']
			workdaydata = Workday.objects.get(id=workdayid)
			form = OpenShiftForm(request.POST,instance=workdaydata)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.name = request.user
				instance.accepted = True
				instance.openmarket = False
				instance.save()

				pm_write(
		            sender=instance.name,
		            recipient=instance.manager,
		            subject='Shift Grabbed for %s!' % instance.start,
		            body='The shift was grabbed by %s %s.  Phone: %s ' %(request.user.first_name, request.user.last_name, request.user.mobile)
		            )

	else:
		form = OpenShiftForm()
	context = {'workday':workday, 'form':form}
	# context.update(contextadd)
	return render(request, 'main/openshift.html', context)

def systemoverview(request, systempass):
	context={}
	return render(request, 'main/systemoverview.html', context)

@user_passes_test(profilecomplete, login_url='badprofile')
def hospital(request, systempass, hospitalpass):
	# system, context = startercontext(request)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	units = Unit.objects.filter(hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass)
	workers = Workday.objects.filter(hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass,start__lte=datetime.datetime.now(),end__gte=datetime.datetime.now()).count()

	context = {'hospital':hospital,'units':units, 'workers': workers}
	# context.update(contextadd)
	return render(request, 'main/hospital.html', context)

def unit(request, systempass, hospitalpass, unitpass):
	# system, context = startercontext(request)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	unit = Unit.objects.get(slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass)

	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

	# workers today, workers now, workers not now, num workers now
	workday = Workday.objects.filter(hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass, unit__slug__iexact=unitpass,start__range=(today_min, today_max))
	workdaynow = workday.filter(start__lte=datetime.datetime.now(),end__gte=datetime.datetime.now())
	workdaylater = workday.exclude(start__lte=datetime.datetime.now(),end__gte=datetime.datetime.now())
	workers = workdaynow.count()
	hourstoday = Workday.objects.filter(start__range=(today_min, today_max)).aggregate(totalhours=Sum('hours'))

	try: 
		censusinfo = CensusInfo.objects.filter(system__slug__iexact=systempass, hospital=hospital, unit=unit).order_by('time')
		lastcensus = censusinfo.latest('time')
	except CensusInfo.DoesNotExist: 
		censusinfo = None
		lastcensus = None

	context = {'hospital':hospital, 'unit':unit, 'workers':workers, 'censusinfo':censusinfo, 'lastcensus':lastcensus, 'hourstoday':hourstoday, 'workdaynow':workdaynow, 'workdaylater':workdaylater}
	# context.update(contextadd)
	return render(request, 'main/unit.html', context)

def inputdates(request, systempass):

	context = {}
	return render(request, 'main/inputdates.html', context)
	

def nursefilter(request, systempass):
	# system, context = startercontext(request)

	if request.method =='GET':
		pass

	userlist = UserProfile.objects.all()

	context = {'userlist':userlist}
	# context.update(contextadd)
	return render(request, 'main/nursefilter.html', context)


def openshiftindex(request, systempass):

	context = {}
	return render(request, 'main/addopenshiftindex.html', context)

def addopenshift(request, systempass, hospitalpass, unitpass):
	system = System.objects.get(slug__iexact=systempass)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	unit = Unit.objects.get(slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass)
	workday = Workday.objects.filter(system__slug__iexact=systempass,unit__slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, openmarket=True, start__gte=datetime.datetime.now())
	if request.method =='POST':
		if 'add' in request.POST:
			form=AddOpenShiftForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.unit = unit
				instance.name = None
				instance.manager = request.user
				instance.hospital = hospital
				instance.start = form.cleaned_data['start']
				instance.end = form.cleaned_data['end']
				timediff = instance.end - instance.start
				instance.hours = timediff.seconds/float(3600)
				instance.system = system
				instance.openmarket = True
				instance.save()
		if 'delete' in request.POST:
			form=AddOpenShiftForm()	
			w = Workday.objects.get(id=request.POST['id'])
			w.delete()

	else:
		form=AddOpenShiftForm()	
	context = {'hospital':hospital, 'unit':unit, 'workday': workday, 'form':form}
	# context.update(contextadd)
	return render(request, 'main/addopenshift.html', context)


def schedule(request, systempass, hospitalpass, unitpass):
	# system, context = startercontext(request)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	unit = Unit.objects.get(slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass)
	userinfo = UserProfile.objects.filter(groups__name=unit.fullslug).annotate(sumhours = Sum('workday__hours'))
	datefilterform = DateFilterForm()

	enddate = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	startdate = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=7), datetime.time.min)


	if request.method =='POST':
		if 'delete' in request.POST:
			workform = WorkdayForm(unit)
			w = Workday.objects.get(id=request.POST['id'])
			w.delete()

		if 'doneopenshift' in request.POST:
			workform = WorkdayForm(unit)
			workdayid = request.POST['id']
			workdaydata = Workday.objects.get(id=workdayid)
			form = OpenShiftForm(request.POST,instance=workdaydata)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.openmarket = True
				instance.name = None
				instance.save()

		elif 'add' in request.POST:
			workform=WorkdayForm(unit,request.POST)
			if workform.is_valid():
				instance = workform.save(commit=False)
				instance.unit = unit
				instance.manager=request.user
				instance.hospital = hospital
				instance.start = workform.cleaned_data['start']
				instance.end = workform.cleaned_data['end']
				timediff = instance.end - instance.start
				instance.hours = timediff.seconds/float(3600)
				instance.system = system
				instance.save()

		elif 'newopenshift' in request.POST:
			workform=WorkdayForm(unit,request.POST)
			if workform.is_valid():
				instance = workform.save(commit=False)
				instance.unit = unit
				instance.name = None
				instance.manager = request.user
				instance.hospital = hospital
				instance.start = workform.cleaned_data['start']
				instance.end = workform.cleaned_data['end']
				timediff = instance.end - instance.start
				instance.hours = timediff.seconds/float(3600)
				instance.system = system
				instance.openmarket = True
				instance.save()

		workday = Workday.objects.filter(unit__slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass, start__range=(startdate, enddate))


	if request.method =='GET':
		workform = WorkdayForm(unit)

		if request.GET.get('filterstart'):
			startdate = request.GET.get('filterstart')
		if request.GET.get('filterend'):
			enddate = request.GET.get('filterend')

		workday = Workday.objects.filter(unit__slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass, start__range=(startdate, enddate))
		

	context = {'workday':workday, 'workform':workform, 'hospital':hospital, 'unit':unit, 'userinfo':userinfo, 'datefilterform':datefilterform, 'startdate': startdate, 'enddate':enddate}
	# context.update(contextadd)
	return render(request, 'main/schedule.html', context)

def addhospital(request,systempass):
	whattoadd = 'Hospital'
	system = System.objects.get(slug__iexact=systempass)
	submitted = False
	if request.method =='POST':
		form = HospitalForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.slug = slugify(instance.name) 
			instance.system = system
			instance.save()
			submitted = True
	else:
		form = HospitalForm()
	context = {"form":form, 'whattoadd': whattoadd, 'system': system, 'submitted': submitted}
	return render(request, 'main/addhospital.html', context)

def addunit(request,systempass, hospitalpass):
	whattoadd = 'Unit'
	# system, context = startercontext(request)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	units = Unit.objects.filter(system__slug__iexact=systempass, hospital__slug__iexact=hospitalpass)
	if request.method =='POST':
		form = UnitForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.slug = slugify(instance.name) 
			instance.system = system
			instance.hospital = hospital
			instance.fullslug = slugify(system.name +"-"+ hospital.name +"-"+ instance.name)
			instance.save()

			Group.objects.create(name=instance.fullslug)

	else:
		form = UnitForm()
	contextadd = {"form":form, 'whattoadd': whattoadd, 'hospital':hospital, 'units':units}
	# context.update(contextadd)
	return render(request, 'main/addhospital.html', context)


def addcensus(request, systempass, hospitalpass):
	system = System.objects.get(slug__iexact=systempass)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	census = CensusInfo.objects.filter(system__slug__iexact=systempass, hospital__slug__iexact=hospitalpass)

	if request.method =='POST':
		if 'add' in request.POST:
			form = CensusForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = system
				instance.hospital = hospital
				instance.save()
		elif 'delete' in request.POST:
			form = CensusForm()
			c = CensusInfo.objects.get(id=request.POST['id'])
			c.delete()

	else:
		form = CensusForm()

	context = {"form":form, 'system': system, 'census': census}
	return render(request, 'main/addcensus.html', context)

def addunitcensus(request, systempass, hospitalpass, unitpass):
	system = System.objects.get(slug__iexact=systempass)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	unit = Unit.objects.get(slug__iexact=unitpass,hospital__slug__iexact=hospitalpass, system__slug__iexact=systempass)

	census = CensusInfo.objects.filter(system__slug__iexact=systempass, hospital__slug__iexact=hospitalpass, unit=unit)

	if request.method =='POST':
		if 'add' in request.POST:
			form = UnitCensusForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = system
				instance.unit = unit
				instance.hospital = hospital
				instance.save()
		elif 'delete' in request.POST:
			form = UnitCensusForm()
			c = CensusInfo.objects.get(id=request.POST['id'])
			c.delete()

	else:
		form = UnitCensusForm()

	context = {"form":form, 'system': system, 'census': census}
	return render(request, 'main/addcensus.html', context)

def addbudget(request, systempass, hospitalpass):
	system = System.objects.get(slug__iexact=systempass)
	hospital = Hospital.objects.get(slug__iexact=hospitalpass, system__slug__iexact=systempass)
	budgets = BudgetInfo.objects.filter(system=system, hospital=hospital)

	if request.method =='POST':
		form = BudgetForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.system = system
			instance.hospital = hospital
			instance.save()

	else:
		form = BudgetForm()

	context = {"form":form, 'system': system, 'budgets': budgets}
	return render(request, 'main/addbudget.html', context)

def badprofile(request):
	if request.user:
		userinfo = UserProfile.objects.get(id=request.user.id)
		context = { 'userinfo':userinfo }
	else: context = {}
	return render(request, 'main/baduserprofile.html', context)








	
# # TOOLS
# def preprocess(request, coursename, quarter):
# 	coursename =coursename.lower()
# 	try: coursepass = Course.objects.get(name__iexact=coursename)
# 	except: raise Http404
# 	groups = request.user.groups.values_list('name',flat=True)
# 	if coursename not in groups: raise Http404
# 	latestquarter = coursepass.latestquarter
# 	if int(quarter)>int(latestquarter): raise Http404
# 	try: submits = Submit.objects.get(quarter=quarter,team=request.user,course=coursepass)
# 	except: submits = {}
# 	return coursename, coursepass, submits

 
# # VIEWS 
# def index(request):
# 	groups = request.user.groups.values_list('name',flat=True)
# 	context = {"groups":groups}
# 	return render(request, 'main/index.html', context)

# @login_required
# def createcourse(request):
# 	if request.method =="POST":
# 		form = CourseForm(request.POST)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
#  			instance.teacher = request.user
#  			instance.latestquarter = 1
#  			instance.name = instance.name.lower()
#  			instance.save()
#  			Group.objects.create(name=instance.name.lower())
# 			adduser = request.user
# 			g = Group.objects.get(name=instance.name.lower())
# 			g.user_set.add(adduser)

# 	context = {"CourseForm":CourseForm}
# 	return render(request, 'main/createcourse.html', context)

# def choosecourse(request):
# 	groups = request.user.groups.values_list('name',flat=True)
# 	# for teacher filter by teacher name
# 	context = {'groups':groups}
# 	return render(request, 'main/choosecourse.html', context)

# def coursehomepage(request, coursename):
# 	coursename = coursename.lower()
# 	try:
# 		group = Group.objects.get(name=coursename)
# 		users = group.user_set.all()
# 		course = Course.objects.get(name=coursename)
# 	except:
# 		raise Http404

# 	context = {'users':users, 'group':group, 'course':course}
# 	return render(request, 'main/coursehomepage.html', context)


# def product(request, coursename, quarter):
# 	coursename, coursepass, submits = preprocess(request,coursename,quarter)
# 	currentpage= 'product'

# 	products = Product.objects.filter(team=request.user, course=coursepass)
# 	allproducts = Product.objects.filter(course=coursepass)

# 	s, created = Submit.objects.get_or_create(quarter=quarter,team=request.user,course=coursepass)
# 	s.product = True
# 	s.save()

# 	context = {"quarter":quarter, 'coursename':coursename, 'currentpage': currentpage, 'products':products, 'allproducts':allproducts, 'submits':submits}
# 	return render(request, 'main/product.html', context)


# def productnew(request, coursename, quarter):
# 	coursename, coursepass, submits = preprocess(request,coursename,quarter)
# 	currentpage= 'product'

# 	context = {"quarter":quarter, 'coursename':coursename, 'currentpage': currentpage, 'submits':submits}
# 	context['ProductForm'] = ProductForm

#  	if request.method =='POST':
#  		try: form =ProductForm(request.POST)
#  		except: form = ProductForm(request.POST)

#  		if form.is_valid(): 
#  			instance = form.save(commit=False)
#  			instance.team = request.user
#  			instance.course = coursepass
#  			instance.quarter = int(quarter)
#  			instance.save()
#  			return HttpResponseRedirect(reverse('main.views.product', args=(coursename, quarter)))

#  		context['errors'] = form.errors
#  		return render(request, 'main/product-newmodel.html', context)

# 	return render(request, 'main/product-newmodel.html', context)

# 