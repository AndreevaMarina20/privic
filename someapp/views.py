from django.views import View
from django.http import JsonResponse
from .models import Habits, HabitSchedule, Completion
from django.contrib.auth.models import User
from json import loads
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


# 1. GET /users - список пользователей + POST
@method_decorator(csrf_exempt, 'dispatch')
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        user_list = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
        return JsonResponse({'data': user_list})

    def post(self, request):
        new_data = loads(request.body)
        form = UserForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


# 2. GET /users/<id> - один пользователь
class UserDetailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email})


# 3. GET /users/<id>/habits + POST
@method_decorator(csrf_exempt, 'dispatch')
class UserHabitsView(View):
    def get(self, request, user_id):
        habits = Habits.objects.filter(user_id=user_id)
        habit_list = [{'id': h.id, 'name': h.name, 'target_per_day': h.target_per_day} for h in habits]
        return JsonResponse({'data': habit_list})

    def post(self, request, user_id):
        new_data = loads(request.body)
        new_data['user'] = user_id
        form = HabitsForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request, user_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


# 4. GET/PUT/PATCH/DELETE /habits/<id>
@method_decorator(csrf_exempt, 'dispatch')
class HabitDetailView(View):
    def get(self, request, habit_id):
        habit = get_object_or_404(Habits, id=habit_id)
        return JsonResponse({
            'id': habit.id,
            'name': habit.name,
            'target_per_day': habit.target_per_day,
            'user_id': habit.user.id,
        })

    def put(self, request, habit_id):
        obj = get_object_or_404(Habits, id=habit_id)
        new_data = loads(request.body)
        form = HabitsForm(new_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def patch(self, request, habit_id):
        obj = get_object_or_404(Habits, id=habit_id)
        new_data = loads(request.body)

        # Собираем полные данные: старые из объекта + новые из запроса
        full_data = {
            'user': obj.user.id,
            'name': obj.name,
            'target_per_day': obj.target_per_day,
        }
        full_data.update(new_data)

        form = HabitsForm(full_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def delete(self, request, habit_id):
        obj = get_object_or_404(Habits, id=habit_id)
        obj.delete()
        return JsonResponse({'status': 'deleted', 'id': habit_id})


# 5. GET/POST/PUT/PATCH/DELETE /habits/<id>/schedule
@method_decorator(csrf_exempt, 'dispatch')
class HabitScheduleView(View):
    def get(self, request, habit_id):
        schedules = HabitSchedule.objects.filter(habit_id=habit_id)
        schedule_list = [{'id': s.id, 'repeat_time': s.repeat_time} for s in schedules]
        return JsonResponse({'data': schedule_list})

    def post(self, request, habit_id):
        new_data = loads(request.body)
        new_data['habit'] = habit_id
        form = HabitScheduleForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def put(self, request, habit_id):
        obj = get_object_or_404(HabitSchedule, habit_id=habit_id)
        new_data = loads(request.body)
        form = HabitScheduleForm(new_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def patch(self, request, habit_id):
        obj = get_object_or_404(HabitSchedule, habit_id=habit_id)
        new_data = loads(request.body)

        full_data = {
            'habit': obj.habit.id,
            'repeat_time': obj.repeat_time,
        }
        full_data.update(new_data)

        form = HabitScheduleForm(full_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def delete(self, request, habit_id):
        obj = get_object_or_404(HabitSchedule, habit_id=habit_id)
        obj.delete()
        return JsonResponse({'status': 'deleted', 'id': habit_id})


# 6. GET/POST/PUT/PATCH/DELETE /habits/<id>/completions
@method_decorator(csrf_exempt, 'dispatch')
class HabitCompletionsView(View):
    def get(self, request, habit_id):
        completions = Completion.objects.filter(habit_id=habit_id)
        completion_list = [{'id': c.id, 'completed_at': c.completed_at} for c in completions]
        return JsonResponse({'data': completion_list})

    def post(self, request, habit_id):
        new_data = loads(request.body)
        new_data['habit'] = habit_id
        form = CompletionForm(new_data)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def put(self, request, habit_id):
        obj = get_object_or_404(Completion, habit_id=habit_id)
        new_data = loads(request.body)
        form = CompletionForm(new_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def patch(self, request, habit_id):
        obj = get_object_or_404(Completion, habit_id=habit_id)
        new_data = loads(request.body)

        full_data = {
            'habit': obj.habit.id,
        }
        full_data.update(new_data)

        form = CompletionForm(full_data, instance=obj)
        if form.is_valid():
            form.save()
            return self.get(request, habit_id)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    def delete(self, request, habit_id):
        obj = get_object_or_404(Completion, habit_id=habit_id)
        obj.delete()
        return JsonResponse({'status': 'deleted', 'id': habit_id})


# 7. GET /habits/<id>/stats
class HabitStatsView(View):
    def get(self, request, habit_id):
        count = Completion.objects.filter(habit_id=habit_id).count()
        return JsonResponse({'habit_id': habit_id, 'total_completions': count})


# 8. GET /users/<id>/stats
class UserStatsView(View):
    def get(self, request, user_id):
        total_habits = Habits.objects.filter(user_id=user_id).count()
        total_completions = Completion.objects.filter(habit__user_id=user_id).count()
        return JsonResponse({
            'user_id': user_id,
            'total_habits': total_habits,
            'total_completions': total_completions,
        })