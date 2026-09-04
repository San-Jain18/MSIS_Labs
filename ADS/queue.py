class Queue:
    def __init__(self):
        self.items = []


    def enqueue(self,data):
        self.items.insert(0,data)

    def dequeue(self):
        if not self.items:
            print("Stack empty")
        else:
            return self.items.pop()

    def display(self):
        print("Queue items:",self.items)

q = Queue()

q.enqueue(103)
q.enqueue(420)
q.enqueue(300)


q.display()

print("Dequeued:", q.dequeue())
q.display()
q.enqueue(102)
q.enqueue(34)


q.display()
