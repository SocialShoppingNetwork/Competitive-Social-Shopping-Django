from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("chat.views",
    url(r"^send-message/$", "send_message", name="chat_send_message"),
    url(r"^ban-user/$", "ban_user", name="chat_ban_user"),
    url(r"^unban-user/$", "unban_user", name="chat_unban_user"),
)