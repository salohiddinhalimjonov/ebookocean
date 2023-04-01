from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.options import TabularInline
from .models import EbookModel, CategoryModel, EbookFavouritesModel



@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(EbookFavouritesModel)
class EbookFavouritesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ebook', 'favourite')


@admin.register(EbookModel)
class EbookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'authors', 'views_count', 'downloads_count', 'created_at', 'updated_at')
    search_fields = ('title', 'authors')
    ordering = ('views_count', 'downloads_count')

