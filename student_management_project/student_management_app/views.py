from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, Staffs, Students, AdminHOD
from django.contrib import messages

def home(request):
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')


def loginUser(request):
	return render(request, 'login_page.html')

def doLogin(request):
	
	print("here")
	email_id = request.GET.get('email')
	password = request.GET.get('password')
	# user_type = request.GET.get('user_type')
	print(email_id)
	print(password)
	print(request.user)
	if not (email_id and password):
		messages.error(request, "Please provide all the details!!")
		return render(request, 'login_page.html')

	user = CustomUser.objects.filter(email=email_id, password=password).last()
	if not user:
		messages.error(request, 'Invalid Login Credentials!!')
		return render(request, 'login_page.html')

	login(request, user)
	print(request.user)

	if user.user_type == CustomUser.STUDENT:
		return redirect('student_home/')
	elif user.user_type == CustomUser.STAFF:
		return redirect('staff_home/')
	elif user.user_type == CustomUser.HOD:
		return redirect('admin_home/')

	return render(request, 'home.html')


def doRegistration(request):
    if request.method != 'POST':
        return render(request, 'registration.html')

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirmPassword')

    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')

    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'registration.html')

    if CustomUser .objects.filter(email=email_id).exists():
        messages.error(request, 'User  with this email id already exists. Please proceed to login!!')
        return render(request, 'registration.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
        return render(request, 'registration.html')

    username = email_id.split('@')[0].split('.')[0]

    if CustomUser .objects.filter(username=username).exists():
        messages.error(request, 'User  with this username already exists. Please use a different username')
        return render(request, 'registration.html')

    # Create the user
    user = CustomUser (
        username=username,
        email=email_id,
        user_type=user_type,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)  # Hash the password
    user.save()


    # Create the related model instance for other user types
    if user_type == CustomUser .STAFF:
        Staffs.objects.create(admin=user)
    elif user_type == CustomUser .HOD:
        AdminHOD.objects.create(admin=user)

    messages.success(request, 'Registration successful! You can now log in.')
    return HttpResponseRedirect('/login')  # Redirect to the login page
	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


def get_user_type_from_email(email_id):
	"""
	Returns CustomUser.user_type corresponding to the given email address
	email_id should be in following format:
	'<username>.<staff|student|hod>@<college_domain>'
	eg.: 'joseph.staff@bellcollege.edu'
	"""

	try:
		email_id = email_id.split('@')[0]
		email_user_type = email_id.split('.')[1]
		return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
	except:
		return None