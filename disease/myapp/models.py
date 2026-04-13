# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# ------------------------
# Custom User Model
# ------------------------
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username


# ------------------------
# Medical Records
# ------------------------
class Medical(models.Model):
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    medicine = models.CharField(max_length=200)
    patient = models.ForeignKey(User, related_name="medical_patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="medical_doctor", on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease


# ------------------------
# Mentorship / Appointment
# ------------------------
class Ment(models.Model):
    approved = models.BooleanField(default=False)
    time = models.CharField(max_length=200, null=True, blank=True)
    patient = models.ForeignKey(User, related_name="ment_patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="ment_doctor", on_delete=models.CASCADE, null=True, blank=True)
    ment_day = models.DateTimeField(null=True, blank=True)
    medical = models.ForeignKey(Medical, related_name="ment_medical", on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentorship: {self.patient.username} - {self.doctor.username if self.doctor else 'Not Assigned'}"


# ------------------------
# User Profile
# ------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/', default='profile/avator.png', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=255, default='', blank=True)
    gender = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, default='Tanzania', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"