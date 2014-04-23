Giggle
======

Giggle is a site crawler that mimics the basic behavior of a search engine crawler. The crawler returns every words it has crawled, and maps each one against a list of the URLs it's appeared on and a score of how relevant that word is to the URL. 

```
{"school": "[("Hackerschool.com, 50), ("NewSchool.com", 20)...]} 
```

I've refactored the crawler a few times to increase it's crawl speed. Note that the scoring algorithm is in an additional file and needs to be refactored into the new crawl method. 

To run the crawler...

```
python giggle.py
```
