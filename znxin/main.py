'''
Created on Oct 23, 2015

@author: v-shayi
'''
import scrapy.cmdline

def main():
#     scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'testspider', '-o', 'output.xml', '-t', 'xml'])
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'testspider'])

if __name__ == '__main__':
    main()