from django.urls import path, re_path
from . import views

app_name = 'admission'

urlpatterns = [
    path('<path:index_no>/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.log_out, name='log_out'),
    path('generate_pdf/<path:index_no>', views.generate_pdf, name='generate_pdf')
]
