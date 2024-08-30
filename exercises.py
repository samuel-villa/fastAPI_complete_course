# Variable assignment
# money = 50
# item_price = 15
# tax = 0.03
# print(money - (item_price + (item_price * tax)))


# String assignment
# days_left = input("how many days until your birthday ?")
# weeks = int(days_left) / 7
# print(f"{round(weeks, 2)} weeks")

# Lists Assignemnt
# zoo = ['dog', 'cat', 'fish', 'giraffe', 'tiger']
# zoo.pop(2)
# zoo.append('lion')
# zoo.pop(0)
# print(zoo)
# print(zoo[:3])


# Dictionaries Assignemnt
# my_vehicle = {
#     "model": "Ford",
#     "make": "Explorer",
#     "year": 2018,
#     "mileage": 40000
# }

# for key, value in my_vehicle.items():
#     print(key, value)

# vehicle2 = my_vehicle.copy()
# vehicle2['number_of_tires'] = 4
# vehicle2.pop('mileage')
# for key in vehicle2.keys():
#     print(key)

# Functions Assignment
# def my_dict(firstname, lastname, age):
#     return {
#         'firstname': firstname,
#         'lastname': lastname,
#         'age': age
#     }

class Test:
    name: str = 'Sam'
    __age: int = 39

test = Test()
test.name = 'Samuel'
print(test.name)
print(test.__age)