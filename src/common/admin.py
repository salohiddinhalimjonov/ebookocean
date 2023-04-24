from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AddEbookModel, BlogModel, CommentModel


@admin.register(AddEbookModel)
class AddEbookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ebook_title', 'email', 'checked', 'created_at', 'updated_at')
    list_filter = ('checked',)
    ordering = ('created_at',)


@admin.register(BlogModel)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'views_count', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('created_at',)

@admin.register(CommentModel)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ebook', 'rate')
    search_fields = ('ebook',)
    ordering = ('created_at',)