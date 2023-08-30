from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


# Class inherited from django builtin 'UserCreationForm' which has
# all the attributes and functionalities from 'UserCreationForm'
class CustomUserCreationForm(UserCreationForm):
    # Customising django builtin 'UserCreationForm' as the way we wanted
    class Meta:
        # Resultant model name when the form action completes
        model = User
        # Required fields for the user form
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        # To change the label of the form field mentioned in the 'fields'
        labels = {
            'first_name': 'Name'
        }
