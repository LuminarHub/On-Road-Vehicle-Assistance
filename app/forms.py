from django import forms
from django.core.exceptions import ValidationError
from .models import *

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']


#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'user'
#         if commit:
#             user.save()
#         return user

# class MechanicRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']


#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'mechanic'
#         if commit:
#             user.save()
#         return user

# class CarRenterRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'car_renter'
#         if commit:
#             user.save()
#         return user
    
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('user', 'User'), ('mechanic', 'Mechanic'), ('car_renter', 'Car Renter')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = "admin"
        user.is_staff = True
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class MechanicProfileForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=True)
    SPECIALIZATION_CHOICES = [
        ("two_wheeler", "Two Wheeler"),
        ("four_wheeler", "Four Wheeler"),
        ("heavy_vehicle", "Heavy Vehicle"),
    ]
    specialized_in = forms.ChoiceField(choices=SPECIALIZATION_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MechanicProfile
        fields = ['name','location', 'phone', 'dob', 'skills', 'experience', 'specialized_in', 'bio', 'profile_pic']


class AddLocationForm(forms.ModelForm):
    class Meta:
        model=Location
        fields=['name',]


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = UserProfile
        fields = ['name', 'address', 'phone', 'dob', 'profile_pic']


class ReqToMechanicForm(forms.ModelForm):
    class Meta:
        model = ReqToMechanic
        fields = ['discription', 'location']

    
class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['text', 'rating']

class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['payment']

class UserPaymentForm(forms.ModelForm):
    class Meta:
        model = UserPayment
        fields = ['acholdername','accno','cvv','exp','amount']

class CarRenterProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CarRenterProfile
        fields = ['name', 'address', 'phone', 'dob', 'bio', 'profile_pic']

class RentCarForm(forms.ModelForm):
    class Meta:
        model = RentCar
        fields = ['name', 'price', 'car_img', 'discription']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter car name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter price'}),
            # 'car_img': forms.FileInput(attrs={}),
            'discription': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter description','rows':4}),
        }
        labels = {
            'name': 'Car Name',
            'price': 'Price',
            'car_img': 'Car Image',
            'discription': 'Description',
        }


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CarReserve
        fields = ['start_date', 'end_date']

class MechanicSearchForm(forms.Form):
    mechanic = forms.CharField(max_length=30, required=False)



class ChangePasswordForm(forms.Form):
    current_password=forms.CharField(max_length=50,label="current password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    new_password=forms.CharField(max_length=50,label="new password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    confirm_password=forms.CharField(max_length=50,label="confirm password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
