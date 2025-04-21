from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'User already exists'})
        User.objects.create_user(username=email, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        elif not User.objects.filter(username=email).exists():
            return render(request, 'login.html', {'error': 'User not found'})
        else:
            return render(request, 'login.html', {'error': 'Incorrect password'})
    return render(request, 'login.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')



# paass
# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.contrib import messages
# from .forms import ForgotPasswordForm, ResetPasswordForm
# import random

# # This will store the OTP temporarily (you can use a database or cache)
# otp_storage = {}

# def forgot_password(request):
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 user = User.objects.get(email=email)
#                 otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
#                 otp_storage[email] = otp  # Store OTP temporarily (use cache or db in real use)
                
#                 # Send OTP to email
#                 send_mail(
#                     'Password Reset OTP',
#                     f'Your OTP for resetting password is {otp}',
#                     'no-reply@example.com',  # Use your email
#                     [email],
#                 )
#                 messages.success(request, 'OTP sent to your email.')
#                 return redirect('reset_password')  # Redirect to OTP input page
#             except User.DoesNotExist:
#                 messages.error(request, 'User with this email not found.')
#     else:
#         form = ForgotPasswordForm()
    
#     return render(request, 'forgot_password.html', {'form': form})

# def reset_password(request):
#     if request.method == 'POST':
#         form = ResetPasswordForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data['otp']
#             new_password = form.cleaned_data['new_password']
            
#             # Check if OTP is correct
#             email = request.session.get('email')  # Store email in session during forgot password
#             if otp == otp_storage.get(email):
#                 user = User.objects.get(email=email)
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, 'Password reset successfully.')
#                 return redirect('login')  # Redirect to login page after success
#             else:
#                 messages.error(request, 'Invalid OTP or OTP expired.')

#     else:
#         form = ResetPasswordForm()
    
#     return render(request, 'reset_password.html', {'form': form})


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from .forms import ForgotPasswordForm, ResetPasswordForm
import random

# This will store the OTP temporarily (you can use a database or cache)
otp_storage = {}

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
                otp_storage[email] = otp  # Store OTP temporarily (use cache or db in real use)
                
                # Send OTP to email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for resetting password is {otp}',
                    'imblackdragondev@gmail.com',  # Replace with your email
                    [email],
                )
                messages.success(request, 'OTP sent to your email.')
                request.session['email'] = email  # Store email in session for OTP validation
                return redirect('reset_password')  # Redirect to OTP input page
            except User.DoesNotExist:
                messages.error(request, 'User with this email not found.')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            
            # Check if OTP is correct
            email = request.session.get('email')  # Store email in session during forgot password
            if otp == otp_storage.get(email):
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                logout(request)  # Log out the user after resetting the password
                return redirect('login')  # Redirect to login page after success
            else:
                messages.error(request, 'Invalid OTP or OTP expired.')

    else:
        form = ResetPasswordForm()
    
    return render(request, 'reset_password.html', {'form': form})
