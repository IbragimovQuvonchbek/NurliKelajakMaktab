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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import pandas as pd
from django.http import HttpResponse
from django.views import View
from django.apps import apps


class ExportAllDataView(View):
    def get(self, request, *args, **kwargs):
        # Get all models
        models = apps.get_models()

        # Create a Pandas Excel writer object
        with pd.ExcelWriter('database_dump.xlsx', engine='openpyxl') as writer:
            # Iterate over each model
            for model in models:
                # Query all data from the model
                data = model.objects.all().values()

                # If there's no data, skip
                if not data:
                    continue

                # Convert the data to a DataFrame
                df = pd.DataFrame(list(data))

                # Write the DataFrame to the Excel file with the model name as the sheet name
                df.to_excel(writer, sheet_name=model._meta.model_name, index=False)

        # Read the Excel file into memory
        with open('database_dump.xlsx', 'rb') as f:
            excel_data = f.read()

        # Create the HTTP response
        response = HttpResponse(excel_data,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=database_dump.xlsx'

        return response


urlpatterns = [
    path('', admin.site.urls),
    path('/api/v1/olimpiada25082024/'),
    path('export-all-data/', ExportAllDataView.as_view(), name='export-all-data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
