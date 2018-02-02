#!/usr/bin/python
import requests
import cookielib
import time

import logging
logger = logging.getLogger("neterra.py")

from urllib2 import HTTPPasswordMgr
from cookielib import CookieJar
from telnetlib import theNULL

#to disable warnings related to https certificates verification
import urllib3
urllib3.disable_warnings()

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape



class NeterraProxy(object):

    def __init__(self):
        self.username = "ananchev"
        self.password = "7C8UCskhbt8Gdvd4OCKc"
        #self.cookieJar = cookielib.CookieJar()
        self.session = requests.Session()
        self.expireTime = 0
        #client 
        #channelsJson
        
    def checkAuthentication(self):
        now = int(time.time() * 1000)
        if now > self.expireTime:
            self.authenticate()
    
    def authenticate(self):
        logger.info('authenticating...')
        logged = False
        self.session.cookies.clear()
        url = "http://www.neterra.tv/user/login_page"
        formBody = {"login_username": self.username, \
                    "login_password": self.password, \
                    "login" : "1", \
                    "login_type" : "1"}
        try:
            r = self.session.post(url, data = formBody) #the session now contains the cookies provided in .cookies
            logged = "var LOGGED = '1'" in r.content
        except requests.exceptions.RequestException as err:
            logger.exception("message")
            sys.exit(1)
            
        if logged:
            self.expiretime = int(time.time() * 1000) + 28800000
        return logged
    
    def getM3U8(self):
        r = self.session.get('http://www.neterra.tv/content/live')
        import json
        from cStringIO import StringIO
        sb = StringIO()
        sb.write("#EXTM3U\n")
        for channel in r.json()['tv_choice_result']:
            #issues_name = channel[0]['issues_name'].encode("utf-8")
            issues_name = channel[0]['media_file_tag']
            issues_id = channel[0]['issues_id']
            tvg_id = channel[0]['product_epg_media_id']
            tvg_name = channel[0]['media_file_tag']
            tvg_logo = channel[0]['product_big_pic']
            group_id = channel[0]['product_group_id']
            chdata = "#EXTINF:-1 tvg-id=\"{0}\" tvg-name=\"{1}\" tvg-logo=\"{2}\" group-id=\"{3}\" {4} \n http://{5}/playlist.m3u8?ch={6}&name={7}\n"\
            .format(tvg_id, tvg_name,'',group_id,issues_name,self.host,issues_id,tvg_name)
            sb.write(chdata.encode("utf-8"))
        
        # import io
        # with io.open('playlist.m3u8', 'w', encoding='utf8') as text_file:
        #     text_file.write(unicode(str(sb)))
        
        return sb.getvalue()     


    def __getStream(self, issueId):
        self.checkAuthentication()
        data = {'issue_id':issueId, 'quality':'0', 'type':'live'}
        sr = self.session.post('http://www.neterra.tv/content/get_stream', data=data)
        
        # playLinkJson = sr.json()
        # import json, io
        # with io.open('playLinkJson.json','w',encoding="utf-8") as outfile:
        #     outfile.write(unicode(json.dumps(playLinkJson, ensure_ascii=False)))
        
        return sr.json()

    def getPlayLink(self, issueId):
        playLinkJson = self.__getStream(issueId)
        raw_link = playLinkJson['play_link']
        # #Cleanup DVR features in live stream that were causing problems for some channels
        # clean_link = raw_link.replace(':443','').replace('DVR&','').replace('/dvr','/live')
        # return clean_link
        return raw_link



