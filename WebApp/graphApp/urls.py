from django.urls import path
from graphApp import views

app_name = 'graphApp'

urlpatterns = [
    path('data/', views.data, name='data'),
    path('sma/', views.sma, name='sma'),
    path('optimizedSma/', views.optimizedSma, name='optimizedSma'),
    path('MLBacktesting/', views.MLBacktesting, name='MLBacktesting'),
    path('optimalLags/', views.optimalLags, name='optimalLags')
]
