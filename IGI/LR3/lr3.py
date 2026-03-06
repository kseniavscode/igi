import math
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
            print("Input int value!")
    return x


while True:
    print("x: x must be from -1 to 1")
    x = input_double()
    if (x >= -1 and x <= 1):
        break
    else:
        print("x must be from -1 to 1")
print("n: ")
n = input_int()
while True:
    print("eps: must be positive")
    eps = input_double()
    if (eps >= 0):
        break
    else:
        print("Eps must be positive")

F = sum_F(x, n, eps)
F_math = math.log(1+x)

print("________________________________________________________________________")
print("|  x  |  n  |        F(x)        |        Math F(x)       |     eps     |")
print(f"| {x} | {n} | {F} | {F_math} | {eps} |")
print("________________________________________________________________________")





