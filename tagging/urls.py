from django.conf.urls import url
from . import views

app_name = 'tagging'

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^label/$', views.label, name="label"),
            url(r'^login/$', views.user_login, name="login"),
            url(r'^logout/$', views.user_logout, name="logout"),
            url(r'^register/$', views.user_register, name="logout"),
            url(r'^check/$', views.check_user, name="check_user")
            ]
