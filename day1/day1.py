class TrieNode:
    def __init__(self, terminal):
        self.children = {}
        self.terminal = terminal
        self.count = 1
        self.index = -1 if terminal else 0

    def _add_child(self, letter, child_node):
        self.children[letter] = child_node

    def _child_exists(self, letter):
        return letter in self.children

    def _get_child(self, letter):
        return self.children[letter]

    def _make_terminal(self):
        if self.terminal:
            self.count += 1
        else:
            self.terminal = True
            self.index = -1

    def _sum(self):
        sum = 0
        for node in self.children.values():
            sum += node._sum()
        if self.terminal:
            sum += self.index * self.count
        return sum

    def _traverse(self, depth=1):
        terminal = 0
        for key, node in self.children.items():
            print(depth * " ", key, "->")
            terminal += node._traverse(depth + 1)

        if self.terminal:
            terminal += self.count
            if self.count > 1:
                print("AAA")
        return terminal




def add_word_to_trie(trie_root, word):
    curr_node = trie_root
    for letter in word[:-1]:
        if not curr_node._child_exists(letter):
            new_child = TrieNode(terminal=False)
            curr_node._add_child(letter, new_child)
        curr_node = curr_node._get_child(letter)

    final_letter = word[-1]
    if not curr_node._child_exists(final_letter):
        new_child = TrieNode(terminal=True)
        curr_node._add_child(final_letter, new_child)
    else:
        child = curr_node._get_child(final_letter)
        child._make_terminal()


def build_trie(words):
    trie_root = TrieNode(terminal=False)
    for word in words:
        add_word_to_trie(trie_root, word)
    return trie_root


def iteration(tokens, trie_root, letter, word_idx):
    new_tokens = []
    tokens.append((trie_root, word_idx))
    for node, index in tokens:
        if not node._child_exists(letter):
            continue
        else:
            new_node = node._get_child(letter)
            if new_node.terminal and new_node.index == -1:
                new_node.index = index
            new_tokens.append((new_node, index))

    return new_tokens


with open('day1_input.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]

    string = lines[0]
    trie_root = build_trie(lines[1:])
    tokens = []

    for word_idx, word in enumerate(string.split()):
        for char in word:
            tokens = iteration(tokens, trie_root, char, word_idx)


    print(trie_root._sum())
