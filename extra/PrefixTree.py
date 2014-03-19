class PrefixNode(object):

	def __init__(self):
		self.tree = {}
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'
		for each in self.alpha:
			self.tree[each] = None

	def add(self, path, value):
		branch = path[0]
		path = path[1:]	
		if len(path) == 0:
			self.tree[branch] = value
			return
		if self.tree[branch] == None:
			self.tree[branch] = PrefixNode()
		self.tree[branch].add(path, value)

	def get(self, path, word):
		if len(path) == 1:
			return self.tree[path]
		branch = path[0]
		path = path[1:]
		i = self.tree[branch]
		return i.get(path)

	def rem(self, path):	
		if len(path) == 1:
			del self.tree[path]
			return self.tree
		branch = path[0]
		path = path[1:]
		i = self.tree[branch]
		return i.rem(path)

class PrefixTree(object):

	def __init__(self):
		self.root = PrefixNode()

	def add(self, key, value):
		return self.root.add(key, value)

	def get(self, word):
		return self.root.get(word)

	def rem(self, word):
		return self.root.rem(word)

p = PrefixTree()
p.add("hel", 8)
i = p.root.tree['h']
print i.tree
