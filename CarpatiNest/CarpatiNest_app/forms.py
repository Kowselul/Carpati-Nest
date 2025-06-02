from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date
from .models import Booking, Review

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

class EmailChangeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Adresă de email nouă"
    )
    confirm_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Confirmă adresa de email"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError(
                    "Cele două adrese de email nu coincid."
                )
                
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Această adresă de email este deja folosită.")
        return email

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nume utilizator'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parolă'})

class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Prenume',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Prenume'})
    )
    last_name = forms.CharField(
        label='Nume',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nume'})
    )
    birth_date = forms.DateField(
        label='Data nașterii',
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@exemplu.com'})
    )
    username = forms.CharField(
        label='Nume utilizator',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nume utilizator'})
    )
    password1 = forms.CharField(
        label='Parolă',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Parolă'})
    )
    password2 = forms.CharField(
        label='Confirmă parola',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirmă parola'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nume utilizator',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nume utilizator'})
    )
    password = forms.CharField(
        label='Parolă',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Parolă'})
    )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'members_count']
        widgets = {
            'booking_date': forms.DateInput(attrs={
                'class': 'form-input flatpickr',
                'data-min-date': date.today().isoformat(),
                'placeholder': 'Alege data rezervării'
            }),
            'members_count': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 20,
                'value': 1
            })
        }

    def __init__(self, *args, **kwargs):
        self.refuge = kwargs.pop('refuge', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        members_count = cleaned_data.get('members_count')
        
        if booking_date:
            if booking_date < date.today():
                raise ValidationError('Data rezervării nu poate fi în trecut.')
            
            if self.refuge:
                # Verificăm locurile disponibile pentru data selectată
                available_spots = self.refuge.get_available_spots(booking_date)
                
                if available_spots <= 0:
                    self.add_error('booking_date', f'Nu mai sunt locuri disponibile pentru data {booking_date.strftime("%d-%m-%Y")}.')
                
                if members_count and members_count > available_spots:
                    self.add_error('members_count', f'Numărul de membri ({members_count}) depășește numărul de locuri disponibile ({available_spots}).')
            else:
                raise ValidationError('Refugiul nu este specificat.')
        
        return cleaned_data

class AccountSettingsForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email nou',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    confirm_email = forms.EmailField(
        label='Confirmă email nou',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    current_password = forms.CharField(
        label='Parolă curentă',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password = forms.CharField(
        label='Parolă nouă',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    confirm_password = forms.CharField(
        label='Confirmă parola nouă',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-input review-rating',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Spune-ne experiența ta la acest refugiu...',
                'rows': 4
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-input'})
        self.fields['comment'].widget.attrs.update({'class': 'form-input'})