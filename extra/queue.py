import Queue

a = Queue.Queue()

for i in range(10):
	a.put(i)
	a.task_done()

print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()
print a.get()