from django.urls import path
from . import views

app_name = 'flights'
urlpatterns = [
    path('',views.index,name='index'),
    path('search',views.search,name='search'),
    path('add',views.add,name='add'),
    path('result/<int:flight_id>',views.result,name='result'),
    path('addpassenger',views.add_passenger,name='addpassenger'),
    path('<int:flight_id>/book',views.book,name='book'),
]

