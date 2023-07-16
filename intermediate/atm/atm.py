import time
class Atm:
    def __init__(self):
        self.pin=0
        self.bal=0
        self.menu()
    def menu(self):
        while(True):
            time.sleep(3)
            c=input("""
            enter choice 
            1. create pin 
            2. deposit
            3. withdraw
            4. check balance
            5. exit
            
            """)
            if int(c)==1:
                self.createpin()
            if int(c)==2:
                self.deposit()
            if int(c)==3:
                self.withdraw()   
            if int(c)==4:
                self.check_bal()
            if int(c)==5:
                break
    def createpin(self):
        pin=input("enter pin code to set : ")
        self.pin=int(pin)

    def deposit(self):
        deposit_amt=input("enter amount to deposit : ")
        self.bal+=int(deposit_amt)
        self.check_bal()

    def withdraw(self):
        withdrawal_amt=input("enter amount to withdraw : ")
        self.bal-=int(withdrawal_amt)
        self.check_bal()

    def check_bal(self):
        print("your current balance is = " + str(self.bal))
        
sbi=Atm()