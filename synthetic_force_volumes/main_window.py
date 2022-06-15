from collections import namedtuple
from typing import Tuple, List, Dict
import os

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
from matplotlib.lines import Line2D

import default_parameter_values as dpv
import generate_synthetic_force_volumes as gsfv
from toolbar_line_plot import ToolbarLinePlot
from export_window import ExportWindow

class MainWindow(ttk.Frame):
	"""A GUI to create and compare synthetic force volumes."""
	def __init__(self, root):
		self.root = root
		self.root.title("Create Synthetic Force Volumes")

		self.forceVolumes = {}

		self._init_style_parameters()
		self._init_parameter_variables()
		self._create_main_window()

	def _init_style_parameters(self) -> None:
		"""Initialise all style related parameters."""
		self.colorActiveCurves = "#00c3ff"
		self.colorActiveIdealCurve = "#fc0008"
		self.colorInactiveCurves = "#b0b0b0"

		style = ttk.Style()
		style.configure("Subscript.TLabel", font=("Helvetica", 14, "italic"))

	def _init_parameter_variables(self) -> None:
		"""Initialise all parameter variables."""
		# Material parameters
		self.kc = tk.StringVar(self.root, value="")
		self.radius = tk.StringVar(self.root, value="")
		self.eSample = tk.StringVar(self.root, value="")
		self.possionRatioSample = tk.StringVar(self.root, value="")
		self.hamakerSample = tk.StringVar(self.root, value="")

		# Measurement parameters
		self.z0 = tk.StringVar(self.root, value="")
		self.dZ = tk.StringVar(self.root, value="")
		self.eTip = tk.StringVar(self.root, value="")
		self.possionRatioTip = tk.StringVar(self.root, value="")
		self.hamakerTip = tk.StringVar(self.root, value="")
		self.maximumDeflection = tk.StringVar(self.root, value="")

		# Force Volume parameters
		self.numberOfCurves = tk.StringVar(self.root, value="4")
		self.noise = tk.StringVar(self.root, value="1e-10")
		self.virtualDeflection = tk.StringVar(self.root, value="3e-9")
		self.topography = tk.StringVar(self.root, value="10e-9")

		# Calculated parameters
		self.etot = tk.StringVar(self.root, value="")
		self.jtc = tk.StringVar(self.root, value="")
		self.hamaker = tk.StringVar(self.root, value="")

		self.parameters = [
			self.kc,
			self.radius,
			self.eSample,
			self.possionRatioSample,
			self.hamakerTip,
			self.hamakerSample,
			self.z0,
			self.dZ,
			self.eTip,
			self.possionRatioTip,
			self.maximumDeflection,
			self.numberOfCurves,
			self.noise,
			self.virtualDeflection,
			self.topography
		]

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
		frameParameters.pack(fill=X, expand=YES, padx=15, pady=15)

		# Probe section
		labelCategoryMaterial = ttk.Label(
			frameParameters, 
			text="Probe", 
			font="bold"
		)
		labelCategoryMaterial.grid(row=0, column=0, sticky=W, pady=(0, 5))

		self.defaultMaterial = tk.StringVar(self.root, value="Material")
		dropdownDefaultMaterial = ttk.OptionMenu(
			frameParameters, 
			self.defaultMaterial, 
			"",
			*dpv.defaultMaterials.keys(), 
			command=self._set_default_material_parameters,
			bootstyle=""
		)
		dropdownDefaultMaterial.grid(row=0, column=1, sticky=W, pady=(0, 5))

		labelKc = ttk.Label(frameParameters, text="kc:")
		labelKc.grid(row=1, column=0, sticky=W)

		entryKc = ttk.Entry(
			frameParameters, 
			textvariable=self.kc, 
			validate="focusout", 
			validatecommand=self._set_material_label
		)
		entryKc.grid(row=1, column=1)

		labelRadius = ttk.Label(frameParameters, text="Radius:")
		labelRadius.grid(row=2, column=0, sticky=W)

		entryRadius = ttk.Entry(
			frameParameters, 
			textvariable=self.radius, 
			validate="focusout", 
			validatecommand=self._set_material_label
		)
		entryRadius.grid(row=2, column=1)

		labelETip = ttk.Label(
			frameParameters, 
			text="e\u209C\u1d62\u209a", 
			style="Subscript.TLabel"
		)
		labelETip.grid(row=3, column=0, sticky=W)

		entryETip = ttk.Entry(
			frameParameters, 
			textvariable=self.eTip, 
			validate="focusout", 
			validatecommand=self._set_material_label
		)
		entryETip.grid(row=3, column=1)

		labelPossionRatioTip = ttk.Label(frameParameters, text="Possion Ratio:")
		labelPossionRatioTip.grid(row=4, column=0, sticky=W)

		entryPossionRatioTip = ttk.Entry(
			frameParameters, 
			textvariable=self.possionRatioTip, 
			validate="focusout", 
			validatecommand=self._set_material_label
		)
		entryPossionRatioTip.grid(row=4, column=1)

		labelHamakerTip = ttk.Label(frameParameters, text="Hamaker:")
		labelHamakerTip.grid(row=5, column=0, sticky=W)

		entryHamakerTip = ttk.Entry(
			frameParameters, 
			textvariable=self.hamakerTip, 
			validate="focusout", 
			validatecommand=self._set_material_label
		)
		entryHamakerTip.grid(row=5, column=1)

		# Sample section
		labelCategoryMeasurement = ttk.Label(
			frameParameters, 
			text="Sample", 
			font="bold"
		)
		labelCategoryMeasurement.grid(row=0, column=2, sticky=W, pady=(0, 5))

		self.defaultMeasurement = tk.StringVar(self.root, value="Material")
		dropdownDefaultMeasurement = ttk.OptionMenu(
			frameParameters, 
			self.defaultMeasurement, 
			"",
			*dpv.defaultMeasurements.keys(), 
			command=self._set_default_measurement_parameters,
			bootstyle=""
		)
		dropdownDefaultMeasurement.grid(row=0, column=3, sticky=W, pady=(0, 5))

		labelESample = ttk.Label(frameParameters, text="ESample:")
		labelESample.grid(row=1, column=2, sticky=W)

		entryESample = ttk.Entry(
			frameParameters, 
			textvariable=self.eSample, 
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryESample.grid(row=1, column=3)

		labelPossionRatioSample = ttk.Label(frameParameters, text="Possion Ratio:")
		labelPossionRatioSample.grid(row=2, column=2, sticky=W)

		entryPossionRatioSample = ttk.Entry(
			frameParameters, 
			textvariable=self.possionRatioSample, 
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryPossionRatioSample.grid(row=2, column=3)

		labelHamakerSample = ttk.Label(frameParameters, text="Hamaker:")
		labelHamakerSample.grid(row=3, column=2, sticky=W)

		entryHamakerSample = ttk.Entry(
			frameParameters, 
			textvariable=self.hamakerSample, 
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryHamakerSample.grid(row=3, column=3)

		#Experimental section
		labelCategoryForceVolume = ttk.Label(
			frameParameters, 
			text="Force Spectroscopy Experiment", 
			font="bold"
		)
		labelCategoryForceVolume.grid(row=0, column=4, columnspan=2, sticky=W, pady=(0, 5))

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
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryMaximumDeflection.grid(row=2, column=5)

		labelZ0 = ttk.Label(frameParameters, text="z0:")
		labelZ0.grid(row=3, column=4, sticky=W)

		entryZ0 = ttk.Entry(
			frameParameters, 
			textvariable=self.z0, 
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryZ0.grid(row=3, column=5)

		labelDZ = ttk.Label(frameParameters, text="dZ:")
		labelDZ.grid(row=4, column=4, sticky=W)

		entryDZ = ttk.Entry(
			frameParameters, 
			textvariable=self.dZ,
			validate="focusout", 
			validatecommand=self._set_measurement_label
		)
		entryDZ.grid(row=4, column=5)	

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

	def _create_frame_lineplot(self) -> None:
		"""Define all elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(self.root, text="Presentation", padding=15)
		frameLinePlot.pack(side=LEFT, fill=X, expand=YES, padx=15, pady=15)

		rowVariables = ttk.Frame(frameLinePlot)
		rowVariables.pack(fill=X, expand=YES, padx=(15, 0), pady=(0, 10))

		labelEtot = ttk.Label(rowVariables, text="etot:")
		labelEtot.pack(side=LEFT, fill=X, expand=YES)

		entryEtot = ttk.Entry(rowVariables, textvariable=self.etot, state="readonly")
		entryEtot.pack(side=LEFT, fill=X, expand=YES, padx=(0, 20))

		labelJtc = ttk.Label(rowVariables, text="jtc:")
		labelJtc.pack(side=LEFT, fill=X, expand=YES)

		entryJtc = ttk.Entry(rowVariables, textvariable=self.jtc, state="readonly")
		entryJtc.pack(side=LEFT, fill=X, padx=(0, 15), expand=YES)

		labelHamaker = ttk.Label(rowVariables, text="hamaker:")
		labelHamaker.pack(side=LEFT, fill=X, expand=YES)

		entryHamaker = ttk.Entry(rowVariables, textvariable=self.hamaker, state="readonly")
		entryHamaker.pack(side=LEFT, fill=X, padx=(0, 15), expand=YES)

		rowLinePlot = ttk.Frame(frameLinePlot)
		rowLinePlot.pack(fill=X, expand=YES)

		figureLinePlot = Figure(figsize=(6, 5), facecolor=("#d3d3d3"))
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
			command=self._save_force_volume,
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

	def _set_material_label(self) -> None:
		"""Change the material label if the user changes 
		   any of it's parameters."""
		self.defaultMaterial.set("Custom Material")

	def _set_measurement_label(self) -> None:
		"""Change the measurement label if the user changes 
		   any of it's parameters."""
		self.defaultMeasurement.set("Custom Measurement")

	def _set_default_material_parameters(self, defaultMaterial:str) -> None:
		"""Set the values of different default materials.

		Parameter:
			defaultMaterial(str): Name of the chosen default material.
		"""
		self.eTip.set(dpv.defaultMaterials[defaultMaterial]["e"])
		self.possionRatioTip.set(dpv.defaultMaterials[defaultMaterial]["possionRatio"])
		self.hamakerTip.set(dpv.defaultMaterials[defaultMaterial]["hamaker"])
		self.kc.set(dpv.defaultMaterials[defaultMaterial]["kc"])
		self.radius.set(dpv.defaultMaterials[defaultMaterial]["radius"])

	def _set_default_measurement_parameters(self, defaultMeasurement:str) -> None:
		"""Set the the values of different default measurement settings.

		Parameter:
			defaultMeasurement(str): Name of the chosen default measurement settings.
		"""
		self.eSample.set(dpv.defaultMaterials[defaultMeasurement]["e"])
		self.possionRatioSample.set(dpv.defaultMaterials[defaultMeasurement]["possionRatio"])
		self.hamakerSample.set(dpv.defaultMaterials[defaultMeasurement]["hamaker"])
		self.maximumDeflection.set(dpv.defaultMaterials[defaultMeasurement]["maximumDeflection"])
		self.z0.set(dpv.defaultMaterials[defaultMeasurement]["z0"])
		self.dZ.set(dpv.defaultMaterials[defaultMeasurement]["dZ"])

	def _create_force_volume(self) -> tk.messagebox:
		"""Create a synthetic force volume with the chosen parameters and display it.

		Returns:
			userFeedback(tk.messagebox): Informs the user whether the force volume could be created or not.
		"""
		try:
			self._check_parameters()
		except ValueError:
			self._reset_parameters()
			return messagebox.showerror(
				"Error", 
				"Please select valid parameters."
			)

		parameterMaterial, parameterMeasurement, parameterForcevolume = self._get_parameters()

		try:
			syntheticForcevolume = gsfv.create_synthetic_force_volume(
				parameterMaterial, 
				parameterMeasurement, 
				parameterForcevolume
			)
		except ValueError:
			self._reset_parameters()
			return messagebox.showerror(
				"Error", 
				"Failed to generate a synthetic force volume. Please change the input parameters."
			)

		self._display_force_volume(
			syntheticForcevolume,
			parameterMaterial.Etot,
			parameterMaterial.jtc,
			parameterMaterial.Hamaker
		)

		return messagebox.showinfo(
			"Success", 
			"Added synthetic force volume."
		)

	def _check_parameters(self) -> None:
		"""Check wether all input parameters are valid."""
		for parameter in self.parameters:
			try:
				float(parameter.get())
			except ValueError:
				raise ValueError("Invalid input parameters!")

	def _reset_parameters(self) -> None:
		"""Reset all input parameters."""
		for parameter in self.parameters:
			parameter.set("")

		self.defaultMaterial.set("Default Materials")
		self.defaultMeasurement.set("Default Measurement")

	def _get_parameters(self) -> Tuple:
		"""Combine all input parameters into namedtuples.
		
		Returns:
			parameterMaterial(namedtuple): Contains every material parameter.
			parameterMeasurement(namedtuple): Contains every measurment parameter.
			parameterForcevolume(namedtuple): Contains every force volume parameter.
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
				"Z0",
				"dZ",
				"maximumdeflection"
			]
		)
		ParameterForcevolume = namedtuple(
			"parameterForcevolume",
			[
				"numberOfCurves",
				"noise",
				"virtualDeflection",
				"topography"
			]
		)

		hamaker = gsfv.calculate_hamaker(
			float(self.hamakerTip.get()),
			float(self.hamakerSample.get())
		)
		
		jtc = gsfv.calculate_jtc(
			hamaker,
			float(self.radius.get()),
			float(self.kc.get())
		)

		etot = gsfv.calculate_etot(
			float(self.possionRatioTip.get()),
			float(self.eTip.get()),
			float(self.possionRatioSample.get()),
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
			Z0=float(self.z0.get()),
			dZ=float(self.dZ.get()),
			maximumdeflection=float(self.maximumDeflection.get()),	
		)

		parameterForcevolume = ParameterForcevolume(
			numberOfCurves=int(self.numberOfCurves.get()),
			noise=float(self.noise.get()),
			virtualDeflection=float(self.virtualDeflection.get()),
			topography=float(self.topography.get())
		)

		return parameterMaterial, parameterMeasurement, parameterForcevolume

	def _display_force_volume(
		self, 
		syntheticForcevolume: List, 
		etot: float, 
		jtc: float,
		hamaker: float
	) -> None:
		"""
		
		Parameters:
			syntheticForcevolume(list): .
			etot(float): .
			jtc(float): .
			hamaker(float): The .
		"""
		lineCollection = self._create_line_collection(syntheticForcevolume)

		newForcevolume = {
			"data": syntheticForcevolume,
			"lineCollection": lineCollection,
			"etot": etot,
			"jtc": jtc,
			"hamaker": hamaker
		}
		nameNewForcevolume = "Force Volume " + str(len(self.forceVolumes) + 1)
		self.forceVolumes[nameNewForcevolume] = newForcevolume

		self.dropdownForceVolumes.set_menu("", *self.forceVolumes.keys())
		self.activeForceVolume.set(nameNewForcevolume)

		self._add_force_volume_to_plot(
			lineCollection
		)

		self._set_active_force_volume()

	def _create_line_collection(
		self, 
		syntheticForcevolume: List
	) -> List[Line2D]:
		"""

		Parameters:
			syntheticForcevolume(list): .

		Returns:
			lineCollection(list): .
		"""
		return [
			self._create_line(line)
			for line in syntheticForcevolume
		]

	@staticmethod
	def _create_line(
		line: List, 
	) -> Line2D:
		"""Creates a displayable line from x and y curve data.

		Parameters:
			line(List): Contains the x and y values of the line.

		Returns:
			line(Line2D): A line that can be added to a plot.
		"""
		return Line2D(
			line[0], 
			line[1], 
			linewidth=0.5, 
		)

	def _add_force_volume_to_plot(
		self, 
		lineCollection: List[Line2D]
	) -> None:
		"""Add a the lines of a synthetic vorce volume to the plot
		   and adjust the view limits.

		Parameters:
			lineCollection(list): Contains all lines of the synthetic force volume.
		"""
		ax = self._get_axes()

		for line in lineCollection:
			ax.add_line(line)

		self._set_current_view_limits(
			ax
		)

		self.holderFigureLinePlot.draw()

	def _get_axes(self):
		"""Create or get axis of the line plot holder.

		Returns:
			axes(axes): New or existing axes of the line plot holder.
		"""
		try:
			return self.holderFigureLinePlot.figure.get_axes()[0]
		except IndexError:
			return self.holderFigureLinePlot.figure.add_subplot(111)

	def _delete_force_volume(self) -> None:
		""""""
		if self.activeForceVolume.get() not in self.forceVolumes:
			return messagebox.showerror(
				"Error", 
				"Please select a Force Volume."
			)		

		self._delete_force_volume_from_plot(
			self.forceVolumes[self.activeForceVolume.get()]["lineCollection"]
		)

		del self.forceVolumes[self.activeForceVolume.get()]
		self.dropdownForceVolumes.set_menu("", *self.forceVolumes.keys())
		self.activeForceVolume.set("Force Volumes")

		self._set_calculated_parameters()

	def _delete_force_volume_from_plot(
		self, 
		lineCollection: List[Line2D]
	) -> None:
		"""

		Parameters:
			lineCollection(list): .
		"""
		for line in lineCollection:
			line.remove()

		self._set_current_view_limits(
			self._get_axes()
		)

		self.holderFigureLinePlot.draw()

	@staticmethod
	def _set_current_view_limits(ax):
		""""""
		ax.relim()
		ax.autoscale_view()

	def _set_active_force_volume(self, forceVolume: str="") -> None:
		"""

		Parameters:
			forceVolume
		"""
		self._set_calculated_parameters(
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["etot"]
			),
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["jtc"]
			),
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["hamaker"]
			)
		)

		for forceVolumeName, forceVolumeData in self.forceVolumes.items():
			if forceVolumeName == self.activeForceVolume.get():
				self._set_active_line_collection(
					forceVolumeData["lineCollection"]
				)
			else:
				self._set_inative_line_collection(
					forceVolumeData["lineCollection"]
				)

	@staticmethod
	def _round_parameter_presentation(
		parameterValue: float
	) -> str: 
		"""

		Parameters:
			parameterValue(float): .

		Returns:
			roundedParameterRepresentation(str): .
		"""
		return '{:.3e}'.format(parameterValue)

	def _set_calculated_parameters(
		self, 
		etot: str = "",
		jtc: str = "",
		hamaker: str = ""
	) -> None:
		"""

		Parameters:
			etot(str): .
			jtc(str): .
			hamaker(str): .
		"""
		self.etot.set(etot)
		self.jtc.set(jtc)
		self.hamaker.set(hamaker)

	def _set_active_line_collection(
		self, 
		lineCollection: List[Line2D]
	) -> None: 
		""".

		Parameters:
			lineCollection(list): .
		"""
		for line in lineCollection[:2]:
			line.set_color(self.colorActiveIdealCurve)
			line.set_zorder(1)

		for line in lineCollection[2:]:
			line.set_color(self.colorActiveCurves)
			line.set_zorder(-1)

		self.holderFigureLinePlot.draw()

	def _set_inative_line_collection(
		self, 
		lineCollection: List[Line2D]
	) -> None:
		""".

		Parameters:
			lineCollection(list): .
		"""
		for line in lineCollection:
			line.set_color(self.colorInactiveCurves)
			line.set_zorder(-1)

		self.holderFigureLinePlot.draw()

	def _save_force_volume(self) -> None:
		""""""
		if self.activeForceVolume.get() not in self.forceVolumes:
			return messagebox.showerror(
				"Error", 
				"Please select a Force Volume."
			)

		ExportWindow(
			self.forceVolumes[self.activeForceVolume.get()]
		)