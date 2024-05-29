from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
class LoginForm(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('Username')
        password = cleaned_data.get('Password')

        if username and password:
            user = authenticate(username=username, password=password)
            print("user ne",user)
            if not user:
                raise forms.ValidationError("Username or password is invalid.")
        return cleaned_data
    
class RegisterForm(UserCreationForm):
    username=forms.CharField(max_length=40, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, label="Phone Number", required=True)  # Telefon numarası alanı eklendi
    email = forms.EmailField(label='Email')   
    
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name','email', 'phone_number', 'password1', 'password2')  # phone_number eklendi
        error_messages={'password_mismatch':'Şifreler eşleşmiyor'}

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")

        if username and email:
            user = CustomUser.objects.filter(username=username).first()
            if user:
                raise forms.ValidationError("Bu kullanıcı adı zaten alınmış.")

            user = CustomUser.objects.filter(email=email).first()
            if user:
                raise forms.ValidationError("Bu e-posta adresi zaten kayıtlı.")

        return cleaned_data

 
  