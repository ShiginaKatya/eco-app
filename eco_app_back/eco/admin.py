from django.contrib import admin

from .models import User, Role, Category, Habit, Form, UserPlan, UserHabit, UserAchievement, Achievement, Task, Challenge, UserChallenge, UserTask, Level, UserStat

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(Form)
admin.site.register(UserPlan)
admin.site.register(UserHabit)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Challenge)
admin.site.register(Task)
admin.site.register(UserChallenge)
admin.site.register(UserTask)
admin.site.register(UserStat)
admin.site.register(Level)

