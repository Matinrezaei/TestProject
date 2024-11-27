from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'is_staff', 'is_superuser')
    search_fields = ('phone_number', 'email')
    ordering = ('phone_number',)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(Account, AccountAdmin)