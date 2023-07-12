from django.urls import path
from .views import RegisterView, DataPointAPIList, get_datapoint_by_id, ConfigurationView, ProjectAPIUpdate, generate_data_auth_user


urlpatterns = [

    # user
    path('register', RegisterView.as_view()),
    path('configuration/', ConfigurationView.as_view(), name='configuration'),
    # project
    # path('project/', ProjectAPIUpdate.as_view()),
    path('project/<int:pk>', ProjectAPIUpdate.as_view()),
    # team
    # datapoint
    path('datapoint/', DataPointAPIList.as_view()),
    path('datapoint/<int:pk>/', get_datapoint_by_id),
    path('gen-data/', generate_data_auth_user),







]
