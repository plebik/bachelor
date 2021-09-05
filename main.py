from pickle import load
from tkinter import *
from tkinter import ttk

import numpy as np
import pandas as pd
from keras.models import load_model

df_player = pd.read_csv("df_player.csv", index_col=0).drop(columns=[' '])
df_surface = pd.read_csv("df_surface.csv", index_col=[0, 1]).drop(columns=[' '])
df_versus = pd.read_csv("df_versus.csv", engine='c', index_col=[0, 1], skiprows=[1, 2]).drop(columns=[' '])
model = load_model('best_model.h5')
scaler = load(open('scaler.pkl', 'rb'))

root = Tk()
root.title("TennisPredictor")
root.resizable(width=False, height=False)
root.configure(bg='#2b2b2b')

window_height = 307
window_width = 920

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

names = list(df_player.columns)
length = len(max(names, key=len))

surface_names = {'Twarda': 'Hard', 'Ceglana': 'Clay', 'Trawiasta': 'Grass', 'Dywanowa': 'Carpet'}
# #input
p1 = ttk.Combobox(root, values=names, width=length)
p2 = ttk.Combobox(root, values=names, width=length)
surface = ttk.Combobox(root, values=list(surface_names.keys()), width=12)

combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                                      {'configure':
                                           {'selectbackground': '#214283',  # color of selection
                                            'fieldbackground': '#2b2b2b',  # color of background
                                            'background': '#cdc5b2',  # color of little button
                                            'foreground': '#cdc5b2'  # color of string
                                            }}}
                        )

combostyle.theme_use('combostyle')


def button_func():
    # default settings
    default_size = "  " * len(max(df_player.columns, key=len))
    name1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    name2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_prob1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_prob2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    elo_rating1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    elo_rating2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    h2h1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    h2h2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    height1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    height2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    hand1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    hand2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_surface1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_surface2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_overall1 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    win_overall2 = Label(root, text=default_size, bg='#2b2b2b', fg='#cdc5b2')
    attention = Label(root, text=" ", bg='#2b2b2b', fg='#e11717',
                      width=len("Uwaga! Wartości conajmniej jednej zmiennej są niekompletne") + 4)

    name1.grid(column=1, row=6)
    name2.grid(column=3, row=6)
    win_prob1.grid(column=1, row=7)
    win_prob2.grid(column=3, row=7)
    elo_rating1.grid(column=1, row=8)
    elo_rating2.grid(column=3, row=8)
    h2h1.grid(column=1, row=9)
    h2h2.grid(column=3, row=9)
    height1.grid(column=1, row=10)
    height2.grid(column=3, row=10)
    hand1.grid(column=1, row=11)
    hand2.grid(column=3, row=11)
    win_surface1.grid(column=1, row=12)
    win_surface2.grid(column=3, row=12)
    win_overall1.grid(column=1, row=13)
    win_overall2.grid(column=3, row=13)
    attention.grid(column=2, row=4)

    p1_name = p1.get().title()
    p2_name = p2.get().title()
    surface_choice = surface.get().capitalize()
    hand_equivalent = {1: 'L', 2: 'R', 3: 'U'}
    hand1 = hand_equivalent[df_player[p1_name]['hand']]
    hand2 = hand_equivalent[df_player[p2_name]['hand']]
    incomplete = False

    hand_choice = {'L': ['left_win', 'left_total'], 'R': ['right_win', 'right_total'], 'U': ['uni_win', 'uni_total']}

    if p1_name in names and p2_name in names and p1_name != p2_name and surface_choice in surface_names:

        diff_height = df_player[p1_name]['height'] - df_player[p2_name]['height']

        if df_player[p1_name]['bp_faced'] > 0 and df_player[p2_name]['bp_faced'] > 0:
            diff_bp = (df_player[p1_name]['bp_saved'] / df_player[p1_name]['bp_faced']) / (
                    df_player[p2_name]['bp_saved'] / df_player[p2_name]['bp_faced'])
        else:
            diff_bp = 0

        if df_player[p1_name]['serves_total'] > 0 and df_player[p2_name]['serves_total'] > 0:
            diff_sp = (df_player[p1_name]['serves_won'] / df_player[p1_name]['serves_total']) - (
                    df_player[p2_name]['serves_won'] / df_player[p2_name]['serves_total'])
        else:
            diff_sp = 0

        diff_elo = df_player[p1_name]['elo'] - df_player[p2_name]['elo']

        if df_player[p1_name][hand_choice[hand2][1]] > 0 and df_player[p2_name][hand_choice[hand1][1]] > 0:
            diff_hand = (df_player[p1_name][hand_choice[hand2][0]] / df_player[p1_name][hand_choice[hand2][1]]) - \
                        (df_player[p2_name][hand_choice[hand1][0]] / df_player[p2_name][hand_choice[hand1][1]])
        else:
            diff_hand = 0.0

        diff_win_h2h = df_versus[p1_name][p2_name]['won'] - df_versus[p2_name][p1_name]['won']
        diff_win_last5 = df_player[p1_name]['last5'] - df_player[p2_name]['last5']

        if df_player[p1_name]['total'] > 0 and df_player[p2_name]['total'] > 0:
            diff_win_overall = df_player[p1_name]['win'] / df_player[p1_name]['total'] - df_player[p2_name]['win'] / \
                               df_player[p2_name]['total']
        else:
            diff_win_overall = 0.0

        if df_surface[p1_name][surface_names[surface_choice]]['total'] > 0 and \
                df_surface[p2_name][surface_names[surface_choice]]['total'] > 0:
            diff_surface_overall = df_surface[p1_name][surface_names[surface_choice]]['win'] / \
                                   df_surface[p1_name][surface_names[surface_choice]][
                                       'total'] - df_surface[p2_name][surface_names[surface_choice]]['win'] / \
                                   df_surface[p2_name][surface_names[surface_choice]]['total']
        else:
            diff_surface_overall = 0.0

        result = np.array([[
            diff_height, diff_bp, diff_sp, diff_elo, diff_hand, diff_win_h2h, diff_win_last5,
            diff_win_overall, diff_surface_overall
        ]])
        transformed_result = scaler.transform(result)
        probability = round(model.predict(transformed_result)[0][0] * 100, 2)

        name1 = Label(root, text=p1_name, bg='#2b2b2b', fg='#cdc5b2')
        name2 = Label(root, text=p2_name, bg='#2b2b2b', fg='#cdc5b2')
        win_prob1 = Label(root, text=probability, bg='#2b2b2b', fg='#cdc5b2')
        win_prob2 = Label(root, text=round(100 - probability, 2), bg='#2b2b2b', fg='#cdc5b2')
        elo_rating1 = Label(root, text=df_player[p1_name]['elo'], bg='#2b2b2b', fg='#cdc5b2')
        elo_rating2 = Label(root, text=df_player[p2_name]['elo'], bg='#2b2b2b', fg='#cdc5b2')
        h2h1 = Label(root, text=df_versus[p1_name][p2_name]['won'], bg='#2b2b2b', fg='#cdc5b2')
        h2h2 = Label(root, text=df_versus[p2_name][p1_name]['won'], bg='#2b2b2b', fg='#cdc5b2')
        height1 = Label(root, text=df_player[p1_name]['height'], bg='#2b2b2b', fg='#cdc5b2')
        height2 = Label(root, text=df_player[p2_name]['height'], bg='#2b2b2b', fg='#cdc5b2')
        hand1 = Label(root, text=hand_equivalent[df_player[p1_name]['hand']], bg='#2b2b2b', fg='#cdc5b2')
        hand2 = Label(root, text=hand_equivalent[df_player[p2_name]['hand']], bg='#2b2b2b', fg='#cdc5b2')

        if df_surface[p1_name][surface_names[surface_choice]]['total'] > 0:
            ws1 = round(df_surface[p1_name][surface_names[surface_choice]]['win'] * 100 /
                        df_surface[p1_name][surface_names[surface_choice]]['total'], 2)
        else:
            incomplete = True
            ws1 = "brak danych"

        if df_surface[p2_name][surface_names[surface_choice]]['total'] > 0:
            ws2 = round(df_surface[p2_name][surface_names[surface_choice]]['win'] * 100 /
                        df_surface[p2_name][surface_names[surface_choice]]['total'], 2)
        else:
            incomplete = True
            ws2 = "brak danych"

        if df_player[p1_name]['total'] > 0:
            wo1 = round(df_player[p1_name]['win'] * 100 / df_player[p1_name]['total'], 2)
        else:
            incomplete = True
            wo1 = 0.0

        if df_player[p2_name]['total'] > 0:
            wo2 = round(df_player[p2_name]['win'] * 100 / df_player[p2_name]['total'], 2)
        else:
            incomplete = True
            wo2 = 0.0

        win_surface1 = Label(root, text=ws1, bg='#2b2b2b', fg='#cdc5b2')
        win_surface2 = Label(root, text=ws2, bg='#2b2b2b', fg='#cdc5b2')
        win_overall1 = Label(root, text=wo1, bg='#2b2b2b', fg='#cdc5b2')
        win_overall2 = Label(root, text=wo2, bg='#2b2b2b', fg='#cdc5b2')

        text = ""
        if incomplete:
            text = "Uwaga! Wartości conajmniej jednej zmiennej są niekompletne"

        attention = Label(root, text=text, bg='#2b2b2b', fg='#e11717',
                          width=len("Uwaga! Wartości conajmniej jednej zmiennej są niekompletne") + 4)

        name1.grid(column=1, row=6)
        name2.grid(column=3, row=6)
        win_prob1.grid(column=1, row=7)
        win_prob2.grid(column=3, row=7)
        elo_rating1.grid(column=1, row=8)
        elo_rating2.grid(column=3, row=8)
        h2h1.grid(column=1, row=9)
        h2h2.grid(column=3, row=9)
        height1.grid(column=1, row=10)
        height2.grid(column=3, row=10)
        hand1.grid(column=1, row=11)
        hand2.grid(column=3, row=11)
        win_surface1.grid(column=1, row=12)
        win_surface2.grid(column=3, row=12)
        win_overall1.grid(column=1, row=13)
        win_overall2.grid(column=3, row=13)
        attention.grid(column=2, row=4)


# static labels
player_name = Label(root, text="Nazwa gracza", bg='#2b2b2b', fg='#cdc5b2')
win_probability = Label(root, text=" " * 18 + "Prawdopodobieńśtwo wygranej" + " " * 18, bg='#2b2b2b', fg='#cdc5b2',
                        width=len("Uwaga! Wartości conajmniej jednej zmiennej są niekompletne") + 4)
elo = Label(root, text="Elo Rating", bg='#2b2b2b', fg='#cdc5b2')
h2h = Label(root, text="H2H", bg='#2b2b2b', fg='#cdc5b2')
height = Label(root, text="Wzrost", bg='#2b2b2b', fg='#cdc5b2')
hand = Label(root, text="Preferowana ręka", bg='#2b2b2b', fg='#cdc5b2')
surface_winratio = Label(root, text="% zwycięstw na wybranej powierzchni", bg='#2b2b2b', fg='#cdc5b2')
win_overall = Label(root, text="% zwycięstw ogółem", bg='#2b2b2b', fg='#cdc5b2')
empty_left = Label(root, text=" " * 10, bg='#2b2b2b', fg='#cdc5b2')
empty_right = Label(root, text=" " * 10, bg='#2b2b2b', fg='#cdc5b2')
empty_up = Label(root, text=" " * 10, bg='#2b2b2b', fg='#cdc5b2')
empty_down = Label(root, text=" " * 10, bg='#2b2b2b', fg='#cdc5b2')
field1 = Label(root, text='Gracz 1', bg='#2b2b2b', fg='#cdc5b2')
field2 = Label(root, text='Powierzchnia', bg='#2b2b2b', fg='#cdc5b2')
field3 = Label(root, text='Gracz 2', bg='#2b2b2b', fg='#cdc5b2')
# buttons
compile_button = Button(root, text="Oblicz", padx=20, pady=5, command=button_func, bg='#2b2b2b', fg='#cdc5b2')

player_name.grid(column=2, row=6)
win_probability.grid(column=2, row=7)
elo.grid(column=2, row=8)
h2h.grid(column=2, row=9)
height.grid(column=2, row=10)
hand.grid(column=2, row=11)
surface_winratio.grid(column=2, row=12)
win_overall.grid(column=2, row=13)
field1.grid(column=1, row=0)
field2.grid(column=2, row=0)
field3.grid(column=3, row=0)

empty_left.grid(column=0, row=0)
empty_right.grid(column=4, row=15)
empty_up.grid(column=2, row=2)
empty_down.grid(column=2, row=4)
p1.grid(column=1, row=1)
p2.grid(column=3, row=1)
surface.grid(column=2, row=1)

compile_button.grid(column=2, row=5)

root.mainloop()
