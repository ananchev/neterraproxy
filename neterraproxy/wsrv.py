#!/usr/bin/python

#logger definitions
import os
#from os.path import expanduser
#logpath = os.path.join(expanduser("~"), r"neterra.log")
#script_dir = os.path.dirname(os.path.abspath(__file__))

from urllib.parse import parse_qs

##below to be uncommented when building as module 
from neterraproxy.neterra import NeterraProxy
from neterraproxy.downloadepg import EPGDownloader

##lines below are for dev purpose only - when using startnetman
#from neterra import NeterraProxy
#from downloadepg import EPGDownloader


import logging
logger = logging.getLogger(__name__)

class Wsrv:
    def __call__(self, environ, start_response):
        params = parse_qs(environ.get('QUERY_STRING'))
        start_response('200 Ok', [('Content-type', 'text/plain')])
        return ['I am an on-demand m3u8 playlist/playback daemon for Neterra.tv.']    
    
class NeterraMiddlware:
    
    def __init__(self, app, username, password, app_dir):
        self.app = app
        self.net = NeterraProxy(username, password, app_dir)

    def __call__(self, environ, start_response):
        call = environ['PATH_INFO'][1:] #without the first char (/)
        
        if call in ['epg.xml']:
            logging.info('serving EPG')
            response = b''
            filename = self.net.app_dir + "/epg.xml"
            with open(filename, 'rb', buffering=0) as f:
                response= f.readall()
            status = '200 OK'
            response_headers =[('content-type', 'application/xml')]

        elif call in ['neterralinks.m3u8']:
            if self.net.authenticate2():
                logging.info('serving playlist with direct links')
                status = '200 OK'
                self.net.host = environ['HTTP_HOST']
                response = self.net.getM3U82(False)
                response_headers = [('Content-Type', 'application/x-mpegURL'),\
                                    ('Content-Disposition', 'attachment; filename=\"neterralinks.m3u8\"')]
            else:
                error = b'Failed to login. Check username and password.'
                logger.error(error)
                status = '200 OK'
                response = error 
                response_headers = [('Content-Type', "text/plain"),('Content-Length', str(len(response)))]                            
        
        elif call in ['playlist.m3u8']:
            query = environ['QUERY_STRING']
            #provide the server address to the neterra instance as they will be needed for the link generation
            self.net.host = environ['HTTP_HOST']
            if len(query)==0:
                #fresh authentication every time playlist is served         
                if self.net.authenticate2():
                    logger.info('Now serving playlist')
                    print('Now serving playlist')                
                    status = '200 OK'
                    response = self.net.getM3U82()
                    response_headers = [('Content-Type', 'application/x-mpegURL'),\
                                        ('Content-Disposition', 'attachment; filename=\"playlist.m3u8\"')]
                    # status = '302 Found'                
                    # response = ""     
                    # response_headers = [('Content-Type', 'application/x-mpegURL'),('Location', 'http://www.dir.bg')
                else:
                    error = b'Failed to login. Check username and password.'
                    logger.info(error)
                    print (error)
                    status = '200 OK'
                    response = error 
                    response_headers = [('Content-Type', "text/plain"),('Content-Length', str(len(response)))]
                    #response_headers = [('Content-Type', "text/plain"),('Content-Length', '50'.encode())]
            else:
                param_dict = parse_qs(query)
                ch = param_dict.get('ch', [''])[0]  #Returns channel id
                #chn = param_dict.get('name', [''])[0] #Returns channel name
                chlink = self.net.getPlayLink2(ch)
                #logger.info(('serving stream of channel \"{0}\" with id:\"{2}. The link is: \"{1}\".').format(chn, chlink, ch)) 
                print(chlink)
                status = '302 Found'                
                response = b""     
                response_headers = [('Content-Type', 'application/x-mpegURL'),('Location', str(chlink))]
                # status = '200 OK'
                # response = 'the link to play channel {0} is \"{1}\".'.format(chn, chlink) 
                # response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(response)))]
        else:
            response=b'return error for wrong call here'
            error = 'server was called with wrong argument: {0}'.format(environ['PATH_INFO'])
            logger.debug(error)
            print (error)
            status = '200 OK'
            response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(response)))]

        start_response(status, response_headers)   
        return [response]

def run(username, password, app_dir):
    logpath = app_dir + '/neterra.log'
    #logpath = "/tmp/mnt/disc0-part4/neterra_proxy/neterra.log"
    import logging
    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(levelname)s\t%(asctime)s %(name)s\t\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger("wsrv.py")

    try:
        d = EPGDownloader(app_dir)
        #download epg on first run
        d.extract()
        #initialise background scheduler to download new EPG every 4 hrs
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(d.extract, 'interval', hours=4)
        scheduler.start()

        from wsgiref.simple_server import make_server
        application = NeterraMiddlware(Wsrv(), username, password, app_dir)
        httpd = make_server('', 8080, application)
        logger.debug('Serving on port 8080...')
        httpd.serve_forever()

        while True:
            pass
    except KeyboardInterrupt:
        logger.debug('Shut down command received')
        scheduler.shutdown()

   
# if __name__ == "__main__":
#     run()
