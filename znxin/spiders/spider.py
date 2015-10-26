# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2015

@author: v-shayi
'''
import scrapy
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from znxin.items import ZnxinItem

indexURL = 'http://hqb.nxin.com/index.shtml'

class SpiderSpider(BaseSpider):
    name = 'testspider'
    start_urls = ['http://z.nxin.com/Home/Index']

    def parse(self, response):
        self.logger.info('response url: ' + response.url)
        
        self.logger.info('starting phantomjs')
        dr = webdriver.PhantomJS('C:\\Users\\v-shayi\\Software\\phantomjs\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')

        global indexURL
        self.logger.info('retrieving index URL')
        dr.get(indexURL)
        sleep(10)
        self.logger.info('driver url: ' + dr.current_url)
        
        element = dr.find_element_by_xpath('//form[@id="loginAlert"]')
        dr.find_element_by_xpath('//input[@id="username"]').send_keys('yswhynot')
        dr.find_element_by_xpath('//input[@id="loginPassword"]').send_keys('hello123')
        element.submit()
        sleep(12)
        self.logger.info('driver url after login: ' + dr.current_url)
        
        next_element = dr.find_element_by_xpath('//a[@class="right red_d"]')
        next_element.click()
        sleep(10)
        self.logger.info('driver url after click: ' + dr.current_url)
        
        handles = dr.window_handles
        dr.switch_to_window(handles[1])
        self.logger.info('driver url after switching tab: ' + dr.current_url)
        
        item = ZnxinItem()
        item['name'] = dr.title
        item['html'] = dr.page_source
        yield item
        
        src = dr.page_source.encode('utf-8','ignore')
        hxs = HtmlXPathSelector(text=src)    
        areas = hxs.select('//div[@id="so_baojia_list"]/div')
        region_elements = []
        i = 0
        for area in areas:
            districts = area.select('.//dd/a')
            tmp = [(i, j) for j in range(len(districts))]
            region_elements.extend(tmp)
            i += 1
        
        for region_element in region_elements:
            areas = dr.find_elements_by_xpath('//div[@id="area"]/ul/li')
            hov = ActionChains(dr).move_to_element(areas[region_element[0]])
            hov.perform()
            
            districts = dr.find_elements_by_xpath('//div[@id="so_baojia_list"]/div[contains(@style, "display")]//dd/a')
            sleep(0.1)
            districts[region_element[1]].click()
            sleep(8)
            self.logger.info('current title: ' + dr.title)
                  
            item = ZnxinItem()
            item['name'] = dr.title
            item['html'] = dr.page_source
            yield item
            
            
        dr.quit()
#         areas = dr.find_elements_by_xpath('//div[@id="so_baojia_list"]/div[class="layer"]')
#         for area in areas:
#             js = 'arguments[0].style.height="auto"; arguments[0].style.display="block";'
#             dr.execute_script(js, area)
#             
#         area_lists = dr.find_elements_by_xpath('//div[@id="area"]/ul/li')
#         for area_list in area_lists:
#             js = 'argument[0].class="active";'
#             dr.execute_script(js, area_list)
#             
#         districts = dr.find_elements_by_xpath('//dd/a')
#         for district in districts:
#             district.click()
#             print 'current title: ' + dr.title
#             item = ZnxinItem()

        