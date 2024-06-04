import tkinter as tk
import math
import random

class MovingDotApp:
    def __init__(self, root, width, height, start_x, start_y, radius):
        self.root = root
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.radius = radius

        # Create an outer frame with the desired border color
        self.frame = tk.Frame(root, bg='white')
        self.frame.pack(fill='both', expand=True)

        # Create the canvas with some padding to simulate the border
        self.canvas = tk.Canvas(self.frame, width=width, height=height, bg='white')
        self.canvas.pack(padx=10, pady=10)
        
        self.dot = self.canvas.create_oval(0, 0, 10, 10, fill='red')
        self.angle = 0
        self.circle_step = 0.05
        self.radius_step = radius / (2 * math.pi * 2 / self.circle_step)  # Decrease radius step to complete 2 full circles inward
        self.random_appearances_remaining = 20
        self.moving_dot_in_spiral()

    def moving_dot_in_spiral(self):
        current_radius = self.radius * (1 - (self.angle / (4 * math.pi)))
        x = self.start_x + current_radius * math.cos(self.angle)
        y = self.start_y + current_radius * math.sin(self.angle)
        self.canvas.coords(self.dot, x-5, y-5, x+5, y+5)
        self.angle += self.circle_step
        if self.angle < 4 * math.pi:
            self.root.after(50, self.moving_dot_in_spiral)
        else:
            self.canvas.coords(self.dot, -10, -10, 0, 0)
            self.root.after(500, self.random_appearance)

    def random_appearance(self):
        if self.random_appearances_remaining > 0:
            rand_x = self.start_x + random.uniform(-self.radius, self.radius)
            rand_y = self.start_y + random.uniform(-self.radius, self.radius)
            self.canvas.coords(self.dot, rand_x-5, rand_y-5, rand_x+5, rand_y+5)
            self.random_appearances_remaining -= 1
            self.root.after(1000, self.random_appearance)
        else:
            self.canvas.coords(self.dot, -10, -10, 0, 0)

def main():
    root = tk.Tk()
    root.geometry('+1565+205')  # Specify window location
    root.overrideredirect(True)  # Remove window header
    app = MovingDotApp(root, width=400, height=400, start_x=200, start_y=200, radius=125)
    root.mainloop()

if __name__ == '__main__':
    main()
