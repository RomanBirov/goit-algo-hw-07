class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        result = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            result += self.left.__str__(level + 1, "L--- ")
        if self.right:
            result += self.right.__str__(level + 1, "R--- ")
        return result


def get_height(node):
    return node.height if node else 0


def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def right_rotate(y):
    x = y.left
    t3 = x.right

    x.right = y
    y.left = t3

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def left_rotate(x):
    y = x.right
    t2 = y.left

    y.left = x
    x.right = t2

    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def insert(root, key):
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and key < root.left.key:
        return right_rotate(root)

    if balance < -1 and key > root.right.key:
        return left_rotate(root)

    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root


def min_value_node(node):
    # Знаходить найменше значення в AVL-дереві
    current = node
    while current.left:
        current = current.left
    return current


# Перевірка 
root = None
keys = [10, 20, 30, 25, 28, 27, -1]

for key in keys:
    root = insert(root, key)

print("AVL-Дерево:")
print(root)

min_node = min_value_node(root)
print(f"Найменше значення в дереві: {min_node.key}")