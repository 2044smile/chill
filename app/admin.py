from django.contrib import admin

from .models import Hall


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'student_list', 'attend_code', 'is_closed']

    def student_list(self, obj):
        return ",\n".join([i.user_id for i in obj.students.all()])
