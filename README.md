Buttercup
===
Currently provides:
+ input buffer in form of a daemon thread
+ game loop with initiation and update functions
+ basic cursor control

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
		if kEvent.press == kEvent.keys['ctrl+q']:
			self.game_state = False

Basic()
```

Resources
---
- [Console Virtual Terminal Sequences][def]
- [Py-Getch][def2]
- [Javidx9] [def3]


[def]: https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
[def2]: https://github.com/joeyespo/py-getch
[def3]: https://github.com/OneLoneCoder/Javidx9/tree/master/ConsoleGameEngine
