from myconsole.console import *
import math
from classes.solve import *

while True:
    ch_data = menu_input_data()
    while ch_data != '1' and ch_data != '2':
        print("Mistake! Not correct input! Choose 1 or 2")
        ch_data = menu_input_data()
    if ch_data == '1':
        x = input_float_x()
        n = input_int_n()
        eps = input_float_eps()
    elif ch_data == '2':
        gen = generate_random_data()
        x = next(gen)
        n = next(gen)
        eps = next(gen)


    solve = Solve(x, n, eps)
    F = solve.sum_F(save_history=True)
    F_math = math.log(x + 1)
    
    for x in solve.get_stat():
        print(x)
        
    create_table(["x", "n", "F(x)", "Math", "eps"], [solve.x, solve.n, F, F_math, solve.eps])

    solve.get_plot()
    menu()
    choice = check_menu()
    if choice == 0:
        break         
