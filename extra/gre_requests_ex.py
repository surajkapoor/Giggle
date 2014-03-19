import grequests

urls = ['http://www.heroku.com','http://www.hackerschool.com','http://www.bbc.com']

def do_something(response, **kwargs):
	print response.text	


def req(urls):
	rs = (grequests.get(u, hooks = {'response':do_something}) for u in urls)
	x = grequests.map(rs)
	return x

print req(urls)	