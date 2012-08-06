from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("chat.views",
    url(r"^send-message/$", "send_message", name="chat_send_message"),
)