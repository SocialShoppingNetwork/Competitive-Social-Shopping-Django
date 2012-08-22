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
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib import messages
from annoying.decorators import render_to
from gdata.youtube.service import YouTubeService
from annoying.decorators import render_to, ajax_request

from testimonials.utils.loader import load_path_attr
from auctions.models import Auction
from testimonials.models import Video
from testimonials.forms import ReviewForm

import base64
import hmac, sha

def generate_form():
    AWS_KEY = 'AKIAJ4PKN5RE7BF557BA'
    AWS_SECRET_KEY = """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"""
    bucket_name = "videuploadertest1"

    policy_document = """{"expiration": "2013-01-01T00:00:00Z",
      "conditions": [
        {"bucket": "videuploadertest1"},
        ["starts-with", "$key", "uploads/"],
        {"acl": "private"},
        {"success_action_redirect": "http://testing.exhibia.com:8000/"},
        ["starts-with", "$Content-Type", ""],
        ["content-length-range", 0, 1048576],
        [ "eq", "$x-amz-meta-price", "\$10.00" ],
      ]
    }"""
    policy = base64.b64encode(policy_document).replace("\n","")

    signature = base64.b64encode(
        hmac.new(AWS_SECRET_KEY, policy, sha).digest()).replace("\n","")


    return html %({'aws_key':AWS_KEY,
                   'policy':policy,
                   'signature':signature,
                   'bucket':bucket_name})

import datetime
@render_to('testimonials/upload.html')
def uploadx(request):
    AWS_KEY = 'AKIAJ4PKN5RE7BF557BA'
    AWS_SECRET_KEY = """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"""
    bucket_name = "videuploadertest1"

    policy_document = """{"expiration": "2013-01-01T00:00:00Z",
          "conditions": [
            {"bucket": "videuploadertest1"},
            ["starts-with", "$key", "uploads/"],
            {"acl": "private"},
            {"success_action_redirect": "http://testing.exhibia.com:8000/"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, 1048576],
            [ "eq", "$x-amz-meta-price", "\$10.00"]
          ]
        }"""
    policy_document = {
        'expiration': "2013-01-01T00:00:00Z",
        'conditions': [{"bucket": "videuploadertest1"},
            ["starts-with", "$key", "uploads/"],
                {"acl": "private"},
                {"success_action_redirect": "http://testing.exhibia.com:8000/"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, 1048576],
            [ "eq", "$x-amz-meta-price", "10.00"]
        ]
    }
    import cjson

    policy_document  = cjson.encode(policy_document)
    policy = base64.b64encode(policy_document).replace("\n","")

    signature = base64.b64encode(hmac.new(AWS_SECRET_KEY, policy, sha).digest()).replace("\n","")
    return {'bucket':bucket_name,
            "ajax":"ajax",
            'aws_key':AWS_KEY,
            'policy':policy,
            'signature':signature,}




@login_required
@render_to('testimonials/upload.html')
def upload(request):
    member = request.user.get_profile()
    id = request.GET.get('id')
    auction = get_object_or_404(Auction, id=id)
    #if not auction.is_ended or auction.last_bidder_member!=member:
    #    return HttpResponseForbidden()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            file = request.FILES['video']
            Video.objects.get_or_create(auction=auction,
                defaults={'review':data['review'],
                         'rated':data['rated'],
                         'share_on_facebook':data['share_facebook'],
                         'share_on_twitter':data['share_twitter'],
                         'file':file,
                         'member':member
            })
            messages.success(request, 'Video Uploaded')
            return HttpResponseRedirect('/')
    else:
        form = ReviewForm()
    return {'form':form,
            'auction': auction}
