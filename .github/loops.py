# toy_box=["car","bike",25,7.5] #list 
#         #0.    #1     #2   #3
#         #a list starts with 0 adress
# #FOR LOOP
# for i in toy_box:
#     print(i)

# for i in range(0,21,2):#two table
#     print(i)

# name="Shailmann"

# for i in name:
#     print(i)

# information={"name":"Shailmann","age":12,"adress":"east kidwai nagar"}

# for i in information:
#     print(i,":",information[i])

# list=[10,20,30,40,50]

# for i in list:
#     print("before break")
#     if i==30:
#         break
#     print("after break",i)

# print("loop completed")


# customer_staff=[
#     {"name":"shailmann","phone number":2124569232,"age":21,"staff":True},
#     {"name":"rahul","phone number":213219232,"age":24,"staff":True},
#     {"name":"manoj","phone number":211290232,"age":29,"staff":False},
#     {"name":"rohan","phone number":212457832,"age":24,"staff":True},
#     {"name":"robbin","phone number":2124344224,"age":20,"staff":False}
# ]
# for x in customer_staff:
#     if x["staff"]:
#         print("Welcome staff",":",x["name"])
#     else:
#         print("Welcome customer",":",x["name"])
# number=40

# while number>=10:
#     print(number)
#     number-=5

# list=[]
# count=0
# while True:
#     count+=1
#     if count <=1:
#        print("Enter 1 to add number")
#        print("Enter 2 to view list")
#        print("Enter 3 to delete number ")
#        print("Enter 4 to exit loop")

#     user=int(input("Enter a number"))

#     if user==1:
#         num=int(input("Enter a number to add : "))
#         list.append(num)
#     else:
#         print("Enter only 1 to add ")
     
#     if user==2:
#         print("Here is list :",list)
    
#     elif user==3:
#         print("Here is the list and select a number to delete",list)
#         num2=int(input("Enter a number to delete : "))
#         if num2 in list:
#             list.remove(num2)
#         else:
#             print("Please select the number from the list ")
#     elif user==4:
#         print("Bye Bye")
#         break
#     else:
#         ("Please enter the correct number if you want to exit then type 4 .")



