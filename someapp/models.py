from django.db import models
from django.contrib.auth.models import User

class Habits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_per_day = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class HabitSchedule(models.Model):
    habit = models.ForeignKey(Habits, on_delete=models.CASCADE)
    repeat_time = models.TimeField()

    def __str__(self):
        return f"{self.habit.name}"

class Completion(models.Model):
    habit = models.ForeignKey(Habits, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.name}"