#Test for loop and control flow statements
list=[]
count=0
while True:
    count+=1
    if count <=1:   
        print("Enter 1 to add number")
        print("Enter 2 to view list")
        print("Enter 3 to delete number ")
        print("Enter 4 to sort list in ascending order ")
        print("Enter 5 to sort list in descending order ")
        print("Enter 6 to reverse the list ")
        print("Enter 7 to find the maximum number in the list ")
        print("Enter 8 to find the minimum number in the list ")
        print("Enter 9 to find the length of the list ")
        print ("Enter 10 to clear the list ")
        print("Enter 11 to count list items")
        print("Enter  12 a number to sum the items in the list")
        print("Enter 13 to exit loop")
        
    

    user=int(input("Enter a number: "))

    if user==1:
        num=int(input("Enter a number to add : "))
        list.append(num)
    elif user==2:
        print("Here is list :",list)
    elif user==3:
        num=int(input("Enter a number to delete : "))
        if num in list:
            list.remove(num)
            print(num,"has been removed from the list")
        else:
            print(num,"is not in the list")
    elif user==4:
        list.sort()
        print("List sorted in ascending order :",list)
    elif user==5:
        list.sort(reverse=True)
        print("List sorted in descending order :",list)

    elif user==6:
        list.reverse()
        print("Reversed list :",list)
    elif user==7:
        if list:
            print("Maximum number in the list is :",max(list))
        else:
            print("List is empty")
    elif user==8:
        if list:
            print("Minimum number in the list is :",min(list))
        else:
            print("List is empty")
    elif user==9:
        print("Length of the list is :",len(list))
    elif user==10:
        list.clear()
        print("List has been cleared")
    elif user==11:
        item=int(input("Enter the item to count in the list: "))
        count=list.count(item)
        print(f"The item {item} appears {count} times in the list.")
    elif user==12:
        total=sum(list)
        print("The sum of the items in the list is :",total)
    elif user==13:
        print("Exiting the loop. Goodbye!")
        break
    else:
        print("Invalid input, please try again.")
