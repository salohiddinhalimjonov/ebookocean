from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserModel


@admin.register(UserModel)
class AddEbookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'country', 'birthday')
    list_filter = ('country',)
    ordering = ('-date_joined',)
