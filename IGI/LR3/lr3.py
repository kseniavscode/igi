from prettytable import PrettyTable #for pretty table
import math


#LAB 3
#YAROSHEVICH KSENIA, group 453504
#started 06.03.2026 8:13
#python 3.14.3

#task 1
#need to calculate the sum of the series ln(x+1)
def sum_F(x, n, eps):
    F = 0
    i = 1
    while True:
        part = (-1)**(i-1) * x**(i) / i
        F += part
        if abs(part) < eps or i == n:
            break 
        i += 1
    return F

def input_double():
    while True:
        try:
            x = float(input("Input value: "))
            break
        except ValueError:
            print("Input float value!")
    return x

def input_int():
    while True:
        try:
            x = int(input("Input value: "))
            if (x > 0 and x <= 500) :
                break
        except ValueError:
            print("Input int value from 1 to 500")
    return x

table = PrettyTable() 
table.field_names = ["x", "n", "F(x)", "Math", "eps"]
print("")
#Inputting values for function 
while True:
    print("x: x must be from -1 to 1")
    x = input_double()
    if (x >= -1 and x <= 1):
        break
    else:
        print("x must be from -1 to 1")
print("")
print("n: int number from 1 to 500 ")
n = input_int()
print("")
while True:
    print("eps: must be positive")
    eps = input_double()
    if (eps >= 0):
        break
    else:
        print("Eps must be positive")
print("")
F = sum_F(x, n, eps)
F_math = math.log(1+x) #using math

table.add_row([x, n, F, F_math, eps]) #this is our values
print(table)

#bad experience
# print("________________________________________________________________________")
# print("|  x  |  n  |        F(x)        |        Math F(x)       |     eps     |")
# print(f"| {x} | {n} | {F} | {F_math} | {eps} |")
# print("________________________________________________________________________")





