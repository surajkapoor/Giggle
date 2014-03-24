from bs4 import BeautifulSoup
from pybloomfilter import BloomFilter
from urlparse import urlparse, urljoin
from tldextract import extract
from collections import Counter
from multiprocessing import Pool
import requests
import re
import pdb
import os
import time

# setup queues of sites that need to be crawled, request data from pages ready for BeautifulSoup, Ranking Algorithm
urls_to_crawl = []

visited = BloomFilter(1000000, 0.1, 'filter.bloom')
VISITED_LIST = []

#sites that will be crawled - move to separate text file
HOSTS = ["http://www.hackerschool.com", "http://www.mashable.com"]  

def _link_in_domain(url, link):
	#returns Bool to ensure link in domain
	host_domain = extract(url).domain
	return extract(str(link)).domain == host_domain
		
def clean_url(url):
	s = re.compile(r'#\S+')
	return re.sub(s, '', url)

def in_visited(url):
	return url in visited	

def _remove_hash_in_url(url):
        s = re.compile(r'#\S+')
        return re.sub(s, '', url)		

def get_new_urls(url):
	new_urls = []
	try:
		html = requests.get(url).text
	except (requests.exceptions.MissingSchema) as e:
		print e
		return False
	soup = BeautifulSoup(html)
	for each in soup.find_all('a'):
		l = each.get('href')
		link = urljoin(url, l)
		link = _remove_hash_in_url(link)
		if _link_in_domain(link, url) and in_visited(link) == False:
			new_urls.append(link)
	return new_urls

def write_crawled_sites(l):
	with open("crawled_file.txt", "w") as cf:
		cf.write(str(l))	
	print "Writing crawled sites completed!"
	return

if __name__ == "__main__":

	processes = 4	
	urls_pool = Pool(processes = processes)

	for host in HOSTS:
		urls_to_crawl.append(host)
	
	try:
		while len(urls_to_crawl) > 0:
			time.sleep(1)
			for url in urls_to_crawl: #1__get items to crawl
				url = _remove_hash_in_url(url) #2__remove hash in each url if present
				urls_to_crawl.remove(url)#3__remove from list
				print len(urls_to_crawl)	
				if in_visited(url) == False: #4__check to see if in visited
					visited.add(url) #5__add url to visited list
					VISITED_LIST.append(url) 
					new_urls = urls_pool.apply_async(get_new_urls, [url]) #6__get new links and add them to tocrawl
					try:
						new_urls_get = new_urls.get()
					except (requests.exceptions.ConnectionError) as c:
						new_urls_get = False		
					if new_urls_get:
						for new_url in new_urls_get:	
							urls_to_crawl.append(new_url)
		write_crawled_sites(VISITED_LIST)					
	except KeyboardInterrupt:
		print "quit..."
		exit(0)								