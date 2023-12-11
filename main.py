from tkinter import *
from random import *
import pandas as pd

lan1 = input("Enter source language code: ")
lan2 = input("Enter translating language code: ")
database_file = pd.read_csv(f"data/{lan1}{lan2}.csv")

database = database_file.to_dict(orient="records")
card = choice(database)


def skip_card():
    global card, timer
    card = choice(database)
    canvas.itemconfig(card_look, image=card_front_img)
    canvas.itemconfig(language_info, text=f"{lan1}", fill="black")
    canvas.itemconfig(word, text=card[f"{lan1}"], fill="black")
    window.after_cancel(timer)
    timer = window.after(7000, flip_card)


def remove_card():
    global card, timer
    database.remove(card)
    card = choice(database)
    canvas.itemconfig(card_look, image=card_front_img)
    canvas.itemconfig(language_info, text=f"{lan1}", fill="black")
    canvas.itemconfig(word, text=card[f"{lan1}"], fill="black")
    window.after_cancel(timer)
    timer = window.after(7000, flip_card)


def flip_card():
    canvas.itemconfig(card_look, image=card_back_img)
    canvas.itemconfig(language_info, text=f"{lan2}", fill="white")
    canvas.itemconfig(word, text=card[f"{lan2}"], fill="white")


def save():
    df = pd.DataFrame(database)
    df.to_csv("data/words_to_learn.csv", index=False)
    window.destroy()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg="#B1DDC6")

canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_look = canvas.create_image(400, 263, image=card_front_img)
language_info = canvas.create_text(400, 150, text=f"{lan1}", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text=card[f"{lan1}"], font=("Ariel", 60, "bold"))

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=skip_card)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=remove_card)
right_button.grid(column=1, row=1)

timer = window.after(7000, flip_card)

# window.protocol("WM_DELETE_WINDOW", save)
window.mainloop()
