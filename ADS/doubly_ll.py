#to implement the singly linked list and perform basic operations like insert delete update search

class Node:
    def __init__(self,data):
        self.data = data
        self.prev = None
        self.next = None

class Doubly_ll:
    def __init__(self):
        self.head = None
    
    def insert_beginning(self,data):
        new = Node(data)
        if self.head is not None:
            new.next = self.head
            self.head.prev = new
        self.head = new

    def insert_end(self,data):
        new = Node(data)
        if self.head is None:
            self.head = new
            return
        current = self.head

        while current.next is not None:
            current= current.next

        current.next=new
        new.prev = current

    def insert_position(self,data,pos):
        new = Node(data)
        if pos==0:
            self.insert_beginning(data)
        else:
            current = self.head
            for _ in range(pos-1):
                if current is None:
                    print("position out of range")
                    return
                current = current.next

            if current.next is  None:
                current.next = new
                new.prev = current
            else:
                new.next = current.next
                new.prev = current
                current.next.prev = new
                current.next= new 


    def delete_beginning(self):
        if self.head is None:
            print("list is empty")
            return
        self.head = self.head.next
        self.head.prev = None

    def delete_end(self):
        if self.head is None:
            print("list is empty")
            return
        current = self.head
        while current.next.next is not None:
            current= current.next
        current.next = None

    def delete_value(self,value):
        if self.head is None:
            print("list is empty")
            return
        if self.head.data==value:
            self.head=self.head.next
            return

        current = self.head
        while current is not None:
            if current.data == value:
                if current.next is not None:
                    current.next.prev = current.prev
                current.prev.next = current.next
                return
            current = current.next
        
        print(f"Value {value} not found")

    def display(self):
        if self.head is None:
            print("list is empty")
            return
        current = self.head 
        while current is not None:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")
        print("\n")

ll = Doubly_ll()

ll.insert_end(10)
ll.insert_end(20)
ll.insert_end(30)

ll.display()


ll.insert_beginning(5)

ll.display()


ll.insert_position(15, 2)

ll.display()

ll.delete_value(20)
ll.display()

ll.delete_beginning()
ll.display()




    
        
      
