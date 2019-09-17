from django.contrib import admin
from user.models import Users


class UsersAdmin(admin.ModelAdmin):
    # fields = 
    list_display = ( 'first_name', 'last_name', 'username', 'password', 'id')
    search_fields = ( 'first_name', 'last_name', 'username' )
    

admin.site.register(Users, UsersAdmin)



