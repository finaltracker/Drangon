import time

china_lng = (73.33, 135.05)
china_lat = (3.51, 53.33)



class Node:
	def __init__(self, data):
		self._data = data
		self._children = []

	def get_data(self):
		return self._data

	def get_children(self):
		return self._children

	def add(self, Node):
		if len(self._children) == 4:
			return False
		else:
			self._children.append(Node)

	def go(self,data):
		for child in self._children:
			if child.get_data() == data:
				return child
		return None

class Tree:
	def __init__(self):
		self._head = Node('China')
		
	def link_to_head(self, Node):
		self._head.add(Node)

	def insert(self, path, data):
		current = self._head
		for step in path:
			if current.go(step) == None:
				return False
			else:
				current = current.go(step)
		current.add(Node(data))
		return True

	def search(self, path):
		current = self._head
		for step in path:
			if current.go(step) == None:
				return None
			else:
				current = current.go(step)
		return current



if __name__ == '__main__':
	begin = (10,5)
	end = (20,13)
	duration = 20

	x = float(begin[0])
	y = float(begin[1])
	'''
	linear equation
	'''
	x1 = float(begin[0])
	y1 = float(begin[1])
	x2 = float(end[0])
	y2 = float(end[1])
	a = (y2 - y1)/(x2-x1)
	b = (y2*x1-y1*x2)/(x1-x2)

	step = (x2-x1)/20

	print 'a: %f, b: %d, step: %f' %(a,b,step)
	i = 1
	while i <= duration:
		print 'x : %d, y: %d' %(x, y)
		x += step
		y = a*x+b
		i += 1
		time.sleep(1)