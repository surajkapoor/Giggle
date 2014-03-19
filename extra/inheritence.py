class A(object):

	def __init__(self):
		self.intro = "I am Suraj"

	def func1(self):
		return self.intro + "...and I like to code"	

class B(A):

	def __init__(self):
		self.newintro = A.__init__()

	def func1(self, input):
		if input == 7:
			return self.intro + "...and I HATTTTE to code"	
		else:
			return super(B, self).newintro
		print self.newintro	
	

test = A()
print test.intro