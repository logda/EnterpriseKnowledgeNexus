from django.contrib import admin
from .models import Category, Document, UserPermission

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "path")
    search_fields = ("name", "path")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_by", "created_at", "updated_at")
    list_filter = ("category", "created_by")
    search_fields = ("title", "content")


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "permission_type")
    list_filter = ("permission_type",)
    search_fields = ("user__username", "category__name")
