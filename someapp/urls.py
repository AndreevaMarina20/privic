from django.urls import path
from . import views

urlpatterns = [
    # --- ПОЛЬЗОВАТЕЛИ ---

    path('users/', views.UserListView.as_view()),                              # все юзеры
    path('users/<int:user_id>/', views.UserDetailView.as_view()),              # юзер по ID
    path('users/<int:user_id>/habits/', views.UserHabitsView.as_view()),       # привычки юзера
    path('users/<int:user_id>/stats/', views.UserStatsView.as_view()),         # статистика юзера

    # --- ПРИВЫЧКИ ---

    path('habits/<int:habit_id>/', views.HabitDetailView.as_view()),           # привычка по ID
    path('habits/<int:habit_id>/schedule/', views.HabitScheduleView.as_view()), # расписание привычки
    path('habits/<int:habit_id>/completions/', views.HabitCompletionsView.as_view()), # история выполнений
    path('habits/<int:habit_id>/stats/', views.HabitStatsView.as_view()),      # статистика привычки
]