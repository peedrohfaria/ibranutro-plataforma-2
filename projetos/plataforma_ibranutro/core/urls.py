from django.urls import path
from django.contrib.auth import views as auth_views
from .auth_views import VerifiedPasswordResetView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),

    path("profile/", views.profile_view, name="profile"),
    path("docs/", views.docs_view, name="docs"),

    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path(
        "password-reset/",
        VerifiedPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="core/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    path("docs/new/", views.doc_create, name="doc_create"),
path("docs/<int:doc_id>/edit/", views.doc_edit, name="doc_edit"),
path("docs/<int:doc_id>/delete/", views.doc_delete, name="doc_delete"),

]
