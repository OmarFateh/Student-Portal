from django.contrib import admin

from .models import Quiz, QuizQuestion, QuizAnswer, Attempt


# class CategoryAdmin(admin.ModelAdmin):
#     """
#     Override the category admin and customize the categories display.
#     """
#     prepopulated_fields = {"slug": ("title",)}

#     # class Meta:
#     #     model = Category


# models admin site registeration 
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(Attempt)