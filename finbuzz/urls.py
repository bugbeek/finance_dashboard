from django.urls import path
from . import views 

urlpatterns = [
    path('home', views.home, name='home'),
    path('topgainers', views.get_top_gainers, name='topgainers'),
    path('toplosers', views.get_top_losers, name = 'toplosers'),
    path('holidays', views.get_holidays, name='holidays'),
]
