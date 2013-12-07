#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__author__ = 'wxg (wxg4net@gmail.com)'

import sys
import argparse
import pynotify

from weibo.weibo import APIClient
from weibo.weibotools import authorize_clent

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('--auth_host_name', default='localhost' , required=False,
                        help='Hostname when running a local web server.')
argparser.add_argument('--noauth_local_webserver' , required=False,
                        default=False, help='Do not run a local web server.')
argparser.add_argument('--auth_host_port', default=8090, type=int, required=False,
                        help='Port web server should listen on.')
argparser.add_argument('--logging_level', default='ERROR', required=False,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL'],
                        help='Set the logging level of detail.')
argparser.add_argument("-f", dest="filename",  required=True,
                  help="write report to FILE", metavar="FILE")  
                  
flags = argparser.parse_args(sys.argv[1:])

def main():
  c = APIClient('2271670378', '81de0a49e985565466e708148544a3d8', 'http://127.0.0.1:8090/do/')
  c = authorize_clent(c, flags)
 
  with open(flags.filename, mode='rb') as file:
    fileContent = file.read()
    
  try:
    r = c.statuses.upload.post(status=u'图片预览', pic=StringIO(fileContent))
    title =  u'图片上传提醒'
    rr = c.short_url.shorten.get(url_long=r['original_pic'])
    body = rr['urls'][0]['url_short']
    print body
  except:
    title =  u'图片上传提醒'
    body =    u'上传图片失败'
    
  pynotify.init ("pic-notice")
  n = pynotify.Notification (title, body)
  n.set_timeout(2000)
  n.show()

if __name__=='__main__':
  main()