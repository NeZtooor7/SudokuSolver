from django.urls import path
from .services.main_service import home, action_form

urlpatterns = [
    path("", home, name="home"),
    path("action/", action_form, name="action"),
]
