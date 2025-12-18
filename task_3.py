class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def insert(root, value):
    """Insert value into BST and return root."""
    if root is None:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)

    return root


def sum_tree(root):
    if root is None:
        return 0
    return root.value + sum_tree(root.left) + sum_tree(root.right)


if __name__ == "__main__":
    values = [5, 3, 2, 4, 7, 6, 8]

    bst_root = None
    for v in values:
        bst_root = insert(bst_root, v)

    total = sum_tree(bst_root)
    print(f"Сума всіх значень у дереві: {total}")
