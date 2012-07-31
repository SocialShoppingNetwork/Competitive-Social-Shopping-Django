from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

_PREFIX = '__testimonials__'

urlpatterns = patterns("testimonials.views",
    url(r'^%s/m/(.*)$' % _PREFIX, 'media'),
    url(r"^video/record/$", 'record_video', name="record_video"),
    url(r"^video/send/$", "send_video", name="send_video"),
    url(r"^video/record/jpg_encoder_download.php$", "save_snapshot", name="save_snapshot"),
    url(r"^video/record/save_video_to_db.php$", "save_video", name="save_video"),
    url(r"^video/record/(?P<path>.*)(?P<ext>\.php|.xml|.png)$", 'record_media', name="record_media"),
)
  