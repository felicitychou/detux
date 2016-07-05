#!/usr/bin/env python
# coding=utf-8

import requests
import json

class detux(object):

  def __init__(self,api_key):
    '''
    :type api_key: str
    '''
    self.api_key = api_key
    self.r = None

  def requestisok(self):
    if self.r.status_code == requests.codes.ok and self.r.json()['status'] is '1':
        return True
    else:
        return False

  def error(self):
    return ("Error: %s ") % (self.r.json()['message'])


  def search(self,text):
    payload = {'api_key': self.api_key, 'search': text}
    self.r = requests.post("http://detux.org/api/search.php", data=payload)
    return self.requestisok()
    
  def get_report(self,sha256):
    payload = {'api_key': self.api_key, 'sha256': sha256}
    self.r = requests.post("http://detux.org/api/report.php", data=payload)
    return self.requestisok()

def main(api_key):
  de = detux(api_key=api_key)

  text = "28bbfe818e8632d9f9fb18b33a76dfb5c7c29066ed319fc9ef6db2ce6d86e63b"
  if de.search(text=text):
    json.dump(de.r.json(), open('result.json', 'w'))
    print "detux search %s output result.json" % (text)
  else:
    print ("detux Search %s" % (de.error()))

  sha256 = "28bbfe818e8632d9f9fb18b33a76dfb5c7c29066ed319fc9ef6db2ce6d86e63b"
  if de.get_report(sha256=sha256):
    json.dump(de.r.json(), open('report.json', 'w'))
    print "detux get_report %s output report.json" % (sha256)
  else:
    print ("detux get report %s" % (de.error()))

if __name__ == '__main__':
  api_key = ""
	main(api_key)
