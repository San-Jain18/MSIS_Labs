class Stack:
    def __init__(self):
        self.items = []

    def push(self,data):
        self.items.append(data)

    def pop(self):
        if not self.items:
            print("Stack empty")
        else:
            return self.items.pop()

    def display(self):
        print("Stack items:",self.items)

s = Stack()

s.push(90)
s.push(50)
s.push(100)

s.display()

s.pop()

