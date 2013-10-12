from django.contrib import admin
from main.models import Workday, Hospital, Unit, System, CensusInfo, BudgetInfo, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class WorkdayAdmin(admin.ModelAdmin):
	list_display = ('name', 'start', 'end', 'hoursworked', 'hospital', 'unit')

class UnitAdmin(admin.ModelAdmin):
	list_display = ('name', 'hospital', 'system')



# makes the nex UserProfile appear as if it were user in admin
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile

class MyUserCreationForm(UserCreationForm):
    def clean_username(self):
	    username = self.cleaned_data["username"]
	    try:
	        UserProfile._default_manager.get(username=username)
	    except UserProfile.DoesNotExist:
	        return username
	    raise forms.ValidationError(
	        self.error_messages['duplicate_username'],
	        code='duplicate_username',
	    )

    class Meta(UserCreationForm.Meta):
        model = UserProfile

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile','jobtype', 'position', 'wage','picture', 'about', 'recievemail', 'recievetext', 'homehospital','homeunit','homesystem')}),
    )


admin.site.register(Workday, WorkdayAdmin)
admin.site.register(Hospital)
admin.site.register(Unit, UnitAdmin)
admin.site.register(System)
admin.site.register(CensusInfo)
admin.site.register(BudgetInfo)
# admin.site.register(UserProfile)
admin.site.register(UserProfile, MyUserAdmin)









 