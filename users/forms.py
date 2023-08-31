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

    # Overridden the super method and looped through every single
    # field and added a class of input
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
