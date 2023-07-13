from django.urls import path

from .views import (ConfigurationView, DataPointAPIList, ProjectAPIView,
                    UserAPIView, generate_data_auth_user, get_average,
                    get_datapoint_by_id, get_hourly, get_project_by_user)

urlpatterns = [
    path('register', UserAPIView.as_view({'post': 'create'})),
    path('', UserAPIView.as_view({'get': 'list'})),
    path('project/', ProjectAPIView.as_view({'get': 'list'})),
    path('project/create/', ProjectAPIView.as_view({'post': 'create'})),
    path('project/<int:pk>/', ProjectAPIView.as_view({'get': 'retrieve'})),
    path('project/detail/', get_project_by_user),
    path('datapoint/', DataPointAPIList.as_view()),
    path('datapoint/aggregate/', get_datapoint_by_id),
    path('datapoint/avg/', get_average),
    path('datapoint/hourly/<int:start_hour>/<int:hour_range>', get_hourly),
    path('datapoint/gen-data/', generate_data_auth_user),
    path('configuration/', ConfigurationView.as_view(), name='configuration')
]
