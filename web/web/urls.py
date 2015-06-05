from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ubt/', include('ubt.urls')),

    url(r'^login/$', 'account.views.login'),
    url(r'^logout/$', 'account.views.logout'),
    url(r'^send/validation/code/$', 'account.views.send_validation_code'),
    url(r'^profile/$', 'account.views.profile'),

    url(r'^$', 'excel.views.search'),
    url(r'^manage/$', 'excel.views.manage'),

    url(r'^upload/$', 'excel.views.upload'),
    url(r'^download/(\d+)/$', 'excel.views.download'),
    url(r'^detail/(\d+)/$', 'excel.views.detail'),

    url(r'^index/(\d+)/$', 'excel.views.index'),    
    url(r'^unindex/(\d+)/$', 'excel.views.unindex'),

    url(r'^check/$', 'excel.views.check_resource'),

    url(r'^ask/$', 'excel.views.ask'),
    url(r'^record/$', 'excel.views.record'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
