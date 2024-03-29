import gzip
import requests
import re
import bz2
import shutil
import os
from datetime import datetime
import time
import sys

#to disable warnings related to https certificates verification
import urllib3
urllib3.disable_warnings()

import logging
logger = logging.getLogger("downloadepg.py")

class EPGDownloader:
    def __init__(self, script_dir):
        logging.info("EPG downloader initialised: {0}".format(str(datetime.now())))
        self.script_dir = script_dir
        #GZIP format: http://epg.kodibg.org/dl.php
        self.url = "http://epg.cloudns.org/dl.php"
        self.filename = "epg"

    def __donwload(self):
        try:
            logging.info("download started: {0}".format(str(datetime.now())))
            filename = self.script_dir + "/" + self.filename + ".xml.gz"


            # r = requests.get(self.url, allow_redirects=True)
            # with open(self.script_dir + "/" + self.filename + ".xml.bz2", "wb") as f:
            #     f.write(r.content) #tuk
            #     f.close()

            #workaround due to security constraint from kodibg.org
            #to fix for windows OS
            os.system("wget -N --tries=5 http://epg.cloudns.org/dl.php -O " + filename)
        except requests.exceptions.RequestException as err:
            print(err("message"))
            sys.exit(1)

    def extract(self):
        self.__donwload()

        epgGZipped = self.script_dir + "/" + self.filename + ".xml.gz"
        epg = self.script_dir + "/" + self.filename + ".xml"

        with gzip.open(epgGZipped, 'rb') as f_in:
             with open(epg, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

if __name__ == "__main__":
    print ("go go go")
    d = EPGDownloader('/home/ananchev')
    print (d.script_dir)
    d.extract()
