from django.contrib import admin

from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, UserAchievement, Achievement

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(Form)
admin.site.register(UserPlan)
admin.site.register(UserHabit)
admin.site.register(Achievement)
admin.site.register(UserAchievement)

