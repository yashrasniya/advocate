from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'mobile')}),
        ('Personal info', {'fields':
            (
                'first_name', 'last_name','address','gender','birth_date','wallet_balance')}),
        ('Permissions', {'fields': ('is_admin',)}),
        # ('Connection', {'fields': ('connection', 'block')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'first_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('mobile','email')
    ordering = ('mobile', 'id','email')
    filter_horizontal = ()