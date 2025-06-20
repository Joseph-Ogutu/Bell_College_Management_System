from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from .forms import AddStudentForm, EditStudentForm
from .models import CustomUser, Payment, Staffs, Courses, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, NotificationStudent, NotificationStaffs

def admin_home(request):
    
    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)
    
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)
    
    # For Saffs
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]

    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)


    context={
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')



def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')




def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course_name = request.POST.get('course')
        fee = request.POST.get('fee')  # Get the fee from the form

        # Validate the fee input
        if not fee:
            messages.error(request, "Fee is required!")
            return redirect('add_course')

        try:
            # Convert fee to Decimal
            fee = float(fee)  # You can also use Decimal here if you prefer
            course_model = Courses(course_name=course_name, fee=fee)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except IntegrityError:
            messages.error(request, "Failed to add course, it seems that a course with the same name already exists!")
            return redirect('add_course')
        except ValueError:
            messages.error(request, "Invalid fee format! Please enter a valid number.")
            return redirect('add_course')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('add_course')
        
def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'hod_template/edit_course_template.html', context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')

def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)

def add_session(request):
    return render(request, "hod_template/add_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_session')
    
    session_start_year = request.POST.get('session_start_year')
    session_end_year = request.POST.get('session_end_year')

    try:
        sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
        sessionyear.save()
        messages.success(request, "Session Year added Successfully!")
        return redirect("manage_session")  # Redirect to manage session after adding
    except Exception as e:
        messages.error(request, f"Failed to Add Session Year: {str(e)}")
        return redirect("add_session")

def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)

def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')

    session_id = request.POST.get('session_id')
    session_start_year = request.POST.get('session_start_year')
    session_end_year = request.POST.get('session_end_year')

    try:
        session_year = SessionYearModel.objects.get(id=session_id)
        session_year.session_start_year = session_start_year
        session_year.session_end_year = session_end_year
        session_year.save()

        messages.success(request, "Session Year Updated Successfully.")
        return redirect('manage_session')  # Redirect to manage session after editing
    except Exception as e:
        messages.error(request, f"Failed to Update Session Year: {str(e)}")
        return redirect(f'/edit_session/{session_id}')

def delete_session(request, session_id):
    try:
        session = SessionYearModel.objects.get(id=session_id)
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
    except SessionYearModel.DoesNotExist:
        messages.error(request, "Session not found.")
    except Exception as e:
        messages.error(request, f"Failed to Delete Session: {str(e)}")
    
    return redirect('manage_session')

def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']

            
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=3)
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj

                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):

    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['course_id'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Update Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)



def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            
            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id":subject_id}))
        



def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)

@csrf_exempt  # Consider removing this if possible
def staff_feedback_message_reply(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."})

    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    if not feedback_reply:
        return JsonResponse({"success": False, "message": "Reply cannot be empty."})

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return JsonResponse({"success": True, "message": "Reply saved successfully."})

    except FeedBackStaffs.DoesNotExist:
        return JsonResponse({"success": False, "message": "Feedback not found."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):

    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)
    attendance = Attendance.objects.filter(subject_id=subject_model,session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id,
                    "attendance_date":str(attendance_single.attendance_date),
                    "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),
                        content_type="application/json",
                        safe=False)


@csrf_exempt
def admin_get_attendance_student(request):

    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,
                    "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,
                    "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    

@csrf_exempt  # Use this for testing; remove in production
def contact_view(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        # Basic validation
        if not name or not email or not phone or not desc:
            messages.error(request, "All fields are required.")
            return redirect('contact')

        # Prepare email details
        subject = f'Contact Form Submission from {name}'
        message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {desc}"
        recipient_list = ['ogutujoseph892@gmail.com']  # Replace with the HOD's email address

        try:
            # Send the email
            send_mail(subject, message, email, recipient_list)
            messages.success(request, "Your message has been sent to the HOD successfully!")
            return redirect('contact')  # Redirect to the same page or a success page
        except Exception as e:
            messages.error(request, "There was an error sending your message. Please try again later.")
            return redirect('contact')

    # Render the contact form template
    return render(request, 'contact.html')


def staff_profile(request):
    pass


def student_profile(request):
    pass


def manage_enrollments(request):
    # Fetch all courses
    courses = Courses.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Split the search query into words
        search_terms = search_query.split()
        
        # Create a Q object to combine queries
        from django.db.models import Q
        query = Q()
        
        # Add conditions for each search term
        for term in search_terms:
            query |= Q(admin__first_name__icontains=term) | Q(admin__last_name__icontains=term)
        
        # Filter students based on the combined query
        students = Students.objects.filter(query)
    else:
        students = Students.objects.all()
    
    context = {
        'students': students,
        'courses': courses,
    }
    
    return render(request, 'hod_template/manage_enrollments.html', context)

def add_fee(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        fee_amount = request.POST.get('fee_amount')
        
        try:
            course = Courses.objects.get(id=course_id)
            course.fee = fee_amount
            course.save()
            messages.success(request, "Fee updated successfully!")
        except Courses.DoesNotExist:
            messages.error(request, "Course not found.")
        
        return redirect('manage_enrollments')

def update_payment_status(request, student_id):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        amount_paid = request.POST.get('amount_paid')
        
        try:
            student = Students.objects.get(id=student_id)
            payment, created = Payment.objects.get_or_create(student=student, course_id=course_id)
            payment.amount_paid = amount_paid
            payment.save()
            messages.success(request, "Payment status updated successfully!")
        except Students.DoesNotExist:
            messages.error(request, "Student not found.")
        
        return redirect('manage_enrollments')


def get_latest_leaves(request):
    if request.method == "GET":
        leaves = LeaveReportStudent.objects.filter(leave_status=0)  # Get pending leaves
        leave_data = [
            {
                "id": leave.id,
                "student_name": f"{leave.student_id.admin.first_name} {leave.student_id.admin.last_name}",
                "leave_date": leave.leave_date,
                "leave_message": leave.leave_message,
            }
            for leave in leaves
        ]
        return JsonResponse(leave_data, safe=False)






""""
def create_student_notification(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')  # Get the student ID from the form
        message = request.POST.get('message')  # Get the message from the form

        if not student_id or not message:
            messages.error(request, "Student ID and message are required.")
            return redirect('create_student_notification')  # Redirect to the form page

        try:
            student = Students.objects.get(id=student_id)  # Validate the student exists
            notification = NotificationStudent(student_id=student, message=message)
            notification.save()
            messages.success(request, "Notification sent successfully!")
            return redirect('create_student_notification')  # Redirect after success
        except Students.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('create_student_notification')

def list_student_notifications(request):
    notifications = NotificationStudent.objects.all().order_by('-created_at')  # Fetch all notifications
    return render(request, 'notifications/student_notifications.html', {'notifications': notifications})

def create_staff_notification(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')  # Get the staff ID from the form
        message = request.POST.get('message')  # Get the message from the form

        if not staff_id or not message:
            messages.error(request, "Staff ID and message are required.")
            return redirect('create_staff_notification')  # Redirect to the form page

        try:
            staff = Staffs.objects.get(id=staff_id)  # Validate the staff exists
            notification = NotificationStaffs(staff_id=staff, message=message)
            notification.save()
            messages.success(request, "Notification sent successfully!")
            return redirect('create_staff_notification')  # Redirect after success
        except Staffs.DoesNotExist:
            messages.error(request, "Staff not found.")
            return redirect('create_staff_notification')

def list_staff_notifications(request):
    notifications = NotificationStaffs.objects.all().order_by('-created_at')  # Fetch all notifications
    return render(request, 'notifications/staff_notifications.html', {'notifications': notifications})


"""

