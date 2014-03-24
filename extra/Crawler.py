from bs4 import BeautifulSoup
from collections import Counter
from urlparse import urljoin
import requests
import re
import Queue

RESULTS = {}

def search_order(self, item):
    return item[1]    
    
def search(self, word):
    result = RESULTS[word]
    result.sort(key=search_order, reverse=True)
    return result
                  
class IndexPage(object):
    
    def __init__(self, url):
        self._page_results = {}
        self.url = url
        if str(requests.get(self.url)) == "<Response [200]>":
            self.text = requests.get(self.url).text
            self.soup = BeautifulSoup(self.text)
        else:
            self.soup = None
               
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
        
    def _add_to_results(self):
        count = 0
        # creates { keyword: [[url, word_count], [url, word_count]] }
        counter = Counter(i.lower() for i in self.soup.get_text().split()) 
        for key in counter:
            score = self._score(key)
            if key in RESULTS:
                RESULTS[key].append([self.url, counter[key]+score])
            else:    
                RESULTS[key] = [[self.url, counter[key]+score]]           
        
class Crawler(object):
    
    def __init__(self):
        self.visited = []
        self.to_crawl = []
        
    def _link_in_domain(self, link, url):
        return url in link      
        
    def _remove_hash_in_url(self, url):
        s = re.compile(r'#\S+')
        return re.sub(s, '', url)
                 
    def _retrieve_links(self, url):
        #retrieves links on page, appends to "to_crawl" list
        html = requests.get(url).text
        if html:
            soup = BeautifulSoup(html)
            for link in soup.find_all('a'):
                l = link.get("href")
                link = urljoin(url, l)
                if self._link_in_domain(link, url):
                    self.to_crawl.append(link)

    def crawl(self, url):
        self.to_crawl.append(url)
        while len(self.to_crawl) > 0:
            url = self.to_crawl[0] #1__first item in tocrawl
            url = self._remove_hash_in_url(url) #2__remove hash in url
            self.to_crawl.pop(0) #3__remove from list!!
            print len(self.to_crawl)
            if url not in self.visited: #4__check to see if in visited
                ind = IndexPage(url)
                ind._add_to_results()
                self._retrieve_links(url) #5__get new links and add them to tocrawl
                self.visited.append(url)  #6__add url to visited list
        print visited, len(visited), len(set(visited))                 
        return RESULTS 
                                   
url = "https://www.hackerschool.com/"

c = Crawler()
c.crawl(url)


