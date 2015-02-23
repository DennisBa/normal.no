# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.autodiscover()

import website.admin

urlpatterns = patterns ('',
    url(r'^$',              'core.views.index',             name='index'),
    url(r'^nyhetsbrev/$',   'core.views.newsletter',        name='newsletter'),
    url(r'^bli-medlem/$',   'apps.support.views.index',     name='enroll'),
    url(r'^medlem/$',       'apps.support.views.index'),    # alias
    url(r'^opprop/$',       'apps.support.views.petition',  name='petition'),
    url(r'^nettguide/$',    'apps.links.views.index',       name='links'),

    (r'^rss/$', RedirectView.as_view (url='/nyheter/rss/', permanent=True)),
    # Hack to redirect deprecated url's
    # Note: Does not work to urlencode; must use unicode strings.
    #(r'^m%C3%B8/$', RedirectView.as_view (url='/medlem/', permanent=True)),
    (u'^gruppesøksmaal/$', RedirectView.as_view (url='/sider/gruppesoksmaal/', permanent=True)),

    (r'^nyheter/',  include ('apps.news.urls')),
    (r'^tinymce/',  include ('tinymce4.urls')),

    # https://docs.djangoproject.com/en/1.7/topics/auth/default/
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # need registration/login.html template

    # Password reset
    url(r'^admin/password_reset/$',                             auth_views.password_reset,          name='admin_password_reset'),
    url(r'^admin/password_reset/done/$',                        auth_views.password_reset_done,     name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',  auth_views.password_reset_confirm,  name='password_reset_confirm'),
    url(r'^reset/done/$',                                       auth_views.password_reset_complete, name='password_reset_complete'),

    # Note: Must be *after* passrod reset links!
    (r'^admin/',    include (admin.site.urls)),
)


# Hack to serve MEDIA_ROOT in dev mode
# And to map a test view to /test
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns ('', url(r'^test/$', 'core.views.test'))
