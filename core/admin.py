from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Profile, Subject, Test, Question, Choice, Attempt
from .forms import TestAdminForm, QuestionAdminForm, ChoiceAdminForm


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    """Har bir savolda faqat bitta to'g'ri javob bo'lishini majburlaydi."""

    def clean(self):
        super().clean()
        correct_count = 0
        filled_count = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            data = form.cleaned_data
            if not data or data.get("DELETE"):
                continue
            if data.get("text"):
                filled_count += 1
                if data.get("is_correct"):
                    correct_count += 1
        if filled_count and correct_count == 0:
            raise ValidationError("Har bir savolda kamida bitta to'g'ri javob belgilanishi shart.")
        if correct_count > 1:
            raise ValidationError("Bir savolda faqat bitta to'g'ri javob bo'lishi mumkin.")


class ChoiceInline(admin.TabularInline):
    model = Choice
    form = ChoiceAdminForm
    formset = ChoiceInlineFormSet
    extra = 4
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ("text", "test", "order")
    list_filter = ("test",)
    inlines = [ChoiceInline]


class QuestionInline(admin.StackedInline):
    model = Question
    form = QuestionAdminForm
    extra = 1
    show_change_link = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    list_display = ("title", "subject", "duration_hours", "is_active", "question_count", "created_at")
    list_filter = ("subject", "is_active")
    search_fields = ("title",)
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "score", "total", "completed", "started_at")
    list_filter = ("test", "completed")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
