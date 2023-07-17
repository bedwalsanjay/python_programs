import time
from termcolor import colored
 
class lib:
    def __init__(self):
        self.name=""
        self.sclass=""
        self.books=list()
        self.no_book_issued=0
        self.menu()
    def menu(self):
        while True: 
            time.sleep(1)
            c=int(input(colored("""
                What action you want to perform, choose one of below
                1. Initiate student record 
                2. Want to borrow for a book
                3. Want to see the book status
                4. Want to return the book
                5. Exit
                """ ,'green')
                ))
            if c==1:
                self.registeration()
                print("User with name " + self.name + " who belongs to class "+self.sclass +" is registered suceessfully")
            elif c==2:
                self.borrow()
            elif c==3:
                self.book_status()      
            elif c==4:
                self.book_return()        
            else:
                break
    def registeration(self):
        self.name=input("enter your name : ")
        self.sclass=input("enter your class : ")

    def borrow(self):
        if(self.no_book_issued==3):
            print("NOT ALLOWED " + self.name +" has already reached to the maximum limit of borrowing books")
            return
        bname=input("enter book name : ")
        bprice=int(input("enter book price in INR : "))
        self.books.append((bname,bprice))
        self.no_book_issued +=1

    def book_status(self):
        print("\nTotal no of books issue to "+self.name +" = " +str(self.no_book_issued) )
        print("Below is the details of book issued" )
        print('*'*50)
        for i in self.books:
            print(i)
        print('*'*50)

    def book_return(self):
        rbook=input("enter the name of a book to return : ")
        new_books=[book for book in self.books if book[0] !=rbook]
        self.books=new_books
        self.no_book_issued -=1
stud1=lib()


# error message when you want to return a book which even does not exit
# error when you want to return a book which user does not have borrowed
# 