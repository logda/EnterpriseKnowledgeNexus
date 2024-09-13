from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

# ... 其余代码保持不变 ...
from .models import Document


class DocumentAdmin(ModelAdmin):
    model = Document
    menu_label = "Documents"  # ditch this to use verbose_name_plural from model
    menu_icon = "doc-full"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ("title", "category", "created_by", "created_at", "updated_at")
    list_filter = ("category", "created_by")
    search_fields = ("title", "content")


modeladmin_register(DocumentAdmin)
