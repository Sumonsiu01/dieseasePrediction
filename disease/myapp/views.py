import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# =========================
# USER MODEL
# =========================
User = get_user_model()

# =========================
# MODEL & DATA LOAD
# =========================
BASE_DIR = Path(settings.BASE_DIR)
MODEL_DIR = BASE_DIR / 'myapp' / 'models'
DISEASE_CSV = BASE_DIR / 'Disease.csv'

FULL_SYMPTOMS_LIST = []
DISEASE_NAMES = []
lr_model = None
drug_model = None

# নোটবুকের ম্যাপিং অনুযায়ী ডিজিজ আইডি (Drug Model এর জন্য)
DISEASE_MAP = {
    'Acne': 0, 'Allergy': 1, 'Diabetes': 2, 'Fungal infection': 3,
    'Urinary tract infection': 4, 'Malaria': 5, 'Migraine': 6, 
    'Hepatitis B': 7, 'AIDS': 8
}

try:
    # ১. রোগ শনাক্ত করার মডেল (Logistic Regression)
    lr_model = joblib.load(MODEL_DIR / 'lr_classifier.pkl')
    # ২. ওষুধ সাজেস্ট করার মডেল (Decision Tree - তোর নোটবুক থেকে)
    drug_model = joblib.load(MODEL_DIR / 'dt_classifier.pkl')
    
    # CSV লোড করে সিম্পটম এবং রোগের লিস্ট তৈরি
    if DISEASE_CSV.exists():
        df_temp = pd.read_csv(DISEASE_CSV)
        FULL_SYMPTOMS_LIST = [col.strip() for col in df_temp.columns[:-1]]
        DISEASE_NAMES = sorted(df_temp.iloc[:, -1].unique())
        print(f"✅ Success: Loaded {len(FULL_SYMPTOMS_LIST)} symptoms.")
    else:
        print(f"❌ Error: Disease.csv not found at {DISEASE_CSV}")

except Exception as e:
    print(f"⚠️ Initialization Error: {e}")

# =========================
# VIEWS
# =========================

def home(request):
    return render(request, 'myapp/home.html')

def profile(request):

    pw_form = PasswordChangeForm(request.user)
    # এখানে লজিক আরও বাড়ানো যায় (যেমন সেশন থেকে ডিভাইস ট্র্যাকিং)
    # আপাতত বেসিক প্রোফাইল ডেটা পাঠানো হচ্ছে
    return render(request, 'myapp/profile.html', {
        'pw_form': pw_form,
        'last_login': request.user.last_login,
    })



@login_required
def update_profile(request):
    if request.method == "POST":
        # ১. ফরম থেকে ডাটা নেওয়া (HTML input এ name="full_name" আর name="phone" থাকতে হবে)
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        
        # ২. বর্তমান ইউজারকে ধরা
        user = request.user
        
        # ৩. ডাটা আপডেট করা
        if full_name:
            user.first_name = full_name  # জ্যাঙ্গোর ডিফল্ট ফিল্ড
        
        if phone:
            user.phonenumber = phone  # তোর কাস্টম ইউজার মডেলের ফিল্ড
        
        # ৪. ডাটাবেসে সেভ করা (এই লাইনটা সবচেয়ে ইম্পর্ট্যান্ট)
        user.save() 

        messages.success(request, "Profile name updated")
        return redirect('profile') 
    
    return redirect('profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        # এখানে অবশ্যই request.user এবং request.POST দিতে হবে
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            # পাসওয়ার্ড পরিবর্তনের পর সেশন আপডেট করা জরুরি, না হলে ইউজার লগআউট হয়ে যাবে
            update_session_auth_hash(request, user)
            messages.success(request, 'তোর পাসওয়ার্ড সফলভাবে পরিবর্তন করা হয়েছে!')
            return redirect('profile')
        else:
            # ফরম কেন ভ্যালিড হয়নি তার এরর মেসেজগুলো দেখানো
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return redirect('profile')
            
    return redirect('profile')

def patient_home(request):
    return render(request, 'myapp/patient_home.html')

# ✅ MAIN PREDICTION VIEW (Disease + Drug)
def prediction_view(request):
    if not FULL_SYMPTOMS_LIST or lr_model is None:
        return HttpResponse("Server Error: Machine Learning components are not loaded.")

    if request.method == 'POST':
        selected_symptoms = request.POST.getlist('symptoms[]')
        
        # ড্রাগ মডেলের জন্য ইউজার ডেটা (তোর নোটবুক অনুযায়ী Gender ও Age লাগবে)
        # এগুলো সাধারণত ইউজার প্রোফাইল থেকে আসে, আপাতত ডিফল্ট দিচ্ছি
        user_age = 23 
        user_gender = 1 # Male: 1, Female: 0

        if not selected_symptoms:
            messages.warning(request, "দয়া করে অন্তত একটি সিম্পটম সিলেক্ট কর।")
            return render(request, 'myapp/prediction.html', {'symptoms_list': FULL_SYMPTOMS_LIST})

        # --- পার্ট ১: রোগ প্রেডিকশন ---
        input_data = [0] * len(FULL_SYMPTOMS_LIST)
        for symptom in selected_symptoms:
            symptom = symptom.strip()
            if symptom in FULL_SYMPTOMS_LIST:
                index = FULL_SYMPTOMS_LIST.index(symptom)
                input_data[index] = 1
        
        disease_idx = lr_model.predict(np.array([input_data]))[0]
        disease_name = DISEASE_NAMES[disease_idx] if DISEASE_NAMES else f"Code: {disease_idx}"

        # --- পার্ট ২: ওষুধ (Drug) সাজেস্ট করা ---
        suggested_drug = "No specific medication suggested by the model."
        try:
            # নোটবুকের লজিক: রোগের নামকে ম্যাপ করা
            mapped_id = DISEASE_MAP.get(disease_name, 0)
            
            # ড্রাগ মডেল ইনপুট: [[Disease_ID, Gender, Age]]
            drug_input = np.array([[mapped_id, user_gender, user_age]])
            drug_prediction = drug_model.predict(drug_input)
            suggested_drug = drug_prediction[0]
        except Exception as e:
            print(f"Drug Suggestion Error: {e}")

        return render(request, 'myapp/result.html', {
            'prediction': disease_name,
            'suggested_drug': suggested_drug, # ওষুধের নাম
            'model_used': 'Hybrid (LR + DT)',
            'symptoms': selected_symptoms
        })

    return render(request, 'myapp/prediction.html', {'symptoms_list': FULL_SYMPTOMS_LIST})

# =========================
# AUTHENTICATION
# =========================

def patient_register(request):
    return render(request, 'myapp/register.html')

def reg_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'এই ইমেইল দিয়ে আগেই অ্যাকাউন্ট খোলা হয়েছে।')
            return redirect('patient_register')

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
            phonenumber=phone,
            is_patient=True
        )
        messages.success(request, 'অ্যাকাউন্ট তৈরি সফল হয়েছে! এখন লগইন কর।')
        return redirect('login')
    return redirect('patient_register')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                auth_login(request, user)
                return redirect('patient_home')
        messages.error(request, 'ভুল ইমেইল বা পাসওয়ার্ড!')
    return render(request, 'myapp/login.html')

def patient_logout(request):
    logout(request)
    return redirect('home')