from django.conf.urls import url
import views
import populate

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'detail', views.detail, name='detail'),
    url(r'summary', views.summary, name='summary'),
]
