from django.db import models
from django.contrib.auth.models import AbstractUser

class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    COLLEGE_CHOICES = [
        ('COCIS', 'COCIS'),
        ('CEDAT', 'CEDAT'),
        ('CHUSS', 'CHUSS'),
    ]

    INTEREST_CHOICES = [
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Gaming', 'Gaming'),
        ('Movies', 'Movies'),
        ('Tech', 'Tech'),
    ]
    
    bio = models.TextField(blank=True)
    profile_pic = models.CharField(max_length=2083, default=None, null=True, blank=True)
    interests = models.TextField()  # Comma-separated list of interests
    age = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=255)
    college = models.CharField(max_length=10, choices=COLLEGE_CHOICES, null=True, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    def age_bracket(self):
        if self.age is None:
            return None
        if 18 <= self.age <= 19:
            return '18-19'
        elif 20 <= self.age <= 23:
            return '20-23'
        elif 24 <= self.age <= 26:
            return '24-26'
        elif self.age >= 27:
            return '26+'
        return 'Unknown'


    def __str__(self):
        return self.username

