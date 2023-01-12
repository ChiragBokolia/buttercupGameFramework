from abc import ABC, abstractmethod
from threading import Thread
import platform, sys, os, time

keys = {
	"ctrl+q": b"\x11",
	"escape": b"\x1b"
}

pixel_type = {
	"solid":"\u2588",
	"three_quarters":"\u2593",
	"half":"\u2592",
	"quarter":"\u2591"
}

fg_colo = {
	"black":"\x1b[30m",
	"red":"\x1b[31m",
	"green":"\x1b[32m",
	"yellow":"\x1b[33m",
	"blue":"\x1b[34m",
	"magenta":"\x1b[35m",
	"cyan":"\x1b[36m",
	"white":"\x1b[37m",
	# bold/bright color
	"b_black":"\x1b[90m",
	"b_red":"\x1b[91m",
	"b_green":"\x1b[92m",
	"b_yellow":"\x1b[93m",
	"b_blue":"\x1b[94m",
	"b_magenta":"\x1b[95m",
	"b_cyan":"\x1b[96m",
	"b_white":"\x1b[97m"
}

bg_colo = {
	"black":"\x1b[40m",
	"red":"\x1b[41m",
	"green":"\x1b[42m",
	"yellow":"\x1b[43m",
	"blue":"\x1b[44m",
	"magenta":"\x1b[45m",
	"cyan":"\x1b[46m",
	"white":"\x1b[47m",
	# bold/bright color
	"b_black":"\x1b[100m",
	"b_red":"\x1b[101m",
	"b_green":"\x1b[102m",
	"b_yellow":"\x1b[103m",
	"b_blue":"\x1b[104m",
	"b_magenta":"\x1b[105m",
	"b_cyan":"\x1b[106m",
	"b_white":"\x1b[107m"
}

class Screen:
	width = 80
	height = 24

	foreground = ""
	background = ""

	bufChar = [" " for i in range(width * height)]

	def __init__(self):
		self.buf = (i for i in range(Screen.width*Screen.height))
		# set terminal window width and height
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=Screen.height, cols=Screen.width))
		# clear the screen and restore default console colour
		# sys.stdout.write("\033[2J\033[0m")

	def render(self):
		if(Screen.foreground):
			sys.stdout.write(fg_colo[Screen.foreground])
		if(Screen.background):
			sys.stdout.write(bg_colo[Screen.background])

		sys.stdout.write("\x1B[1;1H")

		for i in self.buf:
			sys.stdout.write(Screen.bufChar[i])

def clip(x:int, y:int):
	if x<0: x=0
	if x>=Screen.width: x=Screen.width
	if y<0: y=0
	if y>=Screen.height: y=Screen.height

def draw(x:int, y:int, _char:str="\u2588"):
	if (not isinstance(x, int)) or (not isinstance(y, int)):
		raise ValueError("Coordinates should be integers")

	if (x >= 0 and x < Screen.width and y >= 0 and y < Screen.height):
		Screen.bufChar[y * Screen.width + x] = _char

def fill(x1:int, y1:int, x2:int, y2:int, _char:str="\u2588"):
	if (not isinstance(x1, int)) or (not isinstance(y1, int)):
		raise ValueError("Coordinates should be integers")
	if (not isinstance(x2, int)) or (not isinstance(y2, int)):
		raise ValueError("Coordinates should be integers")

	clip(x1, y1)
	clip(x2, y2)
	x = x1
	while x<x2:
		y = y1
		while y<y2:
			draw(x, y, _char)
			y+=1
		x+=1

def draw_string(x:int, y:int, _string:str):
	if (not isinstance(x, int)) or (not isinstance(y, int)):
		raise ValueError("Coordinates should be integers")

	if (x >= 0 and x < Screen.width and y >= 0 and y < Screen.height):
		for i in range(len(_string)):
			Screen.bufChar[y * Screen.width + x + i] = _string[i]

def draw_line(x1:int, y1:int, x2:int, y2:int, _char:str="\u2588"):
	if (not isinstance(x1, int)) or (not isinstance(y1, int)):
		raise ValueError("Coordinates should be integers")
	if (not isinstance(x2, int)) or (not isinstance(y2, int)):
		raise ValueError("Coordinates should be integers")

	dx = x2 - x1
	dy = y2 - y1
	dx1 = abs(dx)
	dy1 = abs(dy)
	px = 2 * dy1 - dx1
	py = 2 * dx1 - dy1
	if (dy1 <= dx1):
		if (dx >= 0):
			x = x1
			y = y1
			xe = x2
		else:
			x = x2
			y = y2
			xe = x1

		draw(x, y, _char)
		
		while x<xe:
			x = x + 1
			if (px<0):
				px = px + 2 * dy1
			else:
				if ((dx<0 and dy<0) or (dx>0 and dy>0)):
					y = y + 1
				else:
					y = y - 1
				px = px + 2 * (dy1 - dx1)
			draw(x, y, _char)
	else:
		if (dy >= 0):
			x = x1
			y = y1
			ye = y2
		else:
			x = x2
			y = y2
			ye = y1

		draw(x, y, _char)

		while y<ye:
			y = y + 1;
			if (py <= 0):
				py = py + 2 * dx1
			else:
				if ((dx<0 and dy<0) or (dx>0 and dy>0)):
					x = x + 1
				else:
					x = x - 1
				py = py + 2 * (dx1 - dy1)
			draw(x, y, _char)

def draw_triangle(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, _char:str="\u2588"):
	if (not isinstance(x1, int)) or (not isinstance(y1, int)):
		raise ValueError("Coordinates should be integers")
	if (not isinstance(x2, int)) or (not isinstance(y2, int)):
		raise ValueError("Coordinates should be integers")
	if (not isinstance(x3, int)) or (not isinstance(y3, int)):
		raise ValueError("Coordinates should be integers")

	draw_line(x1, y1, x2, y2, _char)
	draw_line(x2, y2, x3, y3, _char)
	draw_line(x3, y3, x1, y1, _char)

def draw_circle(xc:int, yc:int, r:int, _char:str="\u2588"):
	if (not isinstance(xc, int)) or (not isinstance(yc, int)):
		raise ValueError("Coordinates should be integers")
	if (not isinstance(r, int)) or (not r):
		raise ValueError("Radius should not be zero")

	x = 0
	y = r
	p = 3 - 2 * r

	while y>=x:
		draw(xc - x, yc - y, _char) # upper left left
		draw(xc - y, yc - x, _char) # upper upper left
		draw(xc + y, yc - x, _char) # upper upper right
		draw(xc + x, yc - y, _char) # upper right right
		draw(xc - x, yc + y, _char) # lower left left
		draw(xc - y, yc + x, _char) # lower lower left
		draw(xc + y, yc + x, _char) # lower lower right
		draw(xc + x, yc + y, _char) # lower right right

		if (p < 0):
			p += 4 * x + 6;
			x+=1
		else:
			p += 4 * (x - y) + 10;
			x+=1
			y-=1

class kEvent(Thread):
	Thread.daemon = True

	press = None

	t_kyDown = 0
	t_kyUp = 0

	def __init__(self):
		Thread.__init__(self)
		self._stop = False

	@staticmethod
	def key_event():
		if(platform.system() == "Windows"):
			from msvcrt import getch
			return getch()
		else:
			import tty, termios
			fd = sys.stdin.fileno()
			old = termios.tcgetattr(fd)
			try:
				tty.setraw(fd)
				_ch = bytes(sys.stdin.read(1), "ASCII")
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old)
			return _ch

	def run(self):
		while not self._stop:
				_in_buf = kEvent.key_event()
				kEvent.t_kyDown = time.perf_counter_ns()
				if kEvent.press != _in_buf:
					kEvent.press = _in_buf
				elif kEvent.press == _in_buf and kEvent.t_kyUp < 3_000_000:
					kEvent.press = None
		os._exit(0)

class Buttercup(ABC):
	if "utf-8" not in sys.stdout.encoding:
		raise Exception("UTF-8 incompatible terminal")

	game_state = False

	listener = kEvent()
	listener.start()

	deltaTime = 1

	def __init__(self):
		self.console_title = ""

		if platform.system() == "Windows": os.system("")
		# use alternate buffer
		sys.stdout.write("\033[?1049h")
		# hide the text cursor
		sys.stdout.write("\x1B[?25l")

		self.ON_INIT()
		viewport = Screen()

		while self.game_state:
			_f_st = time.perf_counter()

			kEvent.t_kyUp = time.perf_counter_ns() - kEvent.t_kyDown
			if kEvent.t_kyUp > 150_000_000:
				kEvent.press = None

			if (not self.game_state):
				listener._stop = True
				# reset color settings
				sys.stdout.write("\033[0m")
				# switch to main buffer
				sys.stdout.write("\033[?1049l")
				# soft reset settings
				sys.stdout.write("\x1B[!p")
				sys.stdout.write("\x1B[?25h")
				sys.exit(0)

			if (self.console_title):
				# sys.stdout.write("\x1B]30;{}\007".format(self.console_title))
				sys.stdout.write("\x1B]0;{}\x1B\x5C".format(self.console_title))
			else:
				# sys.stdout.write("\x1B]30;{}{}\007".format(self.__class__.__name__ + " ", 1/self.deltaTime))
				sys.stdout.write("\x1B]0;{}{}\x1B\x5C".format(self.__class__.__name__+" ", 1/self.deltaTime))
			
			Screen.bufChar = [" " for i in range(Screen.width * Screen.height)]
			self.ON_UPDATE()
			viewport.render()

			self.deltaTime = time.perf_counter() - _f_st

		# clear screen
		sys.stdout.write("\033[2J")
		# move text cursor to start of window
		sys.stdout.write("\x1B[1;1H")
		# make cursor visible
		sys.stdout.write("\x1B[?25h")

