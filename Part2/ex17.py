import random 

name = input("What is your name?")

codenames = ["Fearless Dragon", "Shadow Tiger", "Thunder Wolf", "Iron Falcon"]

codename = random.choice(codenames)

lucky_number = random.randint(1,100)

print(name + ",your codename is:", codename)
print("Your lucky number is:", lucky_number)