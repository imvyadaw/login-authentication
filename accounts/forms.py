# from django import forms

# class ForgotPasswordForm(forms.Form):
#     email = forms.EmailField()

# class ResetPasswordForm(forms.Form):
#     otp = forms.CharField(max_length=6)
#     new_password = forms.CharField(widget=forms.PasswordInput())

from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    otp = forms.CharField(max_length=6)  # OTP is 6 digits
    new_password = forms.CharField(widget=forms.PasswordInput())
