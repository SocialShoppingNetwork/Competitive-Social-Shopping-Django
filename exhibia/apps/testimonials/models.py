import gdata
import mimetypes

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson
from gdata.youtube.service import YouTubeService

from ndevs.social.facebook import FacebookApi


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

class Video(models.Model):
    member = models.ForeignKey('profiles.Member', related_name='testimonials')
    auction = models.ForeignKey('auctions.Auction', related_name='testimonials')
    #item = models.ForeignKey(Item, related_name='videos')
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='item_videos')
    youtube_url = models.URLField(verify_exists=False)
    facebook_video_id = models.CharField(max_length=500, blank=True, null=True)
    facebook_video_info = models.TextField(blank=True, null=True)
    facebook_page_video_id = models.CharField(max_length=500, blank=True, null=True)
    facebook_page_video_info = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('member', 'auction')
    def upload_record(self, file, type='flv'):
        if self.file:
            self.file.delete()
        name = '%s.%s' % (self.id, type)
        if self.file:
            name = '%s.%s' % (self.file.name, type)
        self.file.save(name=name, content=file)

    def upload_to_youtube(self, category='People', tags=[]):
        if self.file:
            try:
                content_type = mimetypes.guess_type(self.file.name)[0]
            except IndexError:
                content_type = 'video/quicktime'
            config = getattr(settings, 'SOCIAL_ACCOUNTS', {}).get('youtube')
            service = YouTubeService(email=config.get('USERNAME'), password=config.get('PASSWORD'),
                                     developer_key=config.get('DEVELOPER_KEY'), client_id=config.get('CLIENT_ID'),
                                     source=config.get('SOURCE'))
            my_media_group = gdata.media.Group(title=gdata.media.Title(text=self.title or '%s' % self.id),
                                        description=gdata.media.Description(description_type='plain',
                                                                            text=self.description or 'No Description'),
                                        category=[gdata.media.Category(
                                                text=category,
                                                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                label=VIDEO_CATEGORIES_DICT[category].replace('&','&amp;'))],
                            player=None
            )
            print content_type
            video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
            video_entry.AddDeveloperTags(tags)
            service.ProgrammaticLogin()
            new_entry = service.InsertVideoEntry(video_entry, self.file.path, content_type=content_type)
            self.youtube_url = new_entry.GetAlternateLink().href
            self.save()

    def upload_to_facebook(self):
        if self.file:
            config = getattr(settings, 'SOCIAL_ACCOUNTS', {}).get('facebook')
            api = FacebookApi(access_token_str=config.get('ACCESS_TOKEN'), consumer_key=config.get('API_ID'),
                              consumer_secret=config.get('API_SECRET'))
            result = api.video.upload(video_file=self.file, title=self.title or '%s' % self.id,
                             description=self.description or '')
            print result
            self.facebook_video_id = result['id']
            self.save()
            self.facebook_video_info = simplejson.dumps(api.video.get_info(self.facebook_video_id))
            self.save()

    def upload_to_facebook_page(self):
        if self.file:
            config = getattr(settings, 'SOCIAL_ACCOUNTS', {}).get('facebook')
            api = FacebookApi(access_token_str=config.get('PAGE_ACCESS_TOKEN'), consumer_key=config.get('API_ID'),
                              consumer_secret=config.get('API_SECRET'))
            result = api.video.upload(video_file=self.file.file, title=self.title or '%s' % self.id,
                             description=self.description or '', username=config.get('PAGE_ID'))
            self.facebook_page_video_id = result['id']
            self.save()
            self.facebook_page_video_info = simplejson.dumps(api.video.get_info(self.facebook_page_video_id))
            self.save()