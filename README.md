Buttercup
===
Uses virtual terminal sequences
Aims to be simple, scalable and platform independent

Features:
+ [x] input buffer in form of a daemon thread
+ [x] game loop with initiation and update functions
+ [x] basic cursor control
+ [x] frame definition and smooth rendering
+ [x] basic drawing making capabilities

+ [ ] sprite loading (for ASCII art etc.)
+ [ ] player definition and control
+ [ ] builtin multiprocess handler (for strategy games and such)

Usage
---
Install via: `pip install -e buttercupGameFramework`

Example implementation:
```python
from buttercup import *

class Basic(Buttercup):
	def ON_INIT(self):
		self.game_state = True

	def ON_UPDATE(self):
		if kEvent.press == keys['ctrl+q']:
			self.game_state = False

		draw_string(37, 11, repr(kEvent.press))

Basic()
```

Resources
---
+ [Console Virtual Terminal Sequences][def]
+ [Py-Getch][def2]
+ [Javidx9][def3]


[def]: https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
[def2]: https://github.com/joeyespo/py-getch
[def3]: https://github.com/OneLoneCoder/Javidx9/tree/master/ConsoleGameEngine
