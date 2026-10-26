from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import DateField
from django.utils.functional import empty

from ClientsAlbarans.models import Client, Albara, LineaAlbara, Magatzem, Empleat, Producte


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'codi_cliente': forms.TextInput(attrs={'placeholder': 'codi client'}),
        }

class AlbaraForm(forms.ModelForm):
    class Meta:
        model = Albara
        fields = ['client','magatzem']
        widgets = {

        }

class EditarClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class EditarEstatAlbaraForm(forms.ModelForm):
    class Meta:
        model = Albara
        fields = ['estat']



class BuscarAlbaraForm(forms.Form):
    numero_albara = forms.IntegerField(
        label="Número de albarán",
        required=True
    )

class AfegirLineaAlbaraForm(forms.ModelForm):
    class Meta:
        model = LineaAlbara
        fields = ['producte','quantitat','descompte_percentatge']

class MarcarPreparacioForm(forms.ModelForm):
    class Meta:
        model = Albara
        fields = ['estat']

class ReposicioForm(forms.Form):
    magatzem = forms.ModelChoiceField(queryset=Magatzem.objects.all())
    producte = forms.ModelChoiceField(queryset=Producte.objects.all())
    quantitat = forms.IntegerField(min_value=1, label="Unitats a afegir")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    codi_empleat = forms.CharField(max_length=100)
    telefon = forms.CharField(max_length=20)
    carrec = forms.CharField(max_length=100)




    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', 'Les contrasenyes no coincideixen')

        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', 'Aquest usuari ja existeix')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        Empleat.objects.create(
            user=user,
            codi_empleat=self.cleaned_data['codi_empleat'],
            data_alta=date.today(),
            telefon=self.cleaned_data['telefon'],
            carrec=self.cleaned_data['carrec'],
        )

        return user



class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Contrasenya")
    User = get_user_model()
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            return cleaned_data  # Si faltan datos, no seguimos

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', 'No existeix cap usuari amb aquest email')
            return cleaned_data

        if not user.check_password(password):
            self.add_error('password', 'Contrasenya incorrecta')
            return cleaned_data

        cleaned_data['user'] = user
        return cleaned_data






