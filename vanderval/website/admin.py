from django.contrib import admin
from website.models import Site, UserRecords,Jobs

admin.site.register(Site)
admin.site.register(UserRecords)
admin.site.register(Jobs)