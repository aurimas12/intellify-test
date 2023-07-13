from django.urls import path
from .views import *
# from .views import ProjectAPIView, get_avg_values, get_project_by_user, UserAPIView, DataPointAPIList, get_datapoint_by_id, ConfigurationView, ProjectAPIUpdate, generate_data_auth_user


urlpatterns = [

    # user
    path('register', UserAPIView.as_view({'post': 'create'})),
    path('', UserAPIView.as_view({'get': 'list'})),
    # project
    path('project/', ProjectAPIView.as_view({'get': 'list'})),
    path('project/create/', ProjectAPIView.as_view({'post': 'create'})),
    path('project/<int:pk>/', ProjectAPIView.as_view({'get': 'retrieve'})),
    path('project/detail/', get_project_by_user),

    # datapoint
    path('datapoint/', DataPointAPIList.as_view()),
    path('aggregate/', get_datapoint_by_id),

    # datapoint aggregated data
    path('datapoint/avg/', get_average),
    path('datapoint/hourly/<int:start_hour>/<int:hour_range>', get_hourly),

    # mqtt endpoint
    path('gen-data/', generate_data_auth_user),

    # config
    path('configuration/', ConfigurationView.as_view(), name='configuration'),










]
