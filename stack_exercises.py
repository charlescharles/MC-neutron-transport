class SetOfStacks:
    class Stack:
        def __init__(self, cap):
            self.pointer = -1
            self.buffer = [0 for i in range(cap)]
            self.cap = cap

        def push(self, val):
            if self.pointer + 1 >= self.cap:
                raise Exception('Out of space')
            self.buffer[self.pointer + 1] = val

        def pop(self):
            if self.pointer <= 0:
                raise Exception('Trying to pop empty stack')
            val = self.buffer[self.pointer]
            self.buffer[self.pointer] = 0
            self.pointer -= 1
            return val

    def __init__(self, n, cap):
        self.stacks = [Stack(cap) for i in range(n)]
        self.pointers = [-1 for i in range(n)]
        self.n = n

    def push(self, val):
        open_stack = 0
        while self.pointers[open_stack] >= self.cap - 1:
            open_stack += 1
        if open_stack >= n:
            raise Exception('no more space on any stacks')
        self.stacks[open_stack].push(val)
        self.pointers[open_stack] += 1

    def pop(self, val):
        try:
            open_stack = self.pointers.index(-1) - 1
        except ValueError:
            open_stack = self.n - 1
        val = self.stacks[open_stack].pop()
        self.pointers[open_stack] -= 1
        return val

    def popAt(self, index):
        val = self.stacks[index]
        self.stacks[index] = 0
        self.pointers[index] -= 1
        return val


class MinStack:
    class MinNode:
        def __init__(self, val, minm):
            self.val = val
            self.minm = minm
            self.next = None

    def __init__(self):
        self.first = None

    def push(self, val):
        if self.first is None:
            self.first = Node(val, val)
        else:
            new_first = Node(val, min(self.first.minm, val))
            new_first.next = self.first.next
            self.first = new_first

    def pop(self):
        if self.first is None:
            raise Exception('empty stack')
        val = self.first.val
        self.first = self.first.next
        return val

    def minm(self):
        return self.first.minm