# # def greet():
# #     print("hello world")
# # greet()
# def product(x,y,z):
#     return x,y,z
# print(product(10,20,30))



# def multiply():
#     a=int(input("Enter first number")) 
#     b=int(input("Enter second number")) 
#     return a*b
# print(multiply())
# def validations(x):
#     if x=="":
#         return print("User name cannot be empty ") 
# def login(username,password):
    
#     if username == "" or password== "":
#         print("Username or oassword cannot be empty")

#     if username.isspace() or password.isspace():
#         print("Do not give space")

#     if username=="admin" and password=="123":
#         return True
    
    

# username=input("Enter your username : ")
# #for checking that username and password cannot be blank
# if validations(username):
#         print("Authentication failed.")
#         exit()

# password=input("Enter your password : ")
# if validations(password):
#         print("Authentication failed.")
#         exit()
# authorize=login(username,password)

# if authorize:
#     print("Welcome back.")
# else:
#     print("Accsess denied. Please enter correct username or password")

#dictionary by function

# def student(**details):
#     print(details)
# student(name="Rahul",age=21,school="Dehli public school")

#creates tuple 

# def addition(*numbers):
#     return sum(numbers)
# sum_result=addition(1,2,3,4,5)
# print(f"Sum is {sum_result}")

def operations():
    choice=int(input("Enter add to do sum "))
    choice2=int(input("Enter minus to do differnce"))
    if choice=="sum":
        sum=int(input("Enter first number to sum"))
        sum2=int(input("Enter second number to sum"))
        total=sum+sum2
        return total
    if choice2=="minus":
        diff=int(input("Enter first number to do subtraction"))
        diff2=int(input("Enter second number to do subtraction"))
        total=diff-diff2
        return total
    

    

s=operations()


