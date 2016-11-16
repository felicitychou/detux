#!/usr/bin/env python
# coding=utf-8
# version:0.3

import requests
import json
import sys,getopt
import base64,StringIO
import os

class Detux(object):

  def __init__(self,api_key):
    '''
    :type api_key: str
    '''
    self.api_key = api_key
    self.r = None

  def requestisok(self):
    if self.r.status_code == requests.codes.ok and int(self.r.json()['status']) == 1:
        return True
    else:
        return False

  def error(self):
    return ("Error: %s ") % (self.r.json()['message'])

  def search(self,text,fromindex):
    payload = {'api_key': self.api_key, 'search': text, 'from': fromindex}
    self.r = requests.post("https://detux.org/api/search.php", data=payload)
    return self.requestisok()
    
  def get_report(self,sha256):
    payload = {'api_key': self.api_key, 'sha256': sha256}
    self.r = requests.post("https://detux.org/api/report.php", data=payload)
    return self.requestisok()

  def get_file(self,path):
    temp = StringIO.StringIO()
    base64.encode(open(path,'rb'),temp)
    return temp.getvalue()

  def submit(self,path,private,file_name,comments):
    payload = {'api_key': self.api_key, 'file': self.get_file(path), 'private': private, 'file_name': file_name, "comments": comments}
    self.r = requests.post("https://detux.org/api/submit.php", data=payload)
    return self.requestisok()

def main(api_key,text,fromindex,sha256,path,private,file_name,comments):
  de = Detux(api_key=api_key)

  if text is not None:
    if de.search(text=text,fromindex=fromindex):
      json.dump(de.r.json(), open('result.json', 'w'))
      print ("detux search %s output result.json" % (text))
    else:
      print ("detux Search %s" % (de.error()))
 
  if sha256 is not None:
    if de.get_report(sha256=sha256):
      json.dump(de.r.json(), open('report.json', 'w'))
      print ("detux get_report %s output report.json" % (sha256))
    else:
      print ("detux get report %s" % (de.error()))

  if path is not None:
    if os.path.exists(path) and os.path.isfile(path):
      if de.submit(path=path,private=private,file_name=file_name,comments=comments):
        json.dump(de.r.json(), open('submit.json', 'w'))
        print ("detux submit %s result output submit.json" % (path))
      else:
        print ("detux submit %s" % (de.error()))
    else:
      print  ("detux submit %s not exists." % (path))

          
def usage():
    print readme
    return
      
readme = '''
usage:
        detux -k api_key -s text
        detux -k api_key -g sha256
        detux -k api_key --submit filepath

        api_key = 
        text = "*"
        sha256 = ""
param:
        -k/--apikey  api_key
        -s/--search  search text
          --from  search text from 
        -g/--getreport get report based on sha256

        --submit submit file
            --private submit file private
            --filename set file name
            --comments  set comments

        -h/--help    help
'''

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hk:s:g:", ["help","apikey=","search=","from=","getreport=","submit=","private","filename=","comments="])

    api_key = None
    text = None
    fromindex = None
    sha256 = None

    path = None
    private = None
    file_name = None
    comments = None
    
    for op, value in opts:
        if op == "-k" or op == "--apikey":
            api_key = value
        elif op == "-s" or op == "--search":
            text = value
        elif op == "--from":
            fromindex = int(value)
        elif op == "-g" or op == "--getreport":
            sha256 = value
        elif op == "--submit":
            path = value
        elif op == "--private":
            private = 1
        elif op == "--filename":
            file_name = value
        elif op == "--comments":
            comments = value
        elif op == "-h" or op == "--help":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()

    if api_key is None or (text is None and sha256 is None and path is None):
        usage()
        sys.exit()

    main(api_key=api_key,text=text,fromindex=fromindex,sha256=sha256,path=path,private=private,file_name=file_name,comments=comments)