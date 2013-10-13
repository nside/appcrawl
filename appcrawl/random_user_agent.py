from appcrawl.settings import USER_AGENT_LIST
import random
from scrapy import log

class RandomUserAgentMiddleware(object):
    
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        #log.msg('>>>> UA %s'%request.headers)
