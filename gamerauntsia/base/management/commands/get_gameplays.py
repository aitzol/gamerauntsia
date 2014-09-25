from django.core.management.base import BaseCommand
from gamerauntsia.utils.urls import get_urljson
from gamerauntsia.gamer.models import GamerUser
from gamerauntsia.auto_gameplay.models import AutoGamePlaya
import datetime
 
def get_gameplays():
    gamers = GamerUser.objects.filter(is_gamer=True,ytube_channel__isnull=False)

    for gamer in gamers:
        user = gamer.ytube_channel.replace('http://www.youtube.com/user/','').replace('https://www.youtube.com/channel/','')
        channel = u'http://gdata.youtube.com/feeds/api/users/'+user+'/uploads?v=2&alt=json'
        data = get_urljson(channel)

        for video in data['feed']['entry'][:5]:
            print video['title']['$t']
            print video['media$group']['media$description']['$t']
            print video['media$group']['yt$videoid']['$t']
            print str(datetime.timedelta(seconds=int(video['media$group']['yt$duration']['seconds'])))
            for media in video['media$group']['media$thumbnail']:
                if media['yt$name'] == 'sddefault':
                    print media['url']
                elif media['yt$name'] == 'hqdefault':
                    print media['url']
                elif media['yt$name'] == 'default':
                    print media['url']
            print '\n'
        

class Command(BaseCommand):
    help = 'Get GPs automaticaly'
    def handle(self, *args, **options):
        get_gameplays()