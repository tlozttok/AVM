from collections import namedtuple


person=namedtuple("Person",["age","height","weight"])
p=person(age=18,height=170,weight=60)

def BMI(p:person)->float:
    return p.weight/(p.height/100)**2

bmi_of_p = BMI(p)

class Person:
    age:int
    height:int
    weight:int

    def __init__(self,age:int,height:int,weight:int):
        self.age=age
        self.height=height
        self.weight=weight


    def BMI(self):
        return self.weight/(self.height/100)**2

p2=Person(age=18,height=170,weight=60)
bmi_of_p2=p2.BMI()

