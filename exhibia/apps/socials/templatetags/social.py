import datetime
import settings
from django import template
from django.core.urlresolvers import reverse

from annoying.functions import get_object_or_None
from socials.models import LikeItem

register = template.Library()

def google_plus_one_item(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, item, callback, annotation, size = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])

    if not (callback[0] == callback[-1] and callback[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    if not (annotation[0] == annotation[-1] and annotation[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    if not(annotation[1:-1] in ['bubble', 'inline', 'none']):
        raise template.TemplateSyntaxError("size wrong value" % tag_name)

    if not (size[0] == size[-1] and size[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    if not(size[1:-1] in ['small', 'medium', 'standard', 'tall']):
        raise template.TemplateSyntaxError("size wrong value" % tag_name)

    return GplusNode(item, callback[1:-1], annotation[1:-1], size[1:-1])

class GplusNode(template.Node):
    def __init__(self, item, callback, annotation, size):
        self.auction = template.Variable(item)
        self.callback = callback
        self.annotation = annotation
        self.size = size

    def render(self, context):
        try:
            item = self.auction.resolve(context)
            url = item.get_full_url()
            html = """<g:plusone callback="%(callback)s" size="%(size)s" href="%(url)s" annotation="%(annotation)s"
             size="%(size)s"></g:plusone>"""
            params = {'url': url,
                      'callback': self.callback,
                      'size': self.size,
                      'annotation': self.annotation}
            return html % params
        except template.VariableDoesNotExist:
            return ''

register.tag('google_plus_one_item', google_plus_one_item)

@register.inclusion_tag('socials/fb_code.html')
def facebook_js():
    return {'fb_id':settings.FACEBOOK_APP_ID}


@register.inclusion_tag('socials/fb_like.html')
def facebook_like_item(item):
    url = item.get_full_url()
    return {'fb_id': settings.FACEBOOK_APP_ID,
            'url': url}

class IfCanLikeNode(template.Node):

    def __init__(self, nodelist_true, nodelist_false, item, type):
        print item, type

        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.item = template.Variable(item)
        if type == 'facebook':
            type = 'F'
        elif type == 'google':
            type = 'G'
        else:
            type = 'F'
        self.type = type

    def render(self, context):
        item = self.item.resolve(context)
        user = context['user']._wrapped
        member = None
        if user.is_authenticated():
            member = user.get_profile()
        like = get_object_or_None(LikeItem, item=item, member=member, type=self.type)
        if like:
            return self.nodelist_false.render(context)
        else:
            return self.nodelist_true.render(context)

@register.tag
def ifcanlike(parser, token):
    bits = token.split_contents()
    nodelist_true = parser.parse(("else", "endifcanlike"))
    token = parser.next_token()

    if token.contents == "else":
        nodelist_false = parser.parse(("endifcanlike",))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return IfCanLikeNode(nodelist_true, nodelist_false, bits[1], bits[2])
