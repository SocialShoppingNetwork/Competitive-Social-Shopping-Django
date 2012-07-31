from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("uploader.views",
    url(r'start$', 'start', name="start"),
    url(r'ajax-upload$', 'import_uploader', name="my_ajax_upload"),
)
