# 🏥 DigiMed - Digital Healthcare Platform

<p align="center">
  <strong>A modern healthcare management system connecting patients with verified doctors</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-green?style=for-the-badge&logo=django" alt="Django 6.0">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

---

## 📋 Overview

DigiMed is a comprehensive digital healthcare platform built with Django 6.0 that facilitates seamless connections between patients and healthcare providers. The platform features an intelligent symptom-based doctor recommendation chatbot, appointment management system, and role-based dashboards for both patients and doctors.

---

## ✨ Features

### 👤 User Management
- **Multi-role Authentication**: Support for Patients, Doctors, and Admins
- **Profile Management**: Separate profiles for patients (medical history, DOB) and doctors (specialization, bio, availability)
- **Doctor Verification**: Admin-controlled doctor verification system

### 📅 Appointment System
- **Easy Booking**: Patients can book appointments with available doctors
- **Status Tracking**: Appointments have status flow (Pending → Accepted/Rejected → Completed)
- **Symptom Recording**: Patients can describe symptoms when booking
- **Working Hours**: Doctors can set their availability (working days and hours)

### 🤖 AI-Powered Chatbot
- **Symptom Analysis**: Intelligent chatbot that analyzes patient symptoms
- **Doctor Recommendations**: Suggests relevant specialists based on symptoms
- **Dialogflow Integration**: Optional Google Dialogflow ES integration for enhanced NLU
- **Fallback Support**: Works offline with built-in symptom-to-specialization mapping

### 🎨 Modern UI
- **Responsive Design**: Mobile-friendly interface
- **Video Slideshow**: Dynamic homepage with video banners
- **Dashboard Views**: Separate dashboards for patients and doctors

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 6.0, Python 3.12+ |
| **Database** | SQLite (default) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **AI/NLU** | Google Dialogflow ES (optional) |
| **Image Processing** | Pillow |

---

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DigiMed.git
   cd DigiMed
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Application: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

---

## 📁 Project Structure

```
DigiMed/
├── appointments/       # Appointment booking app
├── chatbot/           # AI chatbot with Dialogflow integration
├── core/              # Core app (homepage, common utilities)
├── digimed_project/   # Project settings and configurations
├── media/             # User-uploaded files (profile pictures)
├── static/            # Static assets (CSS, JS, images, videos)
├── templates/         # HTML templates
├── users/             # User authentication and profiles
├── db.sqlite3         # SQLite database
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

---

## ⚙️ Configuration

### Environment Variables (Optional - for Dialogflow)

To enable Google Dialogflow integration for enhanced chatbot capabilities:

```bash
export DIALOGFLOW_PROJECT_ID="your-dialogflow-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Allowed Hosts

For production deployment, update `ALLOWED_HOSTS` in `digimed_project/settings.py`:

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

## 👥 User Roles

| Role | Capabilities |
|------|-------------|
| **Patient** | Browse doctors, book appointments, use symptom chatbot, view appointment history |
| **Doctor** | View patient appointments, accept/reject bookings, manage availability |
| **Admin** | Full system access, verify doctors, manage specializations |

---

## 📱 Screenshots

### Homepage
The homepage features a dynamic video slideshow with call-to-action buttons for login and signup.

### Patient Dashboard
- View appointment history
- Access AI chatbot for symptom analysis
- Browse and book appointments with doctors

### Doctor Dashboard
- View upcoming appointments
- Accept or reject appointment requests
- Manage availability settings

---

## ⚠️ Limitations

### Current Development Status
- **Development Only**: This application is currently configured for development use. Production deployment requires additional security configurations.
- **SQLite Database**: Uses SQLite by default, which is suitable for development and small-scale deployments but may require PostgreSQL or MySQL for production environments with high traffic.

### Security Considerations
- **Secret Key**: The secret key in `settings.py` must be changed and kept secret in production.
- **Debug Mode**: Debug mode is enabled by default. Set `DEBUG = False` in production.
- **Password Validation**: Currently uses minimal password validation (1 character minimum) for development convenience. Strengthen this for production.

### Feature Limitations
- **Payment Integration**: No payment gateway integration currently implemented.
- **Video Consultations**: No real-time video/audio consultation feature.
- **Prescription Management**: No digital prescription system.
- **Medical Records**: Limited medical record/history management.
- **Notifications**: No email/SMS notification system for appointment reminders.
- **Multi-language Support**: Currently supports English only.
- **Mobile App**: Web-based only; no native mobile applications.

### Chatbot Limitations
- **Keyword-based Matching**: The built-in symptom matching uses simple keyword detection, which may not capture complex symptom descriptions.
- **Dialogflow Dependency**: Advanced NLU features require Google Dialogflow configuration and associated Google Cloud costs.
- **Limited Medical Scope**: The chatbot covers a limited set of medical specializations and should not be used for medical diagnosis.

### Technical Limitations
- **File Storage**: Uses local file storage for media files. Cloud storage (S3, GCS) recommended for production.
- **Session Management**: Uses database-backed sessions. Consider Redis for better performance at scale.
- **No API Versioning**: REST API endpoints are not versioned.
- **No Rate Limiting**: API endpoints lack rate limiting protection.

---

## 🔒 Disclaimer

> **⚠️ IMPORTANT**: DigiMed is a **demonstration/educational project** and is **NOT intended for real medical use**. The chatbot and recommendation features are for illustration purposes only and should **NOT be used for medical diagnosis or treatment decisions**. Always consult qualified healthcare professionals for medical advice.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

<p align="center">
  Made with ❤️ for better healthcare
</p>
