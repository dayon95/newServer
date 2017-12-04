from django.contrib import admin

# Register your models here.

from .models import pd1_time
from .models import pd2
from .models import feedbackpost, feedback

admin.site.register(pd1_time)
admin.site.register(pd2)

class feedbackpostAdmin(admin.ModelAdmin):
    list_display=('id','basepost')

admin.site.register(feedbackpost,feedbackpostAdmin)
admin.site.register(feedback)
