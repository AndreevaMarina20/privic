from django.views import View
from django.http import JsonResponse
from .models import Habits, HabitSchedule, Completion
from django.contrib.auth.models import User


# 1. GET /users - получить список пользователей
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
            })
        return JsonResponse({'data': user_list})


# 2. GET /users/<id> - получить конкретного пользователя
class UserDetailView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


# 3. GET /users/<id>/habits - получить привычки пользователя
class UserHabitsView(View):
    def get(self, request, user_id):
        habits = Habits.objects.filter(user_id=user_id)
        habit_list = []
        for habit in habits:
            habit_list.append({
                'id': habit.id,
                'name': habit.name,
                'target_per_day': habit.target_per_day,
            })
        return JsonResponse({'data': habit_list})


# 4. GET /habits/<id> - получить конкретную привычку 
class HabitDetailView(View):
    def get(self, request, habit_id):
        habit = Habits.objects.get(id=habit_id)
        return JsonResponse({
            'id': habit.id,
            'name': habit.name,
            'target_per_day': habit.target_per_day,
            'user_id': habit.user.id,
        })


# 5. GET /habits/<id>/schedule - получить расписание привычки
class HabitScheduleView(View):
    def get(self, request, habit_id):
        schedules = HabitSchedule.objects.filter(habit_id=habit_id)
        schedule_list = []
        for schedule in schedules:
            schedule_list.append({
                'id': schedule.id,
                'repeat_time': schedule.repeat_time,
            })
        return JsonResponse({'data': schedule_list})


# 6. GET /habits/<id>/completions - получить историю выполнений
class HabitCompletionsView(View):
    def get(self, request, habit_id):
        completions = Completion.objects.filter(habit_id=habit_id)
        completion_list = []
        for completion in completions:
            completion_list.append({
                'id': completion.id,
                'completed_at': completion.completed_at,
            })
        return JsonResponse({'data': completion_list})


# 7. GET /habits/<id>/stats - получить статистику привычки
class HabitStatsView(View):
    def get(self, request, habit_id):
        count = Completion.objects.filter(habit_id=habit_id).count()
        return JsonResponse({
            'habit_id': habit_id,
            'total_completions': count,
        })


# 8. GET /users/<id>/stats - получить общую статистику пользователя
class UserStatsView(View):
    def get(self, request, user_id):
        total_habits = Habits.objects.filter(user_id=user_id).count()
        total_completions = Completion.objects.filter(habit__user_id=user_id).count()
        return JsonResponse({
            'user_id': user_id,
            'total_habits': total_habits,
            'total_completions': total_completions,
        })