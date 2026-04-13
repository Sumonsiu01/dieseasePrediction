from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # AUTH
    path('register/', views.patient_register, name='register'),
    path('login/', views.login, name='login'),
    path('reg_user/', views.reg_user, name='reg_user'),
    path('logout/', views.patient_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/password/', views.change_password, name='change_password'),

    # DASHBOARD
    path('patient/', views.patient_home, name='patient_home'),

    # 🔥 MAIN PREDICTION FLOW (ONLY ONE ENTRY POINT)
    path('prediction/', views.prediction_view, name='predict'),

    # OPTIONAL: direct result page (NOT REQUIRED)
    # path('result/', views.result, name='result'),
]