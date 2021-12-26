from django.urls import path
from django.views.generic import TemplateView

app_name = 'testapp'

urlpatterns = [

    path('', TemplateView.as_view(template_name='testapp/home.html'), name=''),
    path('', TemplateView.as_view(template_name='testapp/home.html'), name='home'),
    path('', TemplateView.as_view(template_name='testapp/home.html'), name='index'),

]
