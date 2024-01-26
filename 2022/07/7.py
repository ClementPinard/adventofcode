class Tree:
    def __init__(self, name, parent) -> None:
        self.name = name
        self.parent = parent
        self.children = {}
        self.file_size = 0

    def append(self, name):
        child_node = Tree(name, self)
        self.children[name] = child_node

    def append_file(self, size):
        self.file_size += size

    def __repr__(self) -> str:
        return f"{self.name}\n{self.file_size}\n{self.children}"


with open("input.txt") as f:
    input_data = f.read().split("\n")[:-1]

below_10k_size = 0
smallest_to_free = 70000000
to_free = 70000000


def dir_sizes(tree):
    global below_10k_size, smallest_to_free, to_free
    size = tree.file_size
    for name, child in tree.children.items():
        size += dir_sizes(child)
    if size <= 100000:
        below_10k_size += size
    if size > to_free and size < smallest_to_free:
        smallest_to_free = size
    return size


root_tree = Tree("/", None)
file_tree = root_tree

for line in input_data:
    if line.startswith("$"):
        a, *b = line.split()
        if b[0] == "cd":
            dirname = b[1]
            if dirname == "..":
                file_tree = file_tree.parent
            else:
                if dirname not in file_tree.children:
                    file_tree.append(dirname)
                file_tree = file_tree.children[dirname]
    else:
        a, b = line.split()
        if a == "dir":
            file_tree.append(b)
        else:
            file_tree.append_file(int(a))

total_size = dir_sizes(root_tree)
print(below_10k_size)

free = 70000000 - total_size
to_free = 30000000 - free
dir_sizes(root_tree)
print(smallest_to_free)
