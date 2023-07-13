from django.contrib import admin
from .models import *

admin.site.register(UserAccount)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(ProjectTeam)
admin.site.register(OrganizationObject)
admin.site.register(DataPoint)

admin.site.register(TimeSeries)
admin.site.register(Configuration)
