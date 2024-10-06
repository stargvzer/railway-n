import random
token = "5257043486:AAFgddkVAq9Ls0EwjMLi8PFlGjj_uKI3zrw"


startAnswer = "Проклятый срущий ньюсрустер...."


f = open("dict.txt", "r", encoding="utf-8")
lines = f.readlines()

random_message = lambda: random.choice(lines)
