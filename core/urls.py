from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.UZLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("test/", views.test_list, name="test_list"),
    path("test/<int:test_id>/", views.take_test, name="take_test"),
    path("result/<int:attempt_id>/", views.result, name="result"),
    path("rating/", views.leaderboard, name="leaderboard"),
]
