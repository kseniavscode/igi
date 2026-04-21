from classes.spotify_class import *
from console.console import *

import tkinter as tk
from tkinter import filedialog

from IPython.display import display

BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

while True:

    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(
        title="Выберите CSV файл",
        filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            spotify = SpotifyClass(file_path)
            spotify.load_data()
            print(spotify)
        except Exception as e:
            print(f"ERROE: {e}")
            continue
    else:
        print("File not chosen")
        break

    print("\nOutput of first 10 songs, their singer and popularity in spotify charts\n")
    songs = spotify._df['track_name'].head(10).tolist()
    charts = spotify._df['in_spotify_charts'].head(10).tolist()

    my_series = pandas.Series(data=songs, index=charts)
    display(my_series)
    print()
    print()
    print(f"iloc: {my_series.iloc[0]}")
    print(f"loc: {my_series.loc[charts[0]]}")
    print()
    pop = spotify.get_popularity()
    print(f"Sliding average for 15 first: \n{spotify.sliding_average(pop).head(15)}")

    print('\n')
    spotify._df.info()
    print()
    display(spotify._df.describe())
    print()

    num_cols = spotify._df.select_dtypes(include=['number']).columns.tolist()

    print(f"\n{BLUE}It is avaliable colums for analysis{RESET}")
    for i, col in enumerate(num_cols):
        print(f"{i}. {col}")

    while True:
        try:
            criteria = int(input("Choose criteria on which we are looking for extremes (max/min): "))
            target = int(input("Choose number of colum for calculation mean: "))

            if criteria < 0 or criteria >= len(num_cols):
                raise ValueError
            if target < 0 or target >= len(num_cols):
                raise ValueError
        except ValueError:
            print("Not correct ...")
        else:
            col_criteria = num_cols[criteria]
            col_target = num_cols[target]

            max_value, min_value, max_group, min_group, ratio = spotify.analize_min_max(col_criteria, col_target)

            print(f"Max value in column criteria: {max_value}")
            print(f"Min value in column criteria: {min_value}")

            print(f"Group with max value:\n{max_group}\n")
            print(f"Group with min value:\n{min_group}\n")

            print(f"Average {num_cols[target]} in {ratio} high")
            break


    popular, unpopular, mean = spotify.analize_danceability()

    display(popular.head(10))
    print()
    print(f"Danceability: {mean}")
    print()
    display(unpopular.head(10))

    menu()
    choice = check_menu()
    if choice == 0:
        break

