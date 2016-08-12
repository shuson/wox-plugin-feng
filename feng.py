# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

BasicUrl = "http://bbs.feng.com/"
URL = 'forum.php?mod=forumdisplay&filter=author&orderby=dateline&fid='

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):
  
    def request(self,url):
	#get system proxy if exists
	if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
            }
            return requests.get(url,proxies = proxies)
        return requests.get(url)
			
    def query(self, param):
        url = BasicUrl + URL
        fname = param.strip()
        if fname == 'mac':
            url = url + "68"
        elif fname == 'ershou':
            url = url + "29"
        elif fname == 'xianmian':
            url = url + "406"
        else:
            url = url + "601"
                
        
	r = self.request(url)
	r.encoding = 'utf-8'
	bs = BeautifulSoup(r.content, 'html.parser')
	posts = bs.select('tbody[id^=normalthread]')

	result = []
	for p in posts:
            ptitle = p.find('a', class_='s xst')
            ptime = p.find('span').string
            pname = p.find('cite').find('a').string
            item = {
                'Title': u'{subject}'.format(subject=full2half(ptitle.string)),
                'SubTitle': u'by: {name} | {time}'.format(name=pname, time=ptime),
                'IcoPath': os.path.join('img', 'feng.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [BasicUrl+ptitle['href']]
                }
            }
            result.append(item)
        
	return result
    
    def open_url(self, url):
	webbrowser.open(url)

if __name__ == '__main__':
    Main()
