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

from typing import List
import functools

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib
from matplotlib.lines import Line2D

colorActiveIdealCurve = "#fc0008"
colorActiveCurves = "#00c3ff"
colorInactiveCurves = "#b0b0b0"

def decorator_update_plot(function):
	"""Get the axes of a plot, update view limits and redraw the holder."""
	@functools.wraps(function)
	def wrapper_update_plot(*args, **kwargs):
		holder = args[0]
		ax = get_axes(holder)
		function(ax, *args, **kwargs)
		set_current_view_limits(ax)
		holder.draw()

	return wrapper_update_plot

def create_line_collection(
	forceVolume: np.ndarray
) -> List[Line2D]:
	"""Create a list of displayable lines from the data of a force volume.

	Parameters:
		forceVolume(np.ndarray): x and y data of every curve in the force volume.

	Returns:
		lineCollection(list): List of displayable Line2D objects.
	"""
	return [
		create_line(line)
		for line in forceVolume
	]

def create_line(
	lineData: List, 
) -> Line2D:
	"""Creates a displayable line from the x and y data of a curve.

	Parameters:
		lineData(List): x and y values of one curve.

	Returns:
		line(matplotlib.Line2D): Line that can be displayed in the plot.
	"""
	return Line2D(
		lineData[0], 
		lineData[1], 
		linewidth=0.5, 
	)

def get_axes(
	holder: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
) -> matplotlib.axes:
	"""Create or get axes of a figure within a holder.

	Returns:
		axes(axes): New or existing axes of the line plot holder.
	"""
	try:
		return holder.figure.get_axes()[0]
	except IndexError:
		return holder.figure.add_subplot(111)

def set_current_view_limits(
	ax: matplotlib.axes
) -> None:
	"""Rescale the current view limits of a plot."""
	ax.relim()
	ax.autoscale_view()

@decorator_update_plot
def plot_force_volume( 
	ax: matplotlib.axes,
	holder: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg,
	lineCollection: List[Line2D]
) -> None:
	"""Add every line of a force volume to a line plot.

	Parameters:
		ax(matplotlib.axes): Axes of a line plot.
		lineCollection(list): Contains every line of the force volume.
	"""
	for line in lineCollection:
		ax.add_line(line)

@decorator_update_plot	
def delete_force_volume_from_plot(
	ax: matplotlib.axes,
	holder: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg,
	lineCollection: List[Line2D]
) -> None:
	"""Remove all lines of a force volume from a line plot.

	Parameters:
		ax(matplotlib.axes): Axes of a line plot.
		lineCollection(list): Contains every line of the force volume.
	"""
	for line in lineCollection:
		line.remove()

def set_active_line_collection(
	lineCollection: List[Line2D]
) -> None: 
	"""Change the color and z order of an active force volume.

	Parameters:
		lineCollection(list): Contains all lines of the active force volume.
	"""
	# Change color and z order of the ideal and shifeted ideal curve.
	for line in lineCollection[:2]:
		line.set_color(colorActiveIdealCurve)
		line.set_zorder(2)
	# Change color and z order of the other curves.
	for line in lineCollection[2:]:
		line.set_color(colorActiveCurves)
		line.set_zorder(1)

def set_inative_line_collection(
	lineCollection: List[Line2D]
) -> None:
	"""Change the color and z order of an inactive force volume.

	Parameters:
		lineCollection(list): Contains all lines of the inactive force volume.
	"""
	for line in lineCollection:
		line.set_color(colorInactiveCurves)
		line.set_zorder(-1)