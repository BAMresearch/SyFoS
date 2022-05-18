from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class ToolbarLinePlot(NavigationToolbar2Tk):
	"""A simplified toolbar to ."""
	def __init__(self, canvas_, parent_):

		self.toolitems = (
			('Home', 'Reset original view', 'home', 'home'),
			('Back', 'Back to previous view', 'back', 'back'),
			('Forward', 'Forward to next view', 'forward', 'forward'),
			('Pan', 'Move line plot', 'move', 'pan'),
			('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom')
		)

		super().__init__(canvas_, parent_)

		for button in self._buttons.values():
			button.configure(
				bg="#ffffff",
				activebackground="#ffffff"
			)