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
import matplotlib.lines as mlines

colorActiveIdealCurve = "#fc0008"
colorActiveCurves = "#00c3ff"
colorInactiveCurves = "#b0b0b0"

def decorator_label_plot_once(function):
	"""Add labels and a legend to plot once."""
	@functools.wraps(function)
	def wrapper_label_plot_once(*args, **kwargs):
		if not wrapper_label_plot_once.hasRun:
			holder = args[0]
			axes = get_axes(holder)
			label_plot(axes)
			wrapper_label_plot_once.hasRun = True

		function(*args, **kwargs)

	wrapper_label_plot_once.hasRun = False
	return wrapper_label_plot_once

def decorator_update_plot(function):
	"""Get axes, update view limits and redraw the holder of a plot."""
	@functools.wraps(function)
	def wrapper_update_plot(*args, **kwargs):
		holder = args[0]
		axes = get_axes(holder)
		function(axes, *args, **kwargs)
		set_current_view_limits(axes)
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

def label_plot(axes: matplotlib.axes) -> None: 
	"""Add x and y labels as well as a legend to the plot.

	Parameters:
		axes(matplotlib.axes): Axes of a line plot.
	"""
	axes.set_xlabel("Piezo [nm]")
	axes.set_ylabel("Deflection [nm]")
	# Create proxy lines for the legend of the plot.
	idealCurve = mlines.Line2D(
		[], [], 
		color=colorActiveIdealCurve, linewidth=0.5, label="ideal curve"
	)
	curve = mlines.Line2D(
		[], [], 
		color=colorActiveCurves, linewidth=0.5, label="force volume"
	)
	inactiveCurve = mlines.Line2D(
		[], [], 
		color=colorInactiveCurves, linewidth=0.5, label="inactive"
	)
	axes.legend(handles=[idealCurve, curve, inactiveCurve])

def set_current_view_limits(
	axes: matplotlib.axes
) -> None:
	"""Rescale the current view limits of a plot.

	Parameters:
		axes(matplotlib.axes): Axes of a line plot.
	"""
	axes.relim()
	axes.autoscale_view()

@decorator_label_plot_once
@decorator_update_plot
def plot_force_volume( 
	axes: matplotlib.axes,
	holder: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg,
	lineCollection: List[Line2D]
) -> None:
	"""Add every line of a force volume to a line plot.

	Parameters:
		axes(matplotlib.axes): Axes of a line plot.
		holder(matplotlib.FigureCanvasTkAgg): Embedds the figure into the GUI.
		lineCollection(list): Contains every line of the force volume.
	"""
	for line in lineCollection:
		axes.add_line(line)

@decorator_update_plot	
def delete_force_volume_from_plot(
	axes: matplotlib.axes,
	holder: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg,
	lineCollection: List[Line2D]
) -> None:
	"""Remove all lines of a force volume from a line plot.

	Parameters:
		axes(matplotlib.axes): Axes of a line plot.
		holder(matplotlib.FigureCanvasTkAgg): Embedds the figure into the GUI.
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