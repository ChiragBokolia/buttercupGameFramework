from buttercup import *

import time

sp = Entity("girl.sp")

sp2 = Entity("girl.sp")
sp2.flip()

class Basic(Buttercup):
	def ON_INIT(self):
		self.game_state = True

		Screen.background = "b_white"
		Screen.foreground = "b_black"

		Screen.height = sp.height
		Screen.width = sp.width
		
	def ON_UPDATE(self):
		if kEvent.press == keys['ctrl+q']:
			self.game_state = False

		t = int(time.time())
		if t%2 == 0: 
			sp.draw(0, 0)
		else:
			sp2.draw(0,0)

Basic()

