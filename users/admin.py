from django.contrib import admin
from users.models import EmailVerificationToken

admin.site.register(EmailVerificationToken)