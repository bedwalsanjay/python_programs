import time
class lib:
    def __init__(self):
        self.name=""
        self.sclass=""
        self.books=list()
        self.menu()
    def menu(self):
        while True: 
            time.sleep(1)
            c=int(input("""
                What action you want to perform, choose one of below
                1. Initiate student record 
                2. Want to borrow for a book
                3. Want to see the student status
                4. Want to return the book
                5. Exit
                """
                ))
            if c==1:
                self.registeration()
                print("User with name " + self.name + " who belongs to class "+self.sclass +" is registered suceessfully")
            elif c==2:
                self.borrow()
            elif c==3:
                self.stud_info()      
            elif c==4:
                self.book_return()        
            else:
                break
    def registeration(self):
        self.name=input("enter your name : ")
        self.sclass=input("enter your class : ")
    def borrow(self):
        bname=input("enter book name : ")
        bprice=int(input("enter book price in INR : "))
        self.books.append((bname,bprice))
    def stud_info(self):
        print("Below is the detail of " + self.name + " who belongs to class "+self.sclass )
        print('*'*50)
        for i in self.books:
            print(i)
        print('*'*50)
    def book_return(self):
        rbook=input("enter the name of a book to return : ")
        new_books=[book for book in self.books if book[0] !=rbook]
        self.books=new_books
stud1=lib()
