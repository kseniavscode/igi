from classes.spotify_class import *

import tkinter as tk
from tkinter import filedialog

from IPython.display import display
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
    popular, unpopular, mean = spotify.analize_danceability()

    display(popular.head(10))
    print()
    print(f"Danceability: {mean}")
    print()
    display(unpopular.head(10))

    break

