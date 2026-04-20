from console.console import *
from numpy_class.matrix_class import *

import numpy
import pandas

while True:

    choose_matrix()
    choice_matrix = check_choose_matrix()
    mat = None
    if choice_matrix == 1:
        print("Enter your matrix size n (rows): ")
        n = size_matrix()
        print("Enter your matrix size m (colums): ")
        m = size_matrix()
        print("Enter start of range for random matrix: ")
        start = range_random()
        print("Enter end of range for random matrix: ")
        end = range_random()

        start, end = check_start_end(start, end)

        mat = RandomMatrix(n,m,start,end)

    elif choice_matrix == 2:
        print("Enter your matrix size n (rows): ")
        n = size_matrix()
        print("Enter your matrix size m (colums): ")
        m = size_matrix()

        array_matrix = array_matrix_input(n,m)

        mat = ArrayMatrix(n,m,array_matrix)

    elif choice_matrix == 3:
        df = pandas_df()
        col_name = colum_pandas()
        
        if col_name in df.columns:
            mat = PandasMatrix(df, col_name)
        else:
            print("Error: Column not found!")
            continue
    
    if mat is not None:
        print("\n=== YOUR MATRIX ===")
        print(mat.matrix)

        print()
        for x in mat.get_stat():
            print(x)
        
        print()
        mat.create_new_matrix()
        print(f"New matrix:\n{mat.matrix}")
        print()
        print(f"NumPy variance: {mat.variance_numpy()}")
        print(f"My variance: {mat.variance()}")
        print()
        for x in mat.get_stat():
            print(x)
        
        mat.slicing()
        mat.universal()

    else:
        print("Your matrix is empty...")
    menu()
    choice = check_menu()
    if choice == 0:
        break
