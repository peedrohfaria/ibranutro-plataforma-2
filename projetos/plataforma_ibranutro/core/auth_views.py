from django.contrib.auth import views as auth_views
from .forms import VerifiedEmailPasswordResetForm

class VerifiedPasswordResetView(auth_views.PasswordResetView):
    form_class = VerifiedEmailPasswordResetForm
    template_name = "core/password_reset.html"
