# student={
#     "name":"Alica",
#     "age":21,
#     "course":"Python",

# }
# print (student.get("name","not found"))

# print(student.keys())

# for a in student.keys():
#     print(a)
# print (student.values())

# if student:
#     for a,b in student.items():
#         print(F"{a} : {b}")

# student.update({"name":"Alicia","age":22,"phone":"1234567890","email":"shailmann","login":True})

# for key,value in student.items():
#     if key=="login" and value==True:
#         print("Welcome back",student["name"])

#     elif key=="login" and value==False:
#         print("Please login to continue")

name ={
    1:{"name":"amit","marks":90},
    2:{"name":"sumit","marks":85},
    3:{"name":"rahul","marks":78},
}
# new=dict.fromkeys(name,"python")
# print(new)

for key in name:
    for value in name[key]:
        print(value,":",name[key][value])

