import turtle
import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import numpy as np
import math
from functools import partial


class TurtlePlot:
	def __init__(self, wn, startFrame, runFrame, stopFrame):
		self.wn = wn
		self.running = True
		self.draw_axes()

		self.draw_turtle = RawTurtle(self.wn)
		self.draw_turtle.hideturtle()
		self.draw_turtle.penup()

		self.start = tk.Button(startFrame, text = "start", fg = "black", command = partial(self.generate_line, 0, 0, 0)).pack(side = tk.LEFT)
		self.run = tk.Button(runFrame, text = "run", fg = "black", command = self.start_drawing).pack(side = tk.LEFT)
		self.stop = tk.Button(stopFrame, text = "stop", fg = "black", command = self.stop_drawing).pack(side = tk.RIGHT)

		self.input_draw()


	def draw_axes(self):
		x = RawTurtle(self.wn)
		x.hideturtle()
		y = RawTurtle(self.wn)
		y.hideturtle()
		z = RawTurtle(self.wn)
		z.hideturtle()

		zline = np.linspace(0, 300, 2)
		xline = np.sin(zline)
		yline = np.cos(zline)

		for i in range(len(zline)):
			x.goto(zline[i], 0)
			y.goto(0, zline[i])

		x.write("x", font = ("Arial", 30, "normal"))
		y.write("y", font = ("Arial", 30, "normal"))

		x2d, y2d = self.convert_projection(xline, yline, zline)
		for i in range(len(x2d)):
			z.goto(x2d[i], y2d[i])

		# self.convert_projection(xline, yline, zline)
		# self.draw_curve()

		z.penup()
		z.goto(-210, -200)
		z.pendown()
		z.write("z", font = ("Arial", 30, "normal"))


	def input_draw(self):
		screen = self.wn
		answer_x = screen.textinput("Input window", "Please enter x_coordinate:")
		answer_y = screen.textinput("Input window", "Please enter y_coordinate:")
		answer_z = screen.textinput("Input window", "Please enter z_coordinate:")

		if answer_x is None or answer_y is None or answer_z is None:
			print("Illegal input")
		else:
			x = float(answer_x)
			y = float(answer_y)
			z = float(answer_z)
			self.generate_line(x, y, z)


	def generate_line(self, x, y, z):
		self.running = True
		zline = np.linspace(z, z + 15, 1000)
		xline = np.linspace(x, x + 15, 1000)
		xline = np.sin(xline)
		yline = np.linspace(y, y + 15, 1000)
		yline = np.cos(yline)

		self.convert_projection(xline, yline, zline)

		self.draw_turtle.goto(self.x2D[0] * 10, self.y2D[0] * 10)
		self.draw_turtle.pendown()

		while self.running == True:
			self.draw_curve()


	def convert_projection(self, xline, yline, zline):
		self.x2D = xline - zline * math.cos(math.radians(45))
		self.y2D = yline - zline * math.sin(math.radians(45))

		return self.x2D, self.y2D


	def draw_curve(self):
		while self.running == True:
			if self.draw_turtle.xcor() == self.x2D[0] * 10 and self.draw_turtle.ycor() == self.y2D[0] * 10:
				for i in range(len(self.x2D)):
					self.draw_turtle.goto(self.x2D[i] * 10, self.y2D[i] * 10)
					if self.draw_turtle.xcor() == self.x2D[len(self.x2D) - 1] and self.draw_turtle.ycor() == self.y2D[len(self.y2D) - 1]:
						break
					if self.running == False:
						break
			else:
				for i in range(len(self.x2D)):
					if self.draw_turtle.xcor() == self.x2D[i] * 10:
						index = i
						while index < len(self.x2D) - 1:
							if self.running == False:
								break
							self.draw_turtle.goto(self.x2D[index + 1] * 10, self.y2D[index + 1] * 10)
							index += 1


	def start_drawing(self):
		self.running = True
		self.draw_curve()


	def stop_drawing(self):
		self.running = False


def create_screen():
	root = tk.Tk()
	canvas = tk.Canvas(root, width = 700, height = 700)
	canvas.pack()
	wn = TurtleScreen(canvas)
	return wn, root


def create_buttons(root):
	startFrame = tk.Frame(root)
	startFrame.pack()

	runFrame = tk.Frame(root)
	runFrame.pack()

	stopFrame = tk.Frame(root)
	stopFrame.pack()

	return startFrame, runFrame, stopFrame


def main():
	wn, root = create_screen()
	startFrame, runFrame, stopFrame = create_buttons(root)
	TurtlePlot(wn, startFrame, runFrame, stopFrame)
	wn.mainloop()


main()