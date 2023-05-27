import turtle
from words import WORDLE_LENGTH
# x and y positions for each letter box
TOTAL_SIZE = 400
LETTER_SIZE = TOTAL_SIZE/WORDLE_LENGTH
TOP_LEFT_X = -TOTAL_SIZE/2
TOP_LEFT_Y = 200
# colors/font
BG_GRAY = 18,18,20
OUTLINE_GRAY = 58,58,60
LETTER_COLOR = 255,255,255
FONT = ("Arial", int(LETTER_SIZE/2), "normal")
YELLOW_COLOR = 182,157,63
GREEN_COLOR = 82,141,78
def move(row,col):
    # proportional to the letter size and in consequence the number of letters in each word
    x = TOP_LEFT_X + col * LETTER_SIZE
    y = TOP_LEFT_Y - row * LETTER_SIZE
    turtle.up()
    turtle.goto(x,y)
def draw_square(x,y,color):
    move(y,x-1) 
    turtle.down()
    turtle.pencolor(OUTLINE_GRAY)
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(LETTER_SIZE-LETTER_SIZE/(WORDLE_LENGTH*3))
        turtle.left(90)
    turtle.end_fill()
    turtle.pencolor("Black")
    turtle.up()
def draw_wordle_grid():
    turtle.hideturtle()
    turtle.colormode(255)
    turtle.bgcolor(BG_GRAY)
    turtle.tracer(0)
    turtle.speed(0)
    for y in range(6):
        for x in range(WORDLE_LENGTH):
            draw_square(x,y,BG_GRAY)
def write_letter(x,y,letter,color):
    move(y,x)
    turtle.down()
    draw_square(x,y,color)
    turtle.forward(LETTER_SIZE/2)
    turtle.pencolor(LETTER_COLOR)
    turtle.write(letter, align="center", font=FONT)
    turtle.up()
def write_word(word,word_num,guess_dict):
    x = 0
    color = ""
    for index,letter in enumerate(word):
        match guess_dict[index]:
            case "G":
                color = GREEN_COLOR
            case "Y":
                color = YELLOW_COLOR
            case "":
                color = OUTLINE_GRAY
        write_letter(x,word_num-1,letter,color)
        x +=1

def main():
    pass
if __name__ == "__main__":
    main()