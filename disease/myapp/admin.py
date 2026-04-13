from django.contrib import admin
from .models import User, Profile, Medical, Ment

model_list = [User, Profile, Medical, Ment]

for model in model_list:
    admin.site.register(model)