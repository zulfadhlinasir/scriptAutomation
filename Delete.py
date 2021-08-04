class Person():
    "This is a person class"
    def __init__(self,name,age):
        self.age = age
        self.name = name

    def greet(ssf):
        return('Hello')

a = Person("Zars",24)

# Output: 10
print("Person.age is: ",a.age)

# Output: <function Person.greet>
print("Person.greet is: ",a.greet)

# Output: "This is a person class"
print("Person.__doc_ is: ",a.__doc__)

print(a.name)
