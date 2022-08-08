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

from collections import namedtuple
from typing import Tuple, List, Dict
import os
import functools

import numpy as np

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import gui.default_materials as dm
import data_handling.generate_data as gen_data
import data_visualisation.plot_data as plot_data
from data_visualisation.toolbars.toolbar_line_plot import ToolbarLinePlot
from gui.export_window import ExportWindow

def decorator_check_if_force_volume_selected(function):
	"""Check if a force volume is selected."""
	@functools.wraps(function)
	def wrapper_check_if_force_volume_selected(self):
		if self.activeForceVolume.get() not in self.forceVolumes:
			return messagebox.showerror(
				"Error", 
				"Please select a Force Volume."
			)
		else:
			function(self)

	return wrapper_check_if_force_volume_selected

class MainWindow(ttk.Frame):
	"""A GUI to create and compare synthetic force volumes."""
	def __init__(self, root):
		self.root = root
		self.root.title("SyFoS")

		self.forceVolumes = {}

		self._init_style_parameters()
		self._init_parameter_variables()
		self._create_main_window()

	def _init_style_parameters(self) -> None:
		"""Initialise all style related parameters."""
		self.colorPlot = "#e6f7f4"

	def _init_parameter_variables(self) -> None:
		"""Initialise all parameter variables."""
		# Probe parameters
		self.eProbe = tk.StringVar(self.root, value="")
		self.poissonRatioProbe = tk.StringVar(self.root, value="")
		self.hamakerProbe = tk.StringVar(self.root, value="")
		self.kc = tk.StringVar(self.root, value="1")
		self.radius = tk.StringVar(self.root, value="25e-9")

		# Sample parameters
		self.eSample = tk.StringVar(self.root, value="")
		self.poissonRatioSample = tk.StringVar(self.root, value="")
		self.hamakerSample = tk.StringVar(self.root, value="")

		# Experimental parameters
		self.numberOfCurves = tk.StringVar(self.root, value="4")
		self.maximumDeflection = tk.StringVar(self.root, value="30e-9")
		self.initialDistance = tk.StringVar(self.root, value="-10e-9")
		self.distanceInterval = tk.StringVar(self.root, value="0.2e-9")
		self.noise = tk.StringVar(self.root, value="1e-10")
		self.virtualDeflection = tk.StringVar(self.root, value="3e-9")
		self.topography = tk.StringVar(self.root, value="10e-9")

		# Calculated parameters
		self.etot = tk.StringVar(self.root, value="")
		self.jtc = tk.StringVar(self.root, value="")
		self.hamaker = tk.StringVar(self.root, value="")

		self.parameters = {
			"kc": self.kc,
			"Radius": self.radius,
			"e probe": self.eProbe,
			"Poisson Ratio Probe": self.poissonRatioProbe,
			"Hamaker Probe": self.hamakerProbe,
			"e sample": self.eSample,
			"Poisson Ratio Sample": self.poissonRatioSample,
			"Hamaker Sample": self.hamakerSample,	
			"Number Of Curves": self.numberOfCurves,
			"Maximum Deflection": self.maximumDeflection,
			"Initial Distance": self.initialDistance,
			"Distance Interval": self.distanceInterval,
			"Noise": self.noise,
			"Virtual Deflection": self.virtualDeflection,
			"Topography": self.topography
		}

	def _create_main_window(self) -> None: 
		"""Define all elements within the main window."""
		self._create_frame_parameters()
		self._create_frame_lineplot()
		self._create_frame_control()

	def _create_frame_parameters(self) -> None:
		"""Define all elements within the parameter frame."""
		frameParameters = ttk.Labelframe(
			self.root, 
			text="Parameters", 
			padding=15
		)
		frameParameters.pack(fill=X, expand=YES, padx=15, pady=(15, 0))

		# Probe section
		labelProbe = ttk.Label(
			frameParameters, 
			text="Probe", 
			font="bold"
		)
		labelProbe.grid(row=0, column=0, sticky=W, pady=(0, 5))

		self.defaultProbe = tk.StringVar(self.root, value="Default Probe")
		dropdownProbe = ttk.OptionMenu(
			frameParameters, 
			self.defaultProbe, 
			"",
			*dm.defaultMaterials.keys(), 
			command=self._set_default_probe_parameters,
			bootstyle=""
		)
		dropdownProbe.grid(row=0, column=1, sticky=W, padx=(7, 0), pady=(0, 5))

		labelKc = ttk.Label(frameParameters, text="kc:")
		labelKc.grid(row=1, column=0, sticky=W)

		entryKc = ttk.Entry(
			frameParameters, 
			textvariable=self.kc, 
			validate="focusout", 
			validatecommand=self._set_probe_label
		)
		entryKc.grid(row=1, column=1)

		labelRadius = ttk.Label(frameParameters, text="Radius:")
		labelRadius.grid(row=2, column=0, sticky=W)

		entryRadius = ttk.Entry(
			frameParameters, 
			textvariable=self.radius, 
			validate="focusout", 
			validatecommand=self._set_probe_label
		)
		entryRadius.grid(row=2, column=1)
		
		labelEProbe = tk.Text(
			frameParameters, 
			width=10, height=1,
		)
		labelEProbe.tag_configure(
			"subscript", 
			offset=-2, 
			font=("Helvetica", 8, "italic")
		)
		labelEProbe.insert(INSERT, "e", "", "probe", "subscript")
		labelEProbe.config(
			state="disabled",
			borderwidth=0,
			highlightthickness=0
		)
		labelEProbe.grid(row=3, column=0, sticky=W)

		entryEProbe = ttk.Entry(
			frameParameters, 
			textvariable=self.eProbe, 
			validate="focusout", 
			validatecommand=self._set_probe_label
		)
		entryEProbe.grid(row=3, column=1)

		labelPoissonRatioProbe = ttk.Label(frameParameters, text="Poisson Ratio:")
		labelPoissonRatioProbe.grid(row=4, column=0, sticky=W)

		entryPoissonRatioProbe = ttk.Entry(
			frameParameters, 
			textvariable=self.poissonRatioProbe, 
			validate="focusout", 
			validatecommand=self._set_probe_label
		)
		entryPoissonRatioProbe.grid(row=4, column=1)

		labelHamakerProbe = ttk.Label(frameParameters, text="Hamaker:")
		labelHamakerProbe.grid(row=5, column=0, sticky=W)

		entryHamakerProbe = ttk.Entry(
			frameParameters, 
			textvariable=self.hamakerProbe, 
			validate="focusout", 
			validatecommand=self._set_probe_label
		)
		entryHamakerProbe.grid(row=5, column=1)

		# Sample section
		labelSample = ttk.Label(
			frameParameters, 
			text="Sample", 
			font="bold"
		)
		labelSample.grid(row=0, column=2, sticky=W, pady=(0, 5))

		self.defaultSample = tk.StringVar(self.root, value="Default Sample")
		dropdownSample = ttk.OptionMenu(
			frameParameters, 
			self.defaultSample, 
			"",
			*dm.defaultMaterials.keys(), 
			command=self._set_default_sample_parameters,
			bootstyle=""
		)
		dropdownSample.grid(row=0, column=3, sticky=W, padx=(7, 0), pady=(0, 5))

		labelESample = tk.Text(
			frameParameters, 
			width=10, height=1,
		)
		labelESample.tag_configure(
			"subscript", 
			offset=-2, 
			font=("Helvetica", 8, "italic")
		)
		labelESample.insert(INSERT, "e", "", "sample", "subscript")
		labelESample.config(
			state="disabled",
			borderwidth=0,
			highlightthickness=0
		)
		labelESample.grid(row=1, column=2, sticky=W)

		entryESample = ttk.Entry(
			frameParameters, 
			textvariable=self.eSample, 
			validate="focusout", 
			validatecommand=self._set_sample_label
		)
		entryESample.grid(row=1, column=3)

		labelPoissonRatioSample = ttk.Label(frameParameters, text="Poisson Ratio:")
		labelPoissonRatioSample.grid(row=2, column=2, sticky=W)

		entryPoissonRatioSample = ttk.Entry(
			frameParameters, 
			textvariable=self.poissonRatioSample, 
			validate="focusout", 
			validatecommand=self._set_sample_label
		)
		entryPoissonRatioSample.grid(row=2, column=3)

		labelHamakerSample = ttk.Label(frameParameters, text="Hamaker:")
		labelHamakerSample.grid(row=3, column=2, sticky=W)

		entryHamakerSample = ttk.Entry(
			frameParameters, 
			textvariable=self.hamakerSample, 
			validate="focusout", 
			validatecommand=self._set_sample_label
		)
		entryHamakerSample.grid(row=3, column=3)

		# Experimental section
		labelExperiment = ttk.Label(
			frameParameters, 
			text="Force Spectroscopy Experiment", 
			font="bold"
		)
		labelExperiment.grid(row=0, column=4, columnspan=2, sticky=W, pady=(0, 5))

		labelNumberOfCurves = ttk.Label(frameParameters, text="Number of Curves:")
		labelNumberOfCurves.grid(row=1, column=4, sticky=W)

		entryNumberOfCurves = ttk.Entry(
			frameParameters, 
			textvariable=self.numberOfCurves
		)
		entryNumberOfCurves.grid(row=1, column=5)

		labelMaximumDeflection = ttk.Label(frameParameters, text="Maximum Deflection:")
		labelMaximumDeflection.grid(row=2, column=4, sticky=W)

		entryMaximumDeflection = ttk.Entry(
			frameParameters, 
			textvariable=self.maximumDeflection, 
		)
		entryMaximumDeflection.grid(row=2, column=5)

		labelInitialDistance = ttk.Label(frameParameters, text="Initial Distance:")
		labelInitialDistance.grid(row=3, column=4, sticky=W)

		entryInitialDistance = ttk.Entry(
			frameParameters, 
			textvariable=self.initialDistance, 
		)
		entryInitialDistance.grid(row=3, column=5)

		labelDistanceInterval = ttk.Label(frameParameters, text="Distance Interval:")
		labelDistanceInterval.grid(row=4, column=4, sticky=W)

		entryDistanceInterval = ttk.Entry(
			frameParameters, 
			textvariable=self.distanceInterval,
		)
		entryDistanceInterval.grid(row=4, column=5)	

		labelNoise = ttk.Label(frameParameters, text="Noise:")
		labelNoise.grid(row=5, column=4, sticky=W)

		entryNoise = ttk.Entry(
			frameParameters, 
			textvariable=self.noise
		)
		entryNoise.grid(row=5, column=5)

		labelVirtualDeflection = ttk.Label(frameParameters, text="Virtual Deflection:")
		labelVirtualDeflection.grid(row=6, column=4, sticky=W)

		entryVirtualDeflection = ttk.Entry(
			frameParameters, 
			textvariable=self.virtualDeflection
		)
		entryVirtualDeflection.grid(row=6, column=5)

		labelTopography = ttk.Label(frameParameters, text="Topography:")
		labelTopography.grid(row=7, column=4, sticky=W)

		entryTopography = ttk.Entry(
			frameParameters, 
			textvariable=self.topography
		)
		entryTopography.grid(row=7, column=5)
		
		frameParameters.grid_columnconfigure(0, weight=1, pad=3)
		frameParameters.grid_columnconfigure(1, weight=1, pad=3)
		frameParameters.grid_columnconfigure(2, weight=1, pad=3)
		frameParameters.grid_columnconfigure(3, weight=1, pad=3)
		frameParameters.grid_columnconfigure(4, weight=1, pad=3)
		frameParameters.grid_columnconfigure(5, weight=1, pad=3)

		frameParameters.grid_rowconfigure(0, weight=1, pad=3)
		frameParameters.grid_rowconfigure(1, weight=1, pad=3)
		frameParameters.grid_rowconfigure(2, weight=1, pad=3)
		frameParameters.grid_rowconfigure(3, weight=1, pad=3)
		frameParameters.grid_rowconfigure(4, weight=1, pad=3)
		frameParameters.grid_rowconfigure(5, weight=1, pad=3)
		frameParameters.grid_rowconfigure(6, weight=1, pad=3)
		frameParameters.grid_rowconfigure(7, weight=1, pad=3)

	def _create_frame_lineplot(self) -> None:
		"""Define all elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(self.root, text="Presentation", padding=15)
		frameLinePlot.pack(side=LEFT, fill=X, expand=YES, padx=15, pady=15)

		rowVariables = ttk.Frame(frameLinePlot)
		rowVariables.pack(fill=X, expand=YES, padx=(15, 0), pady=(0, 10))

		labelEtot = ttk.Label(rowVariables, text="etot:")
		labelEtot.pack(side=LEFT, fill=X, expand=YES)
		
		entryEtot = ttk.Entry(
			rowVariables, 
			textvariable=self.etot, 
			state="readonly", 
			bootstyle="light"
		)
		entryEtot.pack(side=LEFT, fill=X, expand=YES, padx=(0, 20))

		labelJtc = ttk.Label(rowVariables, text="jtc:")
		labelJtc.pack(side=LEFT, fill=X, expand=YES)

		entryJtc = ttk.Entry(
			rowVariables, 
			textvariable=self.jtc, 
			state="readonly", 
			bootstyle="light"
		)
		entryJtc.pack(side=LEFT, fill=X, padx=(0, 15), expand=YES)

		labelHamaker = ttk.Label(rowVariables, text="hamaker:")
		labelHamaker.pack(side=LEFT, fill=X, expand=YES)

		entryHamaker = ttk.Entry(
			rowVariables, 
			textvariable=self.hamaker, 
			state="readonly", 
			bootstyle="light"
		)
		entryHamaker.pack(side=LEFT, fill=X, padx=(0, 15), expand=YES)

		rowLinePlot = ttk.Frame(frameLinePlot)
		rowLinePlot.pack(fill=X, expand=YES)

		figureLinePlot = Figure(figsize=(6, 5), facecolor=(self.colorPlot))
		self.holderFigureLinePlot = FigureCanvasTkAgg(figureLinePlot, rowLinePlot)
		toolbarLinePlot = ToolbarLinePlot(
			self.holderFigureLinePlot, 
			rowLinePlot,
		)
		self.holderFigureLinePlot.get_tk_widget().pack(
			side=TOP, fill=BOTH, expand=YES
		)
		toolbarLinePlot.pack(side=BOTTOM, fill=X)

	def _create_frame_control(self) -> None:
		"""Define all elements within the control frame."""
		frameControl = ttk.Labelframe(self.root, text="Control", padding=15)
		frameControl.pack(side=RIGHT, fill=X, expand=YES, anchor=N, padx=15, pady=15)

		buttonCreateForceVolume = ttk.Button(
			frameControl,
			text="Create Force Volume",
			command=self._create_force_volume
		)
		buttonCreateForceVolume.pack(pady=(0, 10))

		seperator = ttk.Separator(frameControl)
		seperator.pack(fill=X, expand=YES, pady=(0, 50))

		self.activeForceVolume = tk.StringVar(self.root, value="Force Volumes")
		
		self.dropdownForceVolumes = ttk.OptionMenu(
			frameControl, 
			self.activeForceVolume, 
			"",
			*self.forceVolumes.keys(), 
			command=self._set_active_force_volume,
			bootstyle=""
		)
		self.dropdownForceVolumes.pack()

		buttonSaveForceVolume = ttk.Button(
			frameControl,
			text="Save Force Volume",
			command=self._export_force_volume,
			width=20
		)
		buttonSaveForceVolume.pack(pady=(20, 0))

		buttonDeleteForceVolume = ttk.Button(
			frameControl,
			text="Delete Force Volume",
			command=self._delete_force_volume,
			width=20
		)
		buttonDeleteForceVolume.pack(pady=(10, 0))

	def _set_probe_label(self) -> None:
		"""Change the probe label if the user changes 
		   any of it's parameters."""
		self.defaultProbe.set("Custom Probe")

	def _set_sample_label(self) -> None:
		"""Change the sample label if the user changes 
		   any of it's parameters."""
		self.defaultSample.set("Custom Sample")

	def _set_default_probe_parameters(self, defaultProbe:str) -> None:
		"""Set the parameters of a selected default probe material.

		Parameter:
			defaultProbe(str): Name of the chosen default probe material.
		"""
		self.eProbe.set(dm.defaultMaterials[defaultProbe]["e"])
		self.poissonRatioProbe.set(dm.defaultMaterials[defaultProbe]["poissonRatio"])
		self.hamakerProbe.set(dm.defaultMaterials[defaultProbe]["hamaker"])

	def _set_default_sample_parameters(self, defaultSample:str) -> None:
		"""Set the parameters of a selected default sample material.

		Parameter:
			defaultSample(str): Name of the chosen default sample material.
		"""
		self.eSample.set(dm.defaultMaterials[defaultSample]["e"])
		self.poissonRatioSample.set(dm.defaultMaterials[defaultSample]["poissonRatio"])
		self.hamakerSample.set(dm.defaultMaterials[defaultSample]["hamaker"])

	def _create_force_volume(self) -> tk.messagebox:
		"""Create a synthetic force volume with the selected parameters and display it.

		Returns:
			userFeedback(tk.messagebox): Informs the user whether the force volume could be created or not.
		"""
		try:
			self._check_parameters()
		except ValueError as e:
			self._reset_parameters()
			return messagebox.showerror(
				"Error", 
				e
			)
		else:
			parameterMaterial, parameterMeasurement, parameterForceVolume = self._get_parameters()

		try:
			forceVolume = gen_data.create_synthetic_force_volume(
				parameterMaterial, 
				parameterMeasurement, 
				parameterForceVolume
			)
		except ValueError as e:
			self._reset_parameters()
			return messagebox.showerror(
				"Error", 
				e
			)

		self._cache_force_volume(
			forceVolume,
			parameterMaterial.Etot,
			parameterMaterial.jtc,
			parameterMaterial.Hamaker
		)

		plot_data.plot_force_volume(
			self.holderFigureLinePlot,
			self.forceVolumes[self.activeForceVolume.get()]["lineCollection"]
		)

		return messagebox.showinfo(
			"Success", 
			"Added synthetic force volume."
		)

	def _check_parameters(self) -> None:
		"""Check wether all input parameters are valid.

		Raises:
			ValueError: If a parameter is not a number.
		"""
		for parameterName, parameterVariable in self.parameters.items():
			try:
				float(parameterVariable.get())
			except ValueError:
				raise ValueError(
					"Invalid input parameter.\n" + parameterName + " must be a number."
				)

	def _reset_parameters(self) -> None:
		"""Reset all input parameters."""
		for parameterVariable in self.parameters.values():
			parameterVariable.set("")

		self.defaultProbe.set("Default Probe")
		self.defaultSample.set("Default Sample")

	def _get_parameters(self) -> Tuple:
		"""Group all input parameters into namedtuples.
		
		Returns:
			parameterMaterial(namedtuple): Contains every material parameter.
			parameterMeasurement(namedtuple): Contains every measurment parameter.
			parameterForceVolume(namedtuple): Contains every force volume parameter.
		"""
		ParameterMaterial = namedtuple(
			"ParameterMaterial",
			[
				"kc",
				"radius",
				"Etot",
				"Hamaker",
				"jtc"
			]
		)
		ParameterMeasurement = namedtuple(
			"ParameterMeasurement",
			[
				"initialDistance",
				"distanceInterval",
				"maximumdeflection"
			]
		)
		ParameterForceVolume = namedtuple(
			"parameterForceVolume",
			[
				"numberOfCurves",
				"noise",
				"virtualDeflection",
				"topography"
			]
		)

		hamaker = gen_data.calculate_hamaker(
			float(self.hamakerProbe.get()),
			float(self.hamakerSample.get())
		)
		
		jtc = gen_data.calculate_jtc(
			hamaker,
			float(self.radius.get()),
			float(self.kc.get())
		)

		etot = gen_data.calculate_etot(
			float(self.poissonRatioProbe.get()),
			float(self.eProbe.get()),
			float(self.poissonRatioSample.get()),
			float(self.eSample.get())
		)

		parameterMaterial = ParameterMaterial(
			kc=float(self.kc.get()),
			radius=float(self.radius.get()),
			Hamaker=hamaker,
			Etot=etot,
			jtc=jtc,
		)

		parameterMeasurement = ParameterMeasurement(
			initialDistance=float(self.initialDistance.get()),
			distanceInterval=float(self.distanceInterval.get()),
			maximumdeflection=float(self.maximumDeflection.get()),	
		)

		parameterForceVolume = ParameterForceVolume(
			numberOfCurves=int(self.numberOfCurves.get()),
			noise=float(self.noise.get()),
			virtualDeflection=float(self.virtualDeflection.get()),
			topography=float(self.topography.get())
		)

		return parameterMaterial, parameterMeasurement, parameterForceVolume

	def _cache_force_volume(
		self,
		forceVolume: np.ndarray, 
		etot: float, 
		jtc: float,
		hamaker: float
	) -> None:
		"""Cache the data of a force volume.

		Parameters:
			forceVolume(np.ndarray): Data of the force volume.
			etot(float): etot value of the force volume.
			jtc(float): jtc value of the force volume.
			hamaker(float): hamaker value of the force volume.
		"""
		nameForceVolume = "Force Volume " + str(len(self.forceVolumes) + 1)

		self.forceVolumes[nameForceVolume] = {
			"data": forceVolume,
			"lineCollection": plot_data.create_line_collection(forceVolume),
			"etot": etot,
			"jtc": jtc,
			"hamaker": hamaker
		}

		self._update_dropdown_force_volumes()
		self.activeForceVolume.set(nameForceVolume)
		self._set_active_force_volume()

	def _update_dropdown_force_volumes(self) -> None:
		"""Update the list of generated force volumes in the dropdown menu."""
		self.dropdownForceVolumes.set_menu("", *self.forceVolumes.keys())
	
	@decorator_check_if_force_volume_selected
	def _delete_force_volume(self) -> None:
		"""Delete the active force volume with all its data."""	
		plot_data.delete_force_volume_from_plot(
			self.holderFigureLinePlot,
			self.forceVolumes[self.activeForceVolume.get()]["lineCollection"]
		)
		# Remove force volume from cache.
		del self.forceVolumes[self.activeForceVolume.get()]
		self._update_dropdown_force_volumes()
		self.activeForceVolume.set("Force Volumes")

		self._reset_calculated_parameters()
	
	def _set_active_force_volume(
		self, 
		forceVolume: str=""
	) -> None:
		""".

		Parameters:
			forceVolume(str): .
		"""
		self._set_calculated_parameters(
			self.forceVolumes[self.activeForceVolume.get()]["etot"],
			self.forceVolumes[self.activeForceVolume.get()]["jtc"],
			self.forceVolumes[self.activeForceVolume.get()]["hamaker"]
		)

		for forceVolumeName, forceVolumeData in self.forceVolumes.items():
			if forceVolumeName == self.activeForceVolume.get():
				plot_data.set_active_line_collection(
					forceVolumeData["lineCollection"]
				)
			else:
				plot_data.set_inative_line_collection(
					forceVolumeData["lineCollection"]
				)

		self.holderFigureLinePlot.draw()

	@staticmethod
	def _round_parameter_presentation(
		parameterValue: float
	) -> str: 
		"""Define the format for the parameter presentation in the GUI.

		Parameters:
			parameterValue(float): Calculated parameter value.

		Returns:
			roundedParameterRepresentation(str): Rounded parameter value in scientific format.
		"""
		return '{:.3e}'.format(parameterValue)

	def _set_calculated_parameters(
		self, 
		etot: str,
		jtc: str,
		hamaker: str
	) -> None:
		"""Set the calculated parameters of the active force volume.

		Parameters:
			etot(str): Calculated and rounded etot value.
			jtc(str): Calculated and rounded jtc value.
			hamaker(str): Calculated and rounded hamaker value.
		"""
		self.etot.set(
			self._round_parameter_presentation(etot)
		)
		self.jtc.set(
			self._round_parameter_presentation(jtc)
		)
		self.hamaker.set(
			self._round_parameter_presentation(hamaker)
		)

	def _reset_calculated_parameters(self) -> None:
		"""Reset the calculated parameters if no force volume is active."""
		self.etot.set("")
		self.jtc.set("")
		self.hamaker.set("")
	
	@decorator_check_if_force_volume_selected
	def _export_force_volume(self) -> None:
		"""Open a window to export the data of the active force volume."""
		ExportWindow(
			self.forceVolumes[self.activeForceVolume.get()]
		)