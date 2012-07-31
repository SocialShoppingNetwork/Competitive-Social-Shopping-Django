import os
import gdata

import django
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response

from annoying.decorators import render_to
from gdata.youtube.service import YouTubeService

from testimonials.utils.loader import load_path_attr
from auctions.models import Auction
from testimonials.models import Video
VIDEO_CATEGORIES = (('Film', 'Film & Animation'),
('Autos','Autos'),
('Music', 'Music'),
('Animals', 'Animals'),
('Sports', 'Sports'),
('Travel', 'Travel'),
('Games', 'Gaming'),
('Comedy', 'Comedy'),
('People', 'People'),
('News', 'News & Politics'),
('Entertainment', 'Entertainment'),
('Education', 'Education'),
('Howto', 'Howto & Style'),
('Nonprofit', 'Nonprofits & Activism'),
('Tech', 'Science & Technology'))

VIDEO_CATEGORIES_DICT = dict(VIDEO_CATEGORIES)

class YoutubeClientLogin(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
    title = forms.CharField(max_length=250, required=False)
    description = forms.CharField(max_length=500, widget=forms.TextInput, required=False)
    category = forms.ChoiceField(choices=VIDEO_CATEGORIES, initial='People')


def media(request, path):
    root = getattr(settings, 'VIDEO_MANAGER_MEDIA_ROOT', None)
    if root is None:
        parent = os.path.abspath(os.path.dirname(__file__))
        root = os.path.join(parent, 'media', 'video_manager')
    return django.views.static.serve(request, path, root)

def video_id_fn(request):
    return 'new%s' % request.user.username

def video_save_fn(request):
    stream_name = request.GET.get('streamName')
    file_path = '%s%s.flv' % (settings.RED5_STREAM_PATH, stream_name)
    print dict(request.GET)
    return True

def video_snapshot_fn(request):
    return True

def video_id_fn(request):
    return 'abc'

def default_video_id_fn(request):
    return '54'

def get_params(request):
    params = ''
    for key in request.GET.keys():
        for value in request.GET.getlist(key):
            if not params:
                params = '?' + key + '=' + smart_unicode(value)
            else:
                params += '&amp;' + key + '=' + smart_unicode(value)
    return params

@csrf_exempt
def record_media(request, path, ext):
    base_url = settings.MEDIA_URL
    if settings.DEBUG:
        base_url = settings.STATIC_URL
    return HttpResponseRedirect('%shdfvr/%s%s%s' % (base_url, path, ext, get_params(request)))


def default_snapshot(request):
    photoName = request.GET.get("name")
    print photoName
    return True

@csrf_exempt
def save_snapshot(request):
    config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
    video_snapshot_fn = default_snapshot
    if config:
        if config.has_key("VIDEO_SNAPSHOT_FN"):
            video_snapshot_fn = load_path_attr(config["VIDEO_SNAPSHOT_FN"])
    if video_snapshot_fn(request):
        return HttpResponse('save=ok')
    return HttpResponse('save=failed')


def default_save_video(request):
    streamName = request.GET.get('streamName')
    streamDuration = request.GET.get('streamDuration')
    user_id = request.GET.get('userId')
    print streamName
    print streamDuration
    print user_id
    return True

def save_video(request):
    config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
    video_save_fn = default_save_video
    if config:
        if config.has_key("VIDEO_SAVE_FN"):
            video_save_fn = load_path_attr(config["VIDEO_SAVE_FN"])
    if video_save_fn(request):
        return HttpResponse('save=ok')
    return HttpResponse('save=failed')


def upload_to_youtube(username, password, video_file,
                      title='Untitled', description='no description', category='People',
                      tags=[], content_type='video/quicktime'):
    config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
    service = YouTubeService(email=username, password=password, developer_key=config.get('DEVELOPER_KEY', ''),
                               client_id=config.get('CLIENT_ID', ''), source=config.get('SOURCE', ''))
    my_media_group = gdata.media.Group(title=gdata.media.Title(text=title),
                                    description=gdata.media.Description(description_type='plain',
                                                                        text=description),
                                    category=[gdata.media.Category(
                                            text=category,
                                            scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                            label=VIDEO_CATEGORIES_DICT[category].replace('&','&amp;'))],
        player=None
    )

    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
    video_entry.AddDeveloperTags(tags)
    service.ProgrammaticLogin()
    new_entry = service.InsertVideoEntry(video_entry, video_file, content_type=content_type)
    return new_entry.GetAlternateLink().href


def default_video_id_fn(request):
    return request.user.username

@login_required
@render_to('video_manager/video_record2.html')
def record_video(request):
    config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
    video_id_fn = default_video_id_fn
    auction = Auction.objects.live()[0]
    if config:
        if config.has_key("VIDEO_ID_FN"):
            video_id_fn = load_path_attr(config["VIDEO_ID_FN"])
    return dict(rtmp_server=config.get('RTMP_SERVER', 'rtmp://localhost/myapp/'), video_id=video_id_fn(request),
                auction=auction)

@login_required
@render_to('video_manager/youtube_auth.html')
def xsend_video(request):
    is_ajax = request.is_ajax()
    if request.method == "POST":
        video_id = request.POST.get('video_id')
        form = YoutubeClientLogin(request.POST)
        if form.is_valid():
            if is_ajax:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                title = form.cleaned_data['title'] or 'Untitled'
                description = form.cleaned_data['description'] or 'no description'
                category = form.cleaned_data['category'] or 'People'
                config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
                file = default_storage.path('%s/%s.flv' % (config.get('VIDEO_PATH', ''), video_id))
                try:
                    url = upload_to_youtube(video_file=file, username=username, password=password,
                                        title=title, description=description, category=category,
                                        content_type='video/x-flv')
                    return HttpResponse(simplejson.dumps(dict(success=True, url=url)))
                except Exception, ex:
                    return HttpResponse(simplejson.dumps(dict(success=False, error_type='youtube', errors=str(ex))))
        else:
            if is_ajax:
                return HttpResponse(simplejson.dumps(dict(success=False, error_type='form', errors=form.errors)))
    else:
        form = YoutubeClientLogin()
        video_id = request.GET.get('video_id')
    result = dict(form=form, is_ajax=is_ajax, video_id=video_id)
    result['BASE_URL'] = request.META.get('SCRIPT_NAME', '').replace('video/send/', '')
    if is_ajax:
        result['TEMPLATE'] = 'video_manager/youtube_auth_form.html'
    return result
@csrf_exempt
@login_required
@render_to('video_manager/youtube_auth.html')
def send_video(request):
    member = request.member
    config = getattr(settings, 'VIDEO_MANAGER_CONFIG', {})
    if request.method == "POST":
        auction_id = request.POST.get('auction')
        auction = get_object_or_404(Auction, id=auction_id)
        #if auction.status not in ['e','f']:
        #    raise Http404
        #file = default_storage.path('%s/%s.flv' % (config.get('VIDEO_PATH', ''), auction_id))
        stream_name = request.POST.get('stream')
        file_path = '%s%s.flv' % (settings.RED5_STREAM_PATH, stream_name)
        video = Video(member=member,
                      auction=auction,
                      title=auction.item.name,
                      description='')
        video.file.save(name='auction_%s.flv' % auction_id, content=File(open(file_path)))
        video.save()
    return HttpResponse('hi')