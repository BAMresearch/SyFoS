"""
This file is part of SyFoS.
SyFoS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SyFoS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SyFoS.  If not, see <http://www.gnu.org/licenses/>.
"""

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class ToolbarLinePlot(NavigationToolbar2Tk):
	"""A simplified toolbar to inspect and compare synthetic force volumes."""
	def __init__(self, canvas_, parent_):

		self.toolitems = (
			('Home', 'Reset original view', 'home', 'home'),
			('Back', 'Back to previous view', 'back', 'back'),
			('Forward', 'Forward to next view', 'forward', 'forward'),
			('Pan', 'Move line plot', 'move', 'pan'),
			('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom')
		)

		super().__init__(canvas_, parent_)

		# Adjust the toolbar button color.
		for button in self._buttons.values():
			button.configure(
				bg="#ffffff",
				activebackground="#ffffff"
			)