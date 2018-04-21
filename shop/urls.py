from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<book_id>\d+)/$', views.detail, name='detail'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]
