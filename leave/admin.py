from django.contrib import admin
from .models import Leave

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'reason')
    list_filter = ('leave_type', 'start_date', 'end_date')
    search_fields = ('user__username', 'leave_type', 'reason')

admin.site.register(Leave, LeaveAdmin)
