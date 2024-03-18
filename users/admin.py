from django.contrib import admin
from .models import User, AdminProfile, LearningCenter, TeachGroup, TeacherProfile, StudentProfile


admin.site.register(User)
admin.site.register(AdminProfile)
admin.site.register(LearningCenter)
admin.site.register(TeachGroup)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)


