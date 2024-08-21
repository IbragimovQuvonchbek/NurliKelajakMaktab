"""
URL configuration for NurliKelajakMaktab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import pandas as pd
from django.http import HttpResponse
from django.views import View
from django.apps import apps

class ExportAllDataView(View):
    def get(self, request, *args, **kwargs):
        models = apps.get_models()

        with pd.ExcelWriter('database_dump.xlsx', engine='openpyxl') as writer:
            for model in models:
                try:
                    data = model.objects.all().values()
                    if not data:
                        continue

                    # Convert data to a DataFrame
                    df = pd.DataFrame(list(data))

                    # Convert timezone-aware datetimes to timezone-naive datetimes
                    for col in df.select_dtypes(include=['datetimetz']).columns:
                        df[col] = df[col].apply(lambda x: x.tz_convert(None) if x.tzinfo is not None else x)

                    df.to_excel(writer, sheet_name=model._meta.model_name, index=False)

                except Exception as e:
                    print(f"Error processing model {model._meta.model_name}: {e}")
                    continue

        with open('database_dump.xlsx', 'rb') as f:
            excel_data = f.read()

        response = HttpResponse(excel_data,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=database_dump.xlsx'

        return response


urlpatterns = [
    path('api/v1/olimpiada25082024/', include('olympia.urls')),
    path('export-all-data/', ExportAllDataView.as_view(), name='export-all-data'),
    path('api/v1/testchecker/', include('customtest.urls')),
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
