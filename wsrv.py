#!/usr/bin/python

#logger definitions
import os
from os.path import expanduser
logpath = os.path.join(expanduser("~"), r"neterra.log")
import logging
logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(levelname)s\t%(asctime)s %(name)s\t\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("wsrv.py")

from urlparse import parse_qs
import neterra

class Wsrv:
    def __call__(self, environ, start_response):
        params = parse_qs(environ.get('QUERY_STRING'))
        start_response('200 Ok', [('Content-type', 'text/plain')])
        return ['I am an on-demand m3u8 playlist/playback daemon for Neterra.tv.']    
    
class NeterraMiddlware:
    
    def __init__(self, app):
        self.app = app
        self.net = neterra.NeterraProxy()
       
#     def __call__(self, environ, start_response):  #this is a method to output the whole environment dictionary   
#         # Sorting and stringifying the environment key, value pairs
#         response_body = [
#             '%s: %s' % (key, value) for key, value in sorted(environ.items())
#         ]
#         response_body = '\n'.join(response_body)
#     
#         status = '200 OK'
#         response_headers = [
#             ('Content-Type', 'text/plain'),
#             ('Content-Length', str(len(response_body)))
#         ]
#         start_response(status, response_headers)
#     
#         return [response_body]

    def __call__(self, environ, start_response):
        call = environ['PATH_INFO'][1:] #without the first char (/)
        
        if call in ['epg.xml']:
            logging.info('serving EPG')
            status = '302 Found'
            response_headers= [('Content-type', 'application/xml'),('Location', 'http://epg.kodibg.org/dl.php')]
            response=""
        elif call in ['playlist.m3u8']:
            query = environ['QUERY_STRING']
            #provide the server address to the neterra instance as they will be needed for the link generation
            self.net.host = environ['HTTP_HOST']
            if len(query)==0:
                #fresh authentication every time playlist is served         
                if self.net.authenticate():
                    logger.info('Now serving playlist')                
                    status = '200 OK'
                    response = self.net.getM3U8()
                    response_headers = [('Content-Type', 'application/x-mpegURL'),\
                                        ('Content-Disposition', 'attachment; filename=\"playlist.m3u8\"')]
                else:
                    logger.info('Failed to login. Check username and password.')
            else:
                param_dict = parse_qs(query)
                ch = param_dict.get('ch', [''])[0]  #Returns channel id
                chn = param_dict.get('name', [''])[0] #Returns channel name
                chlink = self.net.getPlayLink(ch)
                logger.info(('serving stream of channel \"{0}\" with id:\"{2}. The link is: \"{1}\".').format(chn, chlink, ch)) 
                #status = '302 Found'                
                #response = ""     
                #response_headers = [('Content-Type', 'application/x-mpegURL'),('Location', str(chlink))]
                status = '200 OK'
                response = 'the link to play channel {0} is \"{1}\".'.format(chn, chlink) 
                response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(response)))]
        else:
            response='return error for wrong call here'
            logger.debug('server was called with wrong argument: {0}'.format(environ['PATH_INFO']))
            status = '200 OK'
            response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(response)))]

        start_response(status, response_headers)   
        return [response]
    
    
if __name__ == "__main__":
    try:
        from wsgiref.simple_server import make_server
        application = NeterraMiddlware(Wsrv())
        httpd = make_server('', 8080, application)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')