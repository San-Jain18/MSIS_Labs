#A food truck queue represented as a Singley Linked List must be split into two separate lines when a second truck opens at the tail. Assuming no new customer arrivals, implement a Python solution that splits the list at a given position while ensuring customers are ultimately served in their exact original arrival order (fairness/priority).
class Node:
    def __init__(self,customer):
        self.customer = customer
        self.next = None

class Queue:
    def __init__(self):
        #we shall take two pointers head and tail
        self.head = None
        self.tail = None

    def enqueue(self,cust):
        new = Node(cust)

        if self.head is None:
            self.head = self.tail = new
        else:
            self.tail.next = new
            self.tail = new

    def split(self):
        count = 0
        current = self.head

        while current:
            count+=1
            current = current.next
        mid = count//2
        print("MId",mid)
        current = self.head
        print("Frst queue:")
        for i in range(mid):
            print(current.customer,end=" ")
            current = current.next

        print("\nSecond queue:")
        while current:
            print(current.customer,end=" ")
            current = current.next
choice = 1  
count = 0   
q = Queue()          
while choice:
    choice = int(input("Add people?Jus type 1 or 0..nothing else "))
    if choice == 1: 
        count += 1 
        q.enqueue(count)
print("HEAD:", q.head) 
if q.head is not None: 
    print("HEAD CUSTOMER:", q.head.customer) 
q.split()
