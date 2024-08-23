from django.contrib import admin
from .models import Results, Tests, TestFile

admin.site.register(Tests)
admin.site.register(Results)
admin.site.register(TestFile)
