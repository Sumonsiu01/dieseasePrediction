# 🏥 DiseasePredict - Full Stack Healthcare Solution

**DiseasePredict** is a modern, AI-integrated healthcare web application designed to help patients predict potential diseases based on symptoms and manage their medical profiles. Built with **Django** and a sleek **Tailwind CSS** frontend, it offers a premium user experience with both dark and light mode support.

---

## ✨ Key Features

### 🔐 User Authentication & Security
* **Role-Based Access:** Specialized dashboards for Patients and (future-scope) Doctors.
* **Secure Login/Register:** Optimized authentication flow with real-time validation.
* **Password Management:** Robust password update system using Django's session authentication hash to keep users logged in after a change.
* **Session Tracking:** Monitor last login and active device information.

### 🎨 Premium UI/UX
* **Glassmorphism Design:** A modern, translucent interface built with Tailwind CSS.
* **Theme Toggle:** Seamless switching between **Dark Mode** and **Light Mode**.
* **Responsive Layout:** Fully optimized for Mobile, Tablet, and Desktop views.
* **Interactive Elements:** Smooth animations using `Animate.css` and `Framer Motion` (integrated in frontend components).

### 🩺 Healthcare Features
* **Patient Dashboard:** Quick access to disease prediction tools and history.
* **Profile Management:** Update personal information, contact details, and security settings.

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Django (v4.x+) |
| **Frontend** | JavaScript (React/Vite), Tailwind CSS, HTML5 |
| **Database** | MySQL (Production), Redis (Caching) |
| **DevOps** | Docker, GitHub Actions, SonarCloud |
| **Deployment** | AWS / Cloud Infrastructure |

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* MySQL Server
* Virtualenv

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/DiseasePredict.git](https://github.com/yourusername/DiseasePredict.git)
    cd DiseasePredict
    ```

2.  **Create & Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migration:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

---

## 📂 Project Structure

```text
DiseasePredict/
├── core/               # Project configuration
├── patients/           # Patient management logic
├── static/             # CSS, JS, and Images
├── templates/          # HTML Templates (Login, Profile, Home)
├── manage.py           # Django CLI
└── requirements.txt    # Project dependencies
