

RESULTS = {}

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
        count = 0
        # creates { keyword: [[url, word_count], [url, word_count]] }
        counter = Counter(i.lower() for i in self.soup.get_text().split()) 
        for key in counter:
            score = self._score(key)
            if key in RESULTS:
                RESULTS[key].append([self.url, counter[key]+score])
            else:    
                RESULTS[key] = [[self.url, counter[key]+score]]
        