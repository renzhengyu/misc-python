class Node():
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

    def preorder(self):
        yield self.value
        if self.left_child:
            for value in self.left_child.preorder():
                yield value
        if self.right_child:
            for value in self.right_child.preorder():
                yield value

    def inorder(self):
        if self.left_child:
            for value in self.left_child.inorder():
                yield value
        yield self.value
        if self.right_child:
            for value in self.right_child.inorder():
                yield value

    def postorder(self):
        if self.left_child:
            for value in self.left_child.postorder():
                yield value
        if self.right_child:
            for value in self.right_child.postorder():
                yield value
        yield self.value

    def size(self):
        return 1 \
            + (self.left_child.size() if self.left_child is not None else 0) \
            + (self.right_child.size() if self.right_child is not None else 0)

root = Node(1)
root.left_child = Node(1.1)
root.right_child = Node(1.2)
root.left_child.left_child = Node(1.11)
root.left_child.right_child = Node(1.12)
root.right_child.left_child = Node(1.21)
root.right_child.right_child = Node(1.22)

for i in root.preorder():
    print i
print
for i in root.inorder():
    print i
print
for i in root.postorder():
    print i
print
print "Size = {}".format(root.size())
