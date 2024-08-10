from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Isaque')
        add_placeholder(self.fields['last_name'], 'Ex.: Anderson')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Usuário deve possuir letras, números ou um desses @.+-_.'
            'O tamanho deve ser entre 4 e 150 letras.'
        ),
        error_messages={
            'required': 'Este campo não pode estar vazio',
            'min_length': 'Nome de usuário deve possuir mais que 4 letras',
            'max_length': 'Nome de usúario deve possuuir menos que 150 letras',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu primeiro nome'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'Requer email'},
        label='E-mail',
        help_text='O email deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não pode estar vazia'
        },
        help_text=(
            'A senha deve possuir pelo menos uma letra grande, '
            'uma letra pequena e um número.' 
            'O tamanho deve ser de pelo menos 8 caracteres.'
            
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Por faovr, repita sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Email já cadastrado', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })