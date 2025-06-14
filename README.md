# Healthcare Backend System

## 🟢 Project Run Guide

### 1. ✅ Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt
```

---

### 2. 🛠️ Database Setup

Ensure PostgreSQL is installed and running. The database is already configured in `settings.py`:

- **Database:** postgres
- **User:** postgres
- **Password:** Samsung@1029
- **Host:** localhost
- **Port:** 5432

---

### 3. 📦 Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. 👤 Create Admin User

```bash
python manage.py createsuperuser
```

---

### 5. 🚀 Run the Development Server

```bash
python manage.py runserver
```

---

## 🧪 API Testing with Postman

### 🔧 Setup Postman Environment

1. Create new environment: **Healthcare Local**
2. Add variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: _(leave empty, will be auto-filled after login)_

---

### 🧾 API Testing Flow

---

### 🔐 1. Authentication

#### ✅ Register

```
POST {{base_url}}/api/register/
Content-Type: application/json

{
    "email": "test@example.com",
    "name": "Test User",
    "password": "Test@123",
    "password2": "Test@123"
}
```

#### 🔑 Login (Get Token)

```
POST {{base_url}}/api/auth/login/
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "Test@123"
}
```

🔁 Add this **Test Script** in Postman to auto-save token:

```javascript
var jsonData = pm.response.json();
pm.environment.set("access_token", jsonData.access);
```

#### 🔄 Refresh Token

```
POST {{base_url}}/api/auth/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

---

### 🧍‍♂️ 2. Patient Management

#### ➕ Create Patient

```
POST {{base_url}}/api/patients/
Headers:
- Authorization: Bearer {{access_token}}
- Content-Type: application/json

{
    "user_id": 1,
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "address": "123 Main St",
    "phone_number": "1234567890",
    "medical_history": "No issues"
}
```

#### 📃 List Patients

```
GET {{base_url}}/api/patients/
Authorization: Bearer {{access_token}}
```

#### 🔍 Get Patient

```
GET {{base_url}}/api/patients/1/
Authorization: Bearer {{access_token}}
```

#### 📝 Update Patient

```
PUT {{base_url}}/api/patients/1/
Headers:
- Authorization: Bearer {{access_token}}
- Content-Type: application/json

{
    "user_id": 1,
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "address": "456 New St",
    "phone_number": "9876543210",
    "medical_history": "Updated"
}
```

#### ❌ Delete Patient

```
DELETE {{base_url}}/api/patients/1/
Authorization: Bearer {{access_token}}
```

---

### 👨‍⚕️ 3. Doctor Management

#### ➕ Create Doctor

```
POST {{base_url}}/api/doctors/
Headers:
- Authorization: Bearer {{access_token}}
- Content-Type: application/json

{
    "user_id": 1,
    "specialization": "GP",
    "license_number": "DOC123456",
    "years_of_experience": 10,
    "hospital": "City Hospital"
}
```

#### 📃 List Doctors

```
GET {{base_url}}/api/doctors/
Authorization: Bearer {{access_token}}
```

#### 🔍 Get Doctor

```
GET {{base_url}}/api/doctors/1/
Authorization: Bearer {{access_token}}
```

#### 📝 Update Doctor

```
PUT {{base_url}}/api/doctors/1/
Headers:
- Authorization: Bearer {{access_token}}
- Content-Type: application/json

{
    "user_id": 1,
    "specialization": "CARD",
    "license_number": "DOC123456",
    "years_of_experience": 12,
    "hospital": "New Hospital"
}
```

#### ❌ Delete Doctor

```
DELETE {{base_url}}/api/doctors/1/
Authorization: Bearer {{access_token}}
```

---

### 🔗 4. Patient-Doctor Mapping

#### ➕ Create Mapping

```
POST {{base_url}}/api/mappings/
Headers:
- Authorization: Bearer {{access_token}}
- Content-Type: application/json

{
    "patient_id": 1,
    "doctor_id": 1,
    "notes": "Regular checkup"
}
```

#### 📃 List All Mappings

```
GET {{base_url}}/api/mappings/
Authorization: Bearer {{access_token}}
```

#### 🧑‍⚕️ Get Patient's Doctors

```
GET {{base_url}}/api/mappings/patient_doctors/
Authorization: Bearer {{access_token}}
```

#### 🧑‍🤝‍🧑 Get Doctor's Patients

```
GET {{base_url}}/api/mappings/doctor_patients/
Authorization: Bearer {{access_token}}
```

#### ❌ Delete Mapping

```
DELETE {{base_url}}/api/mappings/1/
Authorization: Bearer {{access_token}}
```

---

## 🧭 Testing Flow Summary

1. **Register a new user**
2. **Login** → Save `access_token`
3. **Create patient** (with `user_id`)
4. **Create doctor** (with `user_id`)
5. **Create mapping**
6. Perform all CRUD operations
7. Test special mapping endpoints

---

## 🛠️ Common Errors & Fixes

| Error                     | Reason                 | Fix                             |
| ------------------------- | ---------------------- | ------------------------------- |
| 401 Unauthorized          | Missing/Invalid token  | Check headers and refresh token |
| 400 Bad Request           | Invalid data format    | Check required fields and types |
| 404 Not Found             | ID does not exist      | Verify IDs and endpoints        |
| 500 Internal Server Error | Server/database issues | Check logs, re-run migrations   |
