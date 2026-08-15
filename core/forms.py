from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Test, Question, Choice


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class TestAdminForm(forms.ModelForm):
    """Admin panelda test yaratish/tahrirlash formasi (vaqtni soatda tekshiradi)."""

    class Meta:
        model = Test
        fields = ("title", "subject", "duration_hours", "is_active")

    def clean_duration_hours(self):
        hours = self.cleaned_data["duration_hours"]
        if hours <= 0:
            raise ValidationError("Vaqt 0 soatdan katta bo'lishi kerak.")
        return hours


class QuestionAdminForm(forms.ModelForm):
    """Admin panelda savol qo'shish/tahrirlash formasi."""

    class Meta:
        model = Question
        fields = ("test", "text", "order")

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise ValidationError("Savol matni bo'sh bo'lmasligi kerak.")
        return text


class ChoiceAdminForm(forms.ModelForm):
    """Admin panelda javob varianti qo'shish/tahrirlash formasi."""

    class Meta:
        model = Choice
        fields = ("question", "text", "is_correct")

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise ValidationError("Javob matni bo'sh bo'lmasligi kerak.")
        return text
