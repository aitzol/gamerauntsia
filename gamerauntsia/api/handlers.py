from piston.handler import BaseHandler
import telebot
from django.conf import settings
from gamerauntsia.zerbitzariak.models import MC_Whitelist

class MCHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = MC_Whitelist  
   fields = ('mc_user','created','uuid','rol') 

   def read(self, request, username=None):
        """
        Returns a single post if `blogpost_id` is given,
        otherwise a subset.

        """
        base = MC_Whitelist.objects
        
        if username:
        	try:
	            mc = base.get(mc_user=username)
	            data = {
	                'user': mc.user.username,
	                'mc_user': mc.mc_user,
	        		'created': mc.created.strftime("%Y-%m-%d %H:%M:%S"),
	                'rol': mc.get_rol_display(),
	                'uuid': mc.uuid,
	        	}
	            return data
	        except:
	        	return False
        else:
            return False
            
class MCTelebotHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = MC_Whitelist  
   fields = ('mc_user','created','uuid','rol') 

   def read(self, request, username=None):
        
        base = MC_Whitelist.objects
        
        if username:
        	try:
	            mc = base.get(mc_user=username)
	            tb = telebot.TeleBot(settings.TELEBOT_TOKEN)
	            msg = '[%s] %s-(r)en laguntza eskaera:\n%s' % (mc.get_rol_display(),username,request.GET.get('text', 'Mezurik gabe...'))
	            tb.send_message(settings.MC_CHAT_ID, msg)
	            return True
	        except:
	        	return False
        else:
            return False
