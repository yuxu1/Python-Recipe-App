a = int(input("Enter a number: "))
b = int(input("Enter a number to be added to or subtracted from the first: "))
operator = input("Enter operator + or -: ")

if operator == "+":
    print("The sum of these numbers is", a + b)

elif operator == "-":
    print("The difference of these numbers is", a - b)

else:
    print("Unknown operator")