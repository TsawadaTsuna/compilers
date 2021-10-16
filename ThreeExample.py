from anytree import Node, RenderTree

root = Node(10)

level_1_child_1 = Node(34, parent=root)
level_1_child_2 = Node(89, parent=root)
level_2_child_1 = Node(45, parent=level_1_child_1)
level_2_child_2 = Node(50, parent=level_1_child_2)

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))

"""
class Node:
    def __init__(self, data):
        self.children = []
        self.data = data

left = Node("left")
middle = Node("middle")
right = Node("right")
root = Node("root")
root.children = [left, middle, right]
print(root.children)
"""

num = "3.2"
if "." in num:
    print("si")
else:
    print("no")

if "r" in "R1":
    print("si minus")
elif "R" in "R1":
    print("si mayus")
else:
    print("no r")