from pybloomfilter import BloomFilter
import time

bf = BloomFilter(100000, 0.1, 'filter.bloom')

def open_f(file):
	index = 0
	with open(file) as f:
		for line in f:
			for word in line.split():
				bf.add(word.rstrip().lower())

open_f("random.txt")
x = "tsdext" in bf
if x:
	print "yolo"
