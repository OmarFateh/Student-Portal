from django.contrib import admin

from .models import Category, Course, Grade


class CategoryAdmin(admin.ModelAdmin):
    """
    Override the category admin and customize the categories display.
    """
    prepopulated_fields = {"slug": ("title",)}

    # class Meta:
    #     model = Category


# models admin site registeration 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course)
admin.site.register(Grade)