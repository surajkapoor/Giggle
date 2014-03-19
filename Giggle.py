from bs4 import BeautifulSoup
from pybloomfilter import BloomFilter
from urlparse import urlparse, urljoin
from tldextract import extract
from collections import Counter
from multiprocessing import Pool
import requests
import Queue
import re
import pdb
import os
import time

#Final Search Results
RESULTS = {}
PREFIX_TREE = {}
# setup queues of sites that need to be crawled, request data from pages ready for BeautifulSoup, Ranking Algorithm
TOCRAWL = Queue.Queue()

#sites that will be crawled - move to separate text file
HOSTS = ["http://www.hackerschool.com"]

def search_order(self, item):
    return item[1]    
    
def search(self, word):
    result = RESULTS[word]
    result.sort(key=search_order, reverse=True)
    return result
                  
class IndexPage(object):
    
    def __init__(self, soup, url):
        self.url = url
        self.soup = soup
               
    def _score_image_tags(self):
        score = len(self.soup.find_all('img')) * 2
        return score   
        
    def _score_header_tags(self, word):
        h1 = (len([i.text for i in self.soup.find_all('h1') if word in i.text]) * 20)
        h2 = (len([i.text for i in self.soup.find_all('h2') if word in i.text]) * 14)        
        h3 = (len([i.text for i in self.soup.find_all('h3') if word in i.text]) * 10)
        h4 = (len([i.text for i in self.soup.find_all('h4') if word in i.text]) * 6)
        score = h1 + h2 + h3 + h4
        return score
    
    def _score(self, word):
        return self._score_image_tags() + self._score_header_tags(word)           
        
    def index(self):
        # creates { keyword: [[url, word_count], [url, word_count]] }
        counter = Counter(i.lower() for i in self.soup.get_text().split()) 
        for key in counter:
            score = self._score(key)
            if key in RESULTS:
                RESULTS[key].append([self.url, counter[key]+score])
            else:    
                RESULTS[key] = [[self.url, counter[key]+score]]     

class Crawl(object):

	def __init__(self, tocrawl):
		self.tocrawl = TOCRAWL
		self.visited = BloomFilter(1000000, 0.1, 'filter.bloom')

	def _link_in_domain(self, url, link):
		#returns Bool to ensure link in domain
		host_domain = extract(url).domain
		return extract(str(link)).domain == host_domain

	def _new_url(self, link):
		return link in self.visited 
			
	def clean_url(self, url):
		s = re.compile(r'#\S+')
		return re.sub(s, '', url)

	def _retrieve_link(self, soup, url):
		for each in soup.find_all('a'):
			l = each.get('href')
			link = urljoin(url, l)
			self.tocrawl.put(link)

	def run(self):
		while self.tocrawl.empty() == False:
			url = self.tocrawl.get()
			url = self.clean_url(url)
			if self._new_url(url) == False:
				html = requests.get(url).text
				soup = BeautifulSoup(html)
				self._retrieve_link(soup, url)
				index = IndexPage(soup, url)
				index.index()
				print url
				self.visited.add(url)
				
def run_crawl(host):
	#global function can be pickled
#	for host in HOSTS:
#		TOCRAWL.put(host)
#	c = Crawl(TOCRAWL)
	print host
	print os.getpid()
	return host
#	return c.run()					

if __name__ == "__main__":
	cr_pool = Pool(processes = 5)
	result = cr_pool.apply_async(run_crawl, HOSTS)
	while True:
		time.sleep(0.1)
		urls_to_crawl = []
		while not TOCRAWL.empty():
			urls_to_crawl.append(TOCRAWL.get())
		if urls_to_crawl:
			cr_pool.apply_async(run_crawl,urls_to_crawl)	
	print result.get(timeout = 10)
