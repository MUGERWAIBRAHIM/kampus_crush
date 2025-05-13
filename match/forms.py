from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser, Interest
from django.core.mail import send_mail
import random

class CustomSignupForm(SignupForm):
    age = forms.IntegerField(min_value=18)
    college = forms.ChoiceField(choices=CustomUser.COLLEGE_CHOICES)
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@students.mak.ac.ug'):
            raise forms.ValidationError("Please use your @students.mak.ac.ug email.")
        return email

    def save(self, request):
        user = super().save(request)
        user.age = self.cleaned_data['age']
        user.college = self.cleaned_data['college']

        # Set verification
        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.is_active = False  # temporarily deactivate
        user.save()
        user.interests.set(self.cleaned_data['interests'])

        request.session['pending_user_id'] = user.id  # Store for verification

        send_mail(
            subject="Kampus Crush Email Verification",
            message=f"Hello {user.username},\n\nYour verification code is: {code}",
            from_email="no-reply@kampuscrush.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user
