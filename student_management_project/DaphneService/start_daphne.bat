@echo off
cd C:\path\to\Desktop\Bell_College_Management_System\student_management_project
C:\path\to\your\venv\Scripts\activate  # Activate your virtual environment
daphne -u C:\path\to\your\project\run\daphne.sock myproject.asgi:application  # Adjust path to Daphne if needed