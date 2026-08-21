#to implement the singly linked list and perform basic operations like insert delete update search

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Singly_ll:
    def __init__(self):
        self.head = None
    
    def insert_beginning(self,data):
        new = Node(data)
        new.next = self.head
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
    def insert_position(self,data,pos):
        new = Node(data)
        if pos==0:
            insert_beginning(data)
        else:
            current = self.head
            for _ in range(pos-1):
                if current is None:
                    print("position out of range")
                    return
                current = current.next

            if current.next is  None:
                new.next = current.next
                current.next = new

    def delete_beginning(self):
        if self.head is None:
            print("list is empty")
            return
        self.head = head.next
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
            self.head=head.next
            return

        current = self.head
        while current.next is not None:
            while current.next.data == value:
                current.next = current.next.next
                return
        current = current.next
    def display(self):
        if self.head is None:
            print("list is empty")
            return
        current = self.head 
        while current is not None:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
        print("\n")

ll = Singly_ll()

ll.insert_end(10)
ll.insert_end(20)
ll.insert_end(30)

ll.display()


ll.insert_beginning(5)

ll.display()


ll.insert_position(15, 2)

ll.display()





    
        
      
