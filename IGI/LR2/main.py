from geometric_lib import circle, square
r = 4
a = 10

s_circle = circle.area(r)
p_circle = circle.perimeter(r)

s_square = square.area(a)
p_square = square.perimeter(a)

print(f"Circle radius is {r}, area is {s_circle}, perimeter is {p_circle}")
print(f"Square side is {a}, area is {s_square}, perimeter is {p_square}")