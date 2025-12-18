import timeit
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_lru(n):
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


class SplayNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def find(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                node.value = value
                self._splay(node)
                return

        new_node = SplayNode(key, value, parent=parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def _rotate_left(self, x):
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent

            if g is None:
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == g.left:
                self._rotate_right(g)
                self._rotate_right(p)
            elif x == p.right and p == g.right:
                self._rotate_left(g)
                self._rotate_left(p)
            else:
                if x == p.left:
                    self._rotate_right(p)
                    self._rotate_left(g)
                else:
                    self._rotate_left(p)
                    self._rotate_right(g)


def fib_splay(n, tree):
    if n <= 1:
        return n

    cached = tree.find(n)
    if cached is not None:
        return cached

    value = fib_splay(n - 1, tree) + fib_splay(n - 2, tree)
    tree.insert(n, value)
    return value

def time_lru(n, repeats=5):
    def run():
        fib_lru.cache_clear()  
        return fib_lru(n)

    return min(timeit.repeat(run, number=1, repeat=repeats))


def time_splay(n, repeats=5):
    def run():
        tree = SplayTree()  

    return min(timeit.repeat(run, number=1, repeat=repeats))


def main():
    steps = list(range(0, 951, 50))
    repeats = 5

    print("n\tLRU(s)\t\tSplay(s)")
    print("-" * 32)

    for n in steps:
        t_lru = time_lru(n, repeats=repeats)
        t_spl = time_splay(n, repeats=repeats)
        print(f"{n}\t{t_lru:.6f}\t\t{t_spl:.6f}")

    print("\nВисновок:")
    print("- LRU Cache зазвичай швидший, бо кешування вбудоване і дуже оптимізоване.")
    print("- Splay Tree теж кешує, але має більші накладні витрати на структуру/повороти.")


if __name__ == "__main__":
    main()
