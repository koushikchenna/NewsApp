from django.contrib import admin

# Register your models here.
from .models import User, hotnews, searchnews, idnews, keyword, mynews, usersettings

admin.site.register(User)
admin.site.register(hotnews)
admin.site.register(searchnews)
admin.site.register(idnews)
admin.site.register(keyword)
admin.site.register(mynews)
admin.site.register(usersettings)