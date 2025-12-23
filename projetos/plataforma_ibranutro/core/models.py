from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    email_verified = models.BooleanField(default=False)  # <-- ADD

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_url = models.URLField()
    order_index = models.IntegerField(default=0)

    class Meta:
        ordering = ["order_index", "id"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "lesson")

class Document(models.Model):
    CATEGORY_CHOICES = [
        ("APOSTILAS", "Apostilas"),
        ("LIVROS", "Livros"),
        ("ARTIGOS", "Artigos"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    # owner = null => documento global

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)

    file = models.FileField(upload_to="docs/", blank=True, null=True)
    external_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = "GLOBAL" if self.owner_id is None else self.owner.get_username()
        return f"{self.get_category_display()} - {self.title} ({who})"
