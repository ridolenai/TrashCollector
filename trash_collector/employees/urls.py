from django.urls import path
from . import views

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name = "create"),
    path('edit_profile/', views.edit_profile, name = "edit_profile"),
    path('confirm_pickup/<int:id>', views.confirm_pickup, name = "confirm_pickup"),
    path('daily_filter/', views.daily_filter, name = "daily_filter")
]