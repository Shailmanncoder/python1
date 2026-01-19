student={
    "name":"Alica",
    "age":21,
    \

}
# print (student.get("name","not found"))

# print(student.keys())

# for a in student.keys():
#     print(a)
# print (student.values())

# if student:
#     for a,b in student.items():
#         print(F"{a} : {b}")
student.update({"name":"Alicia","age":22,"phone":"1234567890","email":"shailmann","login":True})

for key,value in student.items():
    if key=="login" and value==True:
        print("Welcome back",student["name"])

    elif key=="login" and value==False:
        print("Please login to continue")

