from tkinter import *

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, self.canvas_width/2, self.canvas_height*0.7)
        self.xspeed = 0

        # Bind keyboard controls
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
    

    def move_left(self, evt):
        self.xspeed = -2

    def move_right(self, evt):
        self.xspeed = 2

    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        if pos[2] >= self.canvas_width:
            self.xspeed = 0

class Ball:
    def __init__(self, canvas, color, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        # Create an oval (ball) with size 15x15 pixels
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        # Move it to the middle of the canvas, 10% from the top
        self.canvas.move(self.id, self.canvas_width/2, self.canvas_height*0.1)

        # Set the initial speed of the ball
        self.xspeed = 2
        self.yspeed = -2

        self.hit_bottom = False

        # Initialize the hit counter
        self.hit_counter = 0
        self.counter_text = canvas.create_text(50, 30, text=f"Hits: {self.hit_counter}", font=("Helvetica", 16), fill='blue')

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        # Move the ball by its speed values
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)

        # Wall collision detection
        if pos[1] <= 0:    # Top wall
            self.yspeed = abs(self.yspeed)
        if pos[3] >= self.canvas_height:  # Bottom wall
            self.hit_bottom = True
        if pos[0] <= 0:    # Left wall
            self.xspeed = abs(self.xspeed)
        if pos[2] >= self.canvas_width:  # Right wall
            self.xspeed = -1*abs(self.xspeed)
        
        if self.hit_paddle(pos):
            self.yspeed = -1*abs(self.yspeed)
            # Increment the hit counter and update the text
            self.hit_counter += 1
            self.canvas.itemconfig(self.counter_text, text=f"Hits: {self.hit_counter}")

    


# Create the main window and canvas
tk = Tk()
tk.resizable(False, False)  # Prevent window resizing
tk.title("Pong Game")
canvas = Canvas(tk, width=600, height=500, bd=0, bg='ivory')
canvas.pack() # Pack is used to display objects in the window
canvas.update() # Needed to get the rendered canvas size 

# Create the paddle
paddle = Paddle(canvas, 'blue')

# create the ball
ball = Ball(canvas, 'red', paddle)




def game_over():
    canvas.create_text(
        canvas.winfo_width()/2, canvas.winfo_height()/2,
        text="GAME OVER",
        font=("Helvetica", 30),
        fill='red'
    )
    canvas.create_text(
        canvas.winfo_width()/2, canvas.winfo_height()/2+50,
        text="Press Space to quit",
        font=("Helvetica", 20),
        fill = 'red'
    )
    # Rebind space key to close the game
    tk.bind('<space>', close_game)

def close_game(event=None):
    tk.destroy()


def animate():
    ball.draw()
    paddle.draw()
    if not ball.hit_bottom:
        tk.after(5, animate)  # Schedule next update in 10ms
    else:
        game_over()

animate() # Start animation
# Run the main loop
tk.mainloop()
