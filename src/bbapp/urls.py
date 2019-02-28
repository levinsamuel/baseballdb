from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:player_id>/', views.player_page, name='player'),
    path('<int:player_id>/batting', views.batting, name='batting'),
    path('<int:player_id>/pitching', views.pitching, name='pitching'),
]
