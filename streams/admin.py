from django.contrib import admin
from .models import Stream,StreamMetric

# Register your models here.
admin.site.register(Stream)
admin.site.register(StreamMetric)