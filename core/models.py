from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def total_score(self):
        return self.user.attempts.filter(completed=True).aggregate(s=Sum("score"))["s"] or 0


class Subject(models.Model):
    name = models.CharField("Fan nomi", max_length=120)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField("Test nomi", max_length=200)
    subject = models.ForeignKey(Subject, verbose_name="Fan", on_delete=models.CASCADE, related_name="tests")
    duration_hours = models.DecimalField(
        "Vaqt (soat)", max_digits=4, decimal_places=2, default=1,
        help_text="Masalan 1 soat uchun 1, 30 daqiqa uchun 0.5 kiriting."
    )
    is_active = models.BooleanField("Faol", default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def duration_minutes(self):
        return int(float(self.duration_hours) * 60)


class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name="Test", on_delete=models.CASCADE, related_name="questions")
    text = models.TextField("Savol matni")
    order = models.PositiveIntegerField("Tartib raqami", default=0)

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name="Savol", on_delete=models.CASCADE, related_name="choices")
    text = models.CharField("Javob varianti", max_length=300)
    is_correct = models.BooleanField("To'g'ri javobmi?", default=False)

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        return self.text


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Urinish"
        verbose_name_plural = "Urinishlar"
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.score}/{self.total})"

    @property
    def deadline(self):
        from datetime import timedelta
        return self.started_at + timedelta(minutes=self.test.duration_minutes)

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() >= self.deadline
