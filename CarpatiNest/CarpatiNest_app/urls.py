from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'CarpatiNest_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='CarpatiNest_app:index'), name='logout'),
    path('register/', views.register, name='register'),
    path('mountains/', views.mountain_selection, name='mountain_selection'),
    path('mountain/<int:mountain_id>/refuges/', views.mountain_refuges, name='mountain_refuges'),
    path('booking/<int:refuge_id>/', views.booking_view, name='booking'),
    path('settings/', views.account_settings, name='account_settings'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
]