from django.contrib import admin
from core.models import SampleModel
# Register your models here.


@admin.register(SampleModel)
class FilterNodeAdmin(admin.ModelAdmin):
    # readonly_fields = ('exc_info', 'task')
    list_display = [f.name for f in SampleModel._meta.fields]
    #list_filter = ['task__status']

