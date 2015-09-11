map_table = [[3,3,8,8],[8,3,14,8],[3,9,8,12],[8,9,14,12]]

position_guard = (10,5)

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
	'''
	define Node
	'''
	a = Node('A')
	b = Node('B')
	c = Node('C')
	d = Node('D')
	e = Node('E')
	f = Node('F')
	g = Node('G')
	h = Node('H')
	i = Node('I')
	j = Node('J')
	k = Node('K')
	l = Node('L')
	m = Node('M')
	n = Node('N')
	o = Node('O')
	 
	'''
	adding Node to build true
	'''
	a.add(b)
	a.add(g)
	a.add(h)
	b.add(c)
	b.add(e)
	g.add(i)
	g.add(j)
	g.add(k)
	g.add(l)
	h.add(m)
	h.add(n)
	h.add(o)
	c.add(d)
	c.add(f)
	i.add(Node(29))
	j.add(Node(28))
	k.add(Node(27))
	l.add(Node(26))
	m.add(Node(25))
	n.add(Node(24))
	o.add(Node(23))
	f.add(Node(30))
	 
	 
	tree = Tree()
	tree.link_to_head(a)
	 
	 
	#testcase
	print 'Node',tree.search("ABE").get_data()
	print 'Node',tree.search("ABC").get_data()
	print 'Node',tree.search("AHM").get_data()
	tree.insert("ABCD", 1)
	for i in d.get_children():
	    print 'value after', d.get_data(),' is ', i.get_data()