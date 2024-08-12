from django.contrib.auth.forms import UserCreationForm
from .models import CiteUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CiteUser
        fields = ('username', 'email')
