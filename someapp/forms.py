from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class HabitsForm(ModelForm):
    class Meta:
        model = Habits
        fields = ['user', 'name', 'target_per_day']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['target_per_day'].required = False

class HabitScheduleForm(ModelForm):
    class Meta:
        model = HabitSchedule
        fields = ['habit', 'repeat_time']

class CompletionForm(ModelForm):
    class Meta:
        model = Completion
        fields = ['habit']