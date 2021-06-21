from django.contrib import admin
from UserApp.models import *

admin.site.register(UserProfile)
admin.site.register(Services)
admin.site.register(Orders)
admin.site.register(Locations)
admin.site.register(ServiceProviders)
admin.site.register(Dummy)
admin.site.register(Category)
admin.site.register(PasswordReset)
# Register your models here.
