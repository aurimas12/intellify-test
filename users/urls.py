from django.urls import path
from .views import RegisterView, RetrieveUserView, DataPointAPIList, get_datapoint_by_id, get_aggregate_data, ConfigurationView, ProjectAPIUpdate


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('me', RetrieveUserView.as_view()),
    path('datapoint/', DataPointAPIList.as_view()),
    path('datapoint/<int:pk>/', get_datapoint_by_id),
    path('datapoint/agg', get_aggregate_data),
    path('configuration/', ConfigurationView.as_view(), name='configuration'),
    path('project/<int:pk>', ProjectAPIUpdate.as_view())

]
