from django.conf.urls import url
from django.contrib import admin
from steamCard import views as steamCard_views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', steamCard_views.getSteamCard, name='main'),
]
