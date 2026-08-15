import random

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RegisterForm
from .models import Test, Attempt, Profile


def home(request):
    profiles = Profile.objects.select_related("user").all()
    leaderboard = sorted(profiles, key=lambda p: p.total_score, reverse=True)[:5]
    tests = Test.objects.filter(is_active=True).select_related("subject")[:6]
    return render(request, "core/home.html", {"leaderboard": leaderboard, "tests": tests})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            auth_login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})


class UZLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


def logout_view(request):
    auth_logout(request)
    return redirect("home")


@login_required
def test_list(request):
    tests = Test.objects.filter(is_active=True).select_related("subject")
    return render(request, "core/test_list.html", {"tests": tests})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, is_active=True)
    questions = list(test.questions.prefetch_related("choices").all())

    # Foydalanuvchining shu test bo'yicha tugallanmagan urinishini topamiz
    # yoki yangisini boshlaymiz (shu bilan sahifa yangilansa ham vaqt hisoblagich davom etadi).
    attempt = (
        Attempt.objects.filter(user=request.user, test=test, completed=False)
        .order_by("-started_at")
        .first()
    )
    if attempt is None or attempt.is_expired:
        if attempt is not None and attempt.is_expired:
            # eski vaqti tugagan urinishni 0 ball bilan yopamiz
            attempt.total = len(questions)
            attempt.completed = True
            attempt.finished_at = timezone.now()
            attempt.save()
        attempt = Attempt.objects.create(user=request.user, test=test, total=len(questions))

    if request.method == "POST":
        if attempt.completed:
            return redirect("result", attempt_id=attempt.id)

        score = 0
        total = len(questions)
        for q in questions:
            selected = request.POST.get(f"question_{q.id}")
            if selected and q.choices.filter(id=selected, is_correct=True).exists():
                score += 1

        attempt.score = score
        attempt.total = total
        attempt.completed = True
        attempt.finished_at = timezone.now()
        attempt.save()
        return redirect("result", attempt_id=attempt.id)

    # Har bir savol uchun javob variantlarini urinish ID'siga bog'liq holda
    # (barqaror, lekin foydalanuvchidan foydalanuvchiga farqli) aralashtiramiz.
    rng = random.Random(f"{attempt.id}")
    prepared_questions = []
    for q in questions:
        choices = list(q.choices.all())
        rng.shuffle(choices)
        prepared_questions.append({"id": q.id, "text": q.text, "choices": choices})

    context = {
        "test": test,
        "questions": prepared_questions,
        "attempt": attempt,
        "deadline_ms": int(attempt.deadline.timestamp() * 1000),
        "server_now_ms": int(timezone.now().timestamp() * 1000),
    }
    return render(request, "core/take_test.html", context)


@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user)
    return render(request, "core/result.html", {"attempt": attempt})


def leaderboard(request):
    profiles = sorted(Profile.objects.select_related("user"), key=lambda p: p.total_score, reverse=True)
    return render(request, "core/leaderboard.html", {"profiles": profiles})
