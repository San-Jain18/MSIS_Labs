class Circular_queue:
    def __init__(self,size):
        self.size = size
        self.items = [None] * size
        self.front = -1
        self.rear = -1
    def enqueue(self,data):
        if (self.rear + 1) % self.size == self.front:
            print("Queue is full")
            return
        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.size
        self.items[self.rear] = data

    def dequeue(self):
        if self.front==-1:
            print("Queue is empty")

        data = self.items[self.front]
        self.items[self.front] = None

        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front+1)%self.size

        return data

    def display(self):
        print("Queue items:",self.items)

cir_queue = Circular_queue(5)

cir_queue.enqueue(123)
cir_queue.enqueue(19)
cir_queue.enqueue(23)
cir_queue.enqueue(203)
cir_queue.enqueue(519)

cir_queue.display()

print("Dequeued:", cir_queue.dequeue())
print("Dequeued:", cir_queue.dequeue())

cir_queue.display()

cir_queue.enqueue(5)
cir_queue.enqueue(91)

cir_queue.display()