from django.conf import settings
from main.models import System, Hospital, Unit
from django.template.defaultfilters import slugify





def systemstarterkit(request):
    sysslug = slugify(request.user.homesystem)
    system = System.objects.get(slug__iexact=sysslug)
    allhospitals = Hospital.objects.filter(system=system)
    allunits = Unit.objects.filter(system=system)
    return {'allhospitals':allhospitals, 'allunits':allunits, 'system':system}