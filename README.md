# 🧠 Student Tools – Final Release Notes

## ✅ User Notes (for Students & Faculty)

These instructions help end users navigate and utilize the software.

### 1. Registration
- Users must provide a unique username and a valid email.
- OTP will be sent to the email for verification before account creation.

### 2. Login
- Enter username and password to log in.
- Forgot password? Use the OTP-based password reset feature.

### 3. Attendance
- Turn on Bluetooth for automated detection.
- Faculty can mark attendance via:
  - Bluetooth auto-mode
  - Semi-auto (with MAC address verification)
  - Manual entry

### 4. MAC Address Registration
- Faculty must register students' MAC addresses to enable Bluetooth-based auto-attendance.

### 5. Attendance Reports
- Faculty can view detailed records.
- Students can track their own attendance percentage.

### 6. Document Tools (Students)
- Upload, download, or delete personal-use files.
- Supported file types and size limitations apply.

### 7. Discussion Forum
- Start or reply to threads.
- Open to both students and faculty.

### 8. Security & Logging
- All critical operations are logged for audit and security.

---

## 🛠️ Developer Notes

This section is for developers maintaining or extending the system.

### 1. Architecture
- Frontend: KivyMD (Python)
- Backend: Django REST Framework
- Database: MySQL

### 2. Bluetooth Integration
- Windows: Uses `pybluez`
- Android: Uses `pyjnius` + Android Bluetooth APIs
- Requires runtime permissions for Android.

### 3. Authentication
- OTP-based email verification for registration and password reset.
- Includes password strength check and field validation.

### 4. Logging
- User actions (logins, attendance, uploads, etc.) are logged securely.

### 5. Attendance System
- Automatically detects registered Bluetooth devices.
- Falls back to semi-auto or manual based on conditions.

### 6. Document Management
- Files are stored server-side and linked to user accounts.
- Validates file size and type.

### 7. Discussion Forum
- Threaded discussions stored in DB.
- Text-only for simplicity.

### 8. Build & Deployment
- Desktop: `.exe` built using PyInstaller.
- Android: Use Buildozer for `.apk`. Ensure correct permissions in `buildozer.spec`.

### 9. Known Limitations
- Android may require manual permission approval (BLUETOOTH, LOCATION).
- Performance may vary due to hardware/threading constraints.
- No support yet for media uploads in discussion.

---

## ✅ Feature Implementation Status

-------------------------------------------------------------------------------------
| Feature/Use Case                    | Status                                       |
|-------------------------------------|----------------------------------------------|
| OTP-Based Registration              | ✅ Implemented                              |
| Login & Password Reset              | ✅ Implemented                              |
| MAC Registration (Faculty)          | ✅ Implemented                              |
| Bluetooth Attendance                | ✅ Implemented                              |
| Manual Attendance                   | ✅ Implemented                              |
| Attendance Reports                  | ✅ Implemented                              |
| File Upload/Download/Delete         | ✅ Implemented                              |
| Discussion Forum                    | ✅ Implemented                              |
| Logging & Security                  | ✅ Implemented                              |
| Android Support                     | ⚠️ Partially (Bluetooth permission issues ) |
--------------------------------------------------------------------------------------
