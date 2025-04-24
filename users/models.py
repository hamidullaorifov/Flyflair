from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import hashlib
import hmac
import time
import os
from dotenv import load_dotenv

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_token(self):
        """Used to generate email token"""
        load_dotenv()
        timestamp = int(time.time())
        token_data = f"{self.user.pk}-{timestamp}".encode("utf-8")
        secret_key = os.getenv("SECRET_KEY")
        token = hmac.new(secret_key.encode("utf-8"), token_data, hashlib.sha256).hexdigest()
        self.token = token
        self.is_verified = False
        self.save()

    def is_token_valid(self):
        """Check if token is expired or not"""
        if timezone.now() - self.created_at < timedelta(minutes=60):
            return True
        return False

