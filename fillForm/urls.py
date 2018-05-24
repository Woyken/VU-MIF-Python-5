from django.conf.urls import url
from . import views

app_name = 'fillForm'
urlpatterns = [
    url(r'^$', views.fill_form, name='index'),
    url(r'^forms/$', views.get_forms, name='allforms'),
    url(r'^form/(?P<formID>\d{0,10})/$', views.get_form, name='singleform'),
    url(r'^form/(?P<formID>\d{0,10})/pdf$', views.get_pdf, name='singleformpdf'),
]
