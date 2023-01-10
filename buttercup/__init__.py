from abc import ABC, abstractmethod
from threading import Thread
import platform, sys, os, time

class Cursor:
	def shape(_shape:int = 0, _steady_state:bool = True) -> None:
		"""
		Customises the cursor shape and blinking state
		0 - User Shape, 1 - Block, 3 - Underline, 5 - Bar
		"""
		if (_shape > 0):
			print(f"\x1B[{_shape + _steady_state}\x20q", end="")
		else:
			print(f"\x1B[{_shape}\x20q", end="")
		return None

	def blinking_mode(_blinking_state:bool = False) -> None:
		"""
		True enables cursor blinking, False disables cursor blinking
		"""
		if (_blinking_state):
			print(f"\x1B[?12h", end="")
		else:
			print(f"\x1B[?12l", end="")
		return None

	def show_mode(_show_state:bool = True) -> None:
		"""
		Sets cursor visibility
		True shows cursor, False hides cursor
		"""
		if (_show_state):
			print(f"\x1B[?25h", end="")
		else:
			print(f"\x1B[?25l", end="")
		return None

	def move(_direction:int, _distance:int = 1) -> None:
		"""
		Move cursor by <n>
		0 - up, 1 - down, 2 - forward (right), 3 - backward (left)
		"""
		_direction = chr(65 + _direction) # type: ignore
		print(f"\x1B[{_distance}{_direction}", end="")
		return None

	def line(_direction:int, _distance:int = 1) -> None:
		_direction = chr(69 + _direction) # type: ignore
		print(f"\x1B[{_distance}{_direction}", end="")
		return None

	def horizontal_absolute(_column:int = 1) -> None:
		print(f"\x1B[{_column}G", end="")
		return None

	def vertical_absolute(_line:int = 1) -> None:
		print(f"\x1B[{_line}d", end="")
		return None

	def position_absolute(_line:int = 1, _column:int = 1) -> None:
		print(f"\x1B[{_line};{_column}H", end="")
		return None

	def horizontal_vertical_absolute(_line:int = 1, _column:int = 1) -> None:
		print(f"\x1B[{_line};{_column}f", end="")
		return None

class Screen:
	width = 80
	height = 24

class kEvent(Thread):
	Thread.daemon = True

	keys = {
		'ctrl+q': b'\x11', 
	}

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
		while (not self._stop):
				_in_buf = kEvent.key_event()
				kEvent.t_kyDown = time.perf_counter_ns()
				if kEvent.press != _in_buf:
					kEvent.press = _in_buf
				elif kEvent.press == _in_buf and kEvent.t_kyUp < 3_000_000:
					kEvent.press = None

class Buttercup(ABC):
	if "utf-8" not in sys.stdout.encoding:
		raise Exception("UTF-8 incompatible terminal")

	game_state = False

	listener = kEvent()
	listener.start()

	def __init__(self):
		self.console_title = ""

		if platform.system() == "Windows": os.system("")
		sys.stdout.write("\033[?1049h\033[H")

		self.ON_INIT()
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=Screen.height, cols=Screen.width))

		_f_dt = 1
		while self.game_state:
			_f_st = time.perf_counter()

			kEvent.t_kyUp = time.perf_counter_ns() - kEvent.t_kyDown
			if kEvent.t_kyUp > 150_000_000:
				kEvent.press = None

			if (not self.game_state):
				listener._stop = True
				sys.stdout.write("\033[?1049l")
				sys.stdout.write("\x1B[!p")
				sys.stdout.write("\x1B[?25h")
				break

			if (self.console_title):
				# sys.stdout.write("\x1B]30;{}\007".format(self.console_title))
				sys.stdout.write("\x1B]0;{}\x1B\x5C".format(self.console_title))
			else:
				# sys.stdout.write("\x1B]30;{}{}\007".format(self.__class__.__name__ + " ", 1/_f_dt))
				sys.stdout.write("\x1B]0;{}{}\x1B\x5C".format(self.__class__.__name__+" ", 1/_f_dt))

			self.ON_UPDATE()
			
			_f_dt = time.perf_counter() - _f_st

