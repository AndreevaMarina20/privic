from django.contrib import admin
from .models import *

admin.site.register(Habits)
admin.site.register(HabitSchedule)
admin.site.register(Completion)