dict={}
count=1
while True:
    count+=1
    print("1. Add item to dictionary")
    print("2. Remove item from dictionary")
    print("3.Delete dictionary")
    print("4. View dictionary")
    print("5.Update item in dictionary")
    print("6.Exit")
    choice=int(input("Enter your choice: "))
    if choice==1:
        key=input("Enter key: ")
        value=input("Enter value: ")
        dict[key]=value
        print("Item added successfully!")
    elif choice==2:
        key=input("Enter key to remove: ")
        if key in dict:
            del dict[key]
            print("Item removed successfully!")
        else:
            print("Key not found!")
    elif choice==3:
        dict.clear()
        print("Dictionary deleted successfully!")
    elif choice==4:
        print("Current dictionary:", dict)
    elif choice==5:
        key=input("Enter key to update: ")
        if key in dict:
            value=input("Enter new value: ")
            dict[key]=value
            print("Item updated successfully!")
        else:
            print("Key not found!")
    elif choice==6:
        print("Bye!")
        break
    #it is  for like if it is not found 
    else:
        print("Invalid choice! not found . Please try again.")
        
 