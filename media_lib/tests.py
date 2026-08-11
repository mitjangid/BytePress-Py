from django.test import TestCase
from media_lib.models import MediaAsset, VideoEmbed, VideoPlatform

class MediaLibTests(TestCase):

    def test_video_embed_youtube_parser(self):
        video = VideoEmbed.objects.create(
            title='Breaking Report Video',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        self.assertEqual(video.platform, VideoPlatform.YOUTUBE)
        self.assertEqual(video.embed_id, 'dQw4w9WgXcQ')
        self.assertEqual(video.thumbnail_url, 'https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg')
