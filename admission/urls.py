from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('<str:index_no>/', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.log_out, name='log_out'),
    path('generate_pdf/<str:index_no>', views.generate_pdf, name='generate_pdf')
]
