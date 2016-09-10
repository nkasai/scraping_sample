#!/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2016/09/03

@author: nkasai
'''
import sys
import argparse
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#
# settings
#
USER_AGNET = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'

class ScrapingBase(object, metaclass=ABCMeta):
    '''
    ScrapingBase
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        self.url = kwargs['url']
        print('url :{}'.format(self.url))
        
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (USER_AGNET)
        
        self.browser = webdriver.PhantomJS(desired_capabilities=dcap)
    
    def get(self):
        """
        get
        """
        self.browser.get(self.url)
        
        source = self.browser.page_source.encode('utf-8')
        #print('source :{}'.format(source))
        
        parsed = self._parse(source)
        #print('parsed :{}'.format(parsed))
        
        obj = self._extract(parsed)
        #print('obj : {}'.format(obj))
        
        self._register(obj)
    
    def _parse(self, source, *args, **kwargs):
        """
        _parse
        """
        return pq(source)
    
    @abstractmethod
    def _extract(self, parsed, *args, **kwargs):
        """
        _extract
        """
        ret = []
        
        return ret
    
    @abstractmethod
    def _register(self, obj, *args, **kwargs):
        """
        _register
        """
        pass

class MyScraping(ScrapingBase):
    '''
    MyScraping
    '''
    def _extract(self, parsed, *args, **kwargs):
        """
        _extract
        """
        ret = []
        
        #
        # example
        #
        obj_emphasis = parsed('ul.emphasis')
        #print('obj_emphasis : {}'.format(obj_emphasis))
        
        for o in obj_emphasis('li'):
            ret.append(pq(o).text())
        
        #print('_extract() : {}'.format(ret))
        
        return ret
    
    def _register(self, obj, *args, **kwargs):
        """
        _register
        """
        for o in obj:
            print(o)

def main(args):
    """
    main
    """
    ret = 0
    
    try:
        rc = MyScraping(
            url=args.url
        )
        rc.get()
    except Exception as e:
        print(e.__class__.__name__)
        print(e)
        
        ret = 1
    
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='scraping sample.')
    parser.add_argument('--url', required=True)
    args = parser.parse_args()

    result = main(args)

    sys.exit(result)

