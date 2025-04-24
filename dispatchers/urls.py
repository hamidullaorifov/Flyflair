from django.urls import path
from . import views

urlpatterns = [
    path('create', views.handover_view_create, name='handover'),
    path('view', views.handover_viewer_view, name='handover_view'),
    path("load-previous-data/", views.previous_data_loader, name="load_previous_day"),
    path("view/selection/", views.handover_view_selection, name='handover_viewer_selection'),

]

