# views.py
from django.shortcuts import render, redirect
from .models import NotificationStudent, NotificationStaffs
from .utils import notify_admin

def send_student_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        student_id = request.user.id  # Assuming the user is a student
        notification = NotificationStudent.objects.create(student_id=student_id, message=message)
        
        # Notify admin
        notify_admin(f"New message from student {student_id}: {message}")
        
        return redirect('some_view')

def send_staff_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        staff_id = request.user.id  # Assuming the user is a staff member
        notification = NotificationStaffs.objects.create(staff_id=staff_id, message=message)
        
        # Notify admin
        notify_admin(f"New message from staff {staff_id}: {message}")
        
        return redirect('some_view')