from django import urls
from django.urls import path
from .views import gold_price_view
urlpatterns =[
     path('gold-price' , gold_price_view , name='gold_price_view')
]
