
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import CustomUser, Payment, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult
from django.shortcuts import render, get_object_or_404



def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)

    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    # Move the return statement outside of the for loop
    context = {
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    
    return render(request, "student_template/student_home_template.html", context)

def student_view_attendance(request):


    # Getting logged in Student Data
    student = Students.objects.get(admin=request.user.id)


    # Getting Course Enrolled of loggedIn Student
    course = student.course_id


    #Getting the subjects of Course Enrolled
    subjects = Subjects.objects.filter(course_id=course)
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    
    # Getting all the Input Data
    subject_id = request.POST.get('subject')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    try:
        # Parsing the date data into Python objects
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)

        # Getting Logged In User Data
        user_obj = CustomUser .objects.get(id=request.user.id)

        # Getting student Data based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data Based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(
            attendance_date__range=(start_date_parse, end_date_parse),
            subject_id=subject_obj
        )

        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(
            attendance_id__in=attendance,
            student_id=stud_obj
        )

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)

    except Subjects.DoesNotExist:
        messages.error(request, "Subject not found.")
        return redirect('student_view_attendance')
    except Students.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('student_view_attendance')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('student_view_attendance')

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }

    return render(request, 'student_template/student_apply_leave.html', context)



def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave.")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)
    

def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply = "")
            add_feedback.save()
            messages.success(request, "Feedback Sent")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to send Feedback.")
            return redirect ('student_feedback')



def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context = {
        "user": user,
        "student" : student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()


            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    # Get the student object, or return a 404 if not found
    student = get_object_or_404(Students, admin=request.user.id)
    
    # Get the results for the student
    student_result = StudentResult.objects.filter(student_id=student.id)
    
    # Prepare the context
    context = {
        "student_result": student_result
    }
    
    # Use render instead of redirect to return the template with context
    return render(request, "student_template/student_view_result.html", context)



def student_courses_and_payments(request):
    # Get the logged-in student
    student = Students.objects.get(admin=request.user.id)

    # Retrieve courses the student is enrolled in
    enrollments = Courses.objects.filter(students=student)

    # Prepare a list to hold enrollment details
    enrollment_details = []
    for course in enrollments:
        payment = Payment.objects.filter(student=student, course=course).first()
        amount_paid = payment.amount_paid if payment else 0
        remaining_amount = course.fee - amount_paid

        enrollment_info = {
            'course': course,
            'paid_amount': amount_paid,
            'remaining_amount': remaining_amount
        }
        enrollment_details.append(enrollment_info)

    context = {
        'enrollments': enrollment_details
    }
    
    return render(request, 'student_template/student_courses_and_payments.html', context)






