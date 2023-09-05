from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Skill


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
    # field and added a class of input for styling the form field
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


# Customising the form to edit User account
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # To avoid selecting users manually fields are included
        fields = ['name', 'email', 'username', 'location', 'short_intro',
                  'bio', 'profile_image', 'social_github', 'social_twitter',
                  'social_linkedin', 'social_youtube', 'social_website']

    # Overridden the super method and looped through every single
    # field and added a class of input for styling the form field
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
