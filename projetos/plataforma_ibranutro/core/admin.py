from django.contrib import admin
from .models import Profile, Course, Lesson, LessonProgress, Document

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order_index")
    list_filter = ("course",)

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed", "completed_at")
    list_filter = ("completed",)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "owner", "created_at")
    list_filter = ("category",)
