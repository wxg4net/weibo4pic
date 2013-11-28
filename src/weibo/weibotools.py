#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import BaseHTTPServer
import logging
import sys
import os
import socket
import time
import json
import webbrowser
from weibo import _parse_json

try:
  from urlparse import parse_qsl
except ImportError:
  from cgi import parse_qsl


class ClientRedirectServer(BaseHTTPServer.HTTPServer):
  """A server to handle OAuth 2.0 redirects back to localhost.

  Waits for a single request and parses the query parameters
  into query_params and then stops serving.
  """
  query_params = {}


class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  """A handler for OAuth 2.0 redirects back to localhost.

  Waits for a single request and parses the query parameters
  into the servers query_params and then stops serving.
  """

  def do_GET(s):
    """Handle a GET request.

    Parses the query parameters and prints a message
    if the flow has completed. Note that we can't detect
    if an error occurred.
    """
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    query = s.path.split('?', 1)[-1]
    query = dict(parse_qsl(query))
    s.server.query_params = query
    s.wfile.write("<html><head><title>Authentication Status</title></head>")
    s.wfile.write("<body><p>The authentication flow has completed.</p>")
    s.wfile.write("</body></html>")

  def log_message(self, format, *args):
    """Do not log messages to stdout while running as command line program."""
    pass
    

def _authorize_clent(client, data):
  client.access_token = data.access_token
  client.expires = data.expires
  return client
  
def authorize_clent(client, flags):

  logging.getLogger().setLevel(getattr(logging, flags.logging_level))
  
  user_data_dir = os.sep.join([os.getenv("HOME"), '.weibo4pic'])
  if not os.path.isdir(user_data_dir):
    try:
      os.mkdir(user_data_dir)
    except:
      raise Exception('OSError')
  

  client_access_token_file = os.sep.join([user_data_dir, 'client_access_token.json'])
  try:
    f = open(client_access_token_file, 'r')
    data = f.readline()
    f.close()
    
    obj_data = _parse_json(data)
    client = _authorize_clent(client, obj_data)
    if client.expires > time.time():
      return client
    else:
      pass
  except:
    pass

  
  if not flags.noauth_local_webserver:
    success = False
    port_number = flags.auth_host_port
    try:
      httpd = ClientRedirectServer((flags.auth_host_name, port_number),
                                   ClientRedirectHandler)
    except socket.error, e:
      pass
    else:
      success = True
    flags.noauth_local_webserver = not success
    if not success:
      print 'Failed to start a local webserver listening on either port 8090'
      print 'Please check your firewall settings and locally'
      print 'running programs that may be blocking or using those ports.'
      print
      print 'Falling back to --noauth_local_webserver and continuing with',
      print 'authorization.'
      print

  oauth_callback = client.redirect_uri

  authorize_url = client.get_authorize_url()

  if not flags.noauth_local_webserver:
    webbrowser.open(authorize_url, new=1, autoraise=True)
    print 'Your browser has been opened to visit:'
    print
    print '    ' + authorize_url
    print
    print 'If your browser is on a different machine then exit and re-run this'
    print 'application with the command-line parameter'
    print
    print '  --noauth_local_webserver'
    print
  else:
    print 'Go to the following link in your browser:'
    print
    print '    ' + authorize_url
    print

  code = None
  if not flags.noauth_local_webserver:
    httpd.handle_request()
    if 'error_code' in httpd.query_params:
      sys.exit('Authentication request was rejected.')
    if 'code' in httpd.query_params:
      code = httpd.query_params['code']
    else:
      print 'Failed to find "code" in the query parameters of the redirect.'
      sys.exit('Try running with --noauth_local_webserver.')
  else:
    code = raw_input('Enter verification code: ').strip()

  try:
    credential = client.request_access_token(code)
  except :
    sys.exit('Authentication has failed')


  client = _authorize_clent(client, credential)
  
  f = open(client_access_token_file, 'w')
  f.write(json.dumps(credential))
  f.close()
  
  print 'Authentication successful.'

  return client