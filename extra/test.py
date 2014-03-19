import ast

with open("results.txt") as r:
    s = ast.literal_eval(r.read())

print type(s)	
