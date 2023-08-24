from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.log_out, name='log_out'),
    path('<path:index_no>/', views.index, name='index'),
    path('generate_pdf_kuccps/<path:index_no>', views.generate_pdf_kuccps, name='generate_pdf_kuccps'),
    path('generate_pdf_internal/<path:index_no>', views.generate_pdf_internal, name='generate_pdf_internal'),
    path('generate_pdf_postgrad/<path:index_no>', views.generate_pdf_postgrad, name='generate_pdf_postgrad'),
    path('generate_pdf_certificate/<path:index_no>', views.generate_pdf_certificate, name='generate_pdf_certificate'),
    path('generate_pdf_evening/<path:index_no>', views.generate_pdf_evening, name='generate_pdf_evening'),
    path('generate_pdf_upgrading/<path:index_no>', views.generate_pdf_upgrading, name='generate_pdf_upgrading'),
    path('generate_pdf_eldoret/<path:index_no>', views.generate_pdf_eldoret, name='generate_pdf_eldoret')
]
