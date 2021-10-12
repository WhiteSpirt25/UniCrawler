from requests import api
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import IGNORED_EXTENSIONS, LinkExtractor

import requests as reqs

import os
from dotenv import load_dotenv
load_dotenv()

# Removed PDF, DOC and DOCX so they could be parsed
MY_IGNORED_EXTENSIONS = [
    # archives
    '7z', '7zip', 'bz2', 'rar', 'tar', 'tar.gz', 'xz', 'zip',

    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg', 'cdr', 'ico',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a', 'm4v', 'flv', 'webm',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'odt', 'ods', 'odg',
    'odp',

    # other
    'css', 'exe', 'bin', 'rss', 'dmg', 'iso', 'apk'
]

API_URL = os.getenv('API_URL')


class ExampleSpider(CrawlSpider):
    name = "uni_crawl" #Spider name
    allowed_domains = [os.getenv('ALOWED_DOMAIN')] # Which (sub-)domains shall be scraped?

    start_urls = [os.getenv('START_URL')] # Start with this one
    #start_urls = ["https://dspace.spbu.ru/handle/11701/21736"] # File test url

    rules = [
        Rule(LinkExtractor(), callback='download_page', follow=True),
        # Rule for files, regexpr searches for urls with pdf,doc or docx on the end.
        Rule(LinkExtractor(allow = '.*\.pdf|.*\.doc|.*\.docx',deny_extensions=MY_IGNORED_EXTENSIONS), callback ='download_page')
        ] 
    
    def _post_handler(self,url:str,file):
        data = {
                'url': url,
            }
        files = {
                'file': file   
            }
        reqs.post(url=API_URL,data=data,files=files)

    def download_page(self, response):
        print('Got a response from %s.' % response.url)

        self._post_handler(response.url,response.body)
