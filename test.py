import ast

with open("results.txt") as r:
    s = ast.literal_eval(r.read())


for i in s.keys():
	if len(s[i]) == 1:
		try:
			print i
		except UnicodeEncodeError:
			pass	
