from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé
    """
    email = forms.EmailField(
        required=True,
        label='Email'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Prénom'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nom'
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        label='Numéro de téléphone'
    )
    
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        label='Rôle',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('role', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'S\'inscrire', css_class='btn btn-primary')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé
    """
    username = forms.CharField(
        label='Nom d\'utilisateur ou Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur ou Email'})
    )
    
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Se connecter', css_class='btn btn-primary w-100')
        )

