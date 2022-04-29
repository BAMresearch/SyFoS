from collections import namedtuple
from typing import Tuple
import os

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection

import default_parameter_values as dpv

class MainWindow(ttk.Frame):
	"""A GUI to create and compare synthetic force volumes."""
	def __init__(self, root):
		self.root = root
		self.root.title("Create Synthetic Force Volumes")

		self.forceVolumes = []

		self.colorActiveCurves = "#00c3ff"
		self.colorActiveIdealCurve = "#006f91"
		self.colorInactiveCurves = "#b0b0b0"
		self.colorInactiveIdealCurve = "#757575"

		self._init_parameter_variables()
		self._create_main_window()

	def _init_parameter_variables(self) -> None:
		"""Initialise all parameter variables."""
		# Material parameters
		self.kc = tk.StringVar(self.root, value="")
		self.radius = tk.StringVar(self.root, value="")
		self.eSample = tk.StringVar(self.root, value="")
		self.possionRatioSample = tk.StringVar(self.root, value="")
		self.hamaker = tk.StringVar(self.root, value="")

		# Measurement parameters
		self.z0 = tk.StringVar(self.root, value="")
		self.dZ = tk.StringVar(self.root, value="")
		self.eTip = tk.StringVar(self.root, value="")
		self.possionRatioTip = tk.StringVar(self.root, value="")
		self.maximumDeflection = tk.StringVar(self.root, value="")

		# Force Volume parameters
		self.numberOfCurves = tk.StringVar(self.root, value="")
		self.noise = tk.StringVar(self.root, value="")
		self.virtualDeflection = tk.StringVar(self.root, value="")
		self.topography = tk.StringVar(self.root, value="")

		self.parameters = [
			self.kc,
			self.radius,
			self.eSample,
			self.possionRatioSample,
			self.hamaker,
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

		# Calculated parameters
		self.etot = tk.StringVar(self.root, value="")
		self.jtc = tk.StringVar(self.root, value="")

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

		# First row
		labelCategoryMaterial = ttk.Label(frameParameters, text="Material", font="bold")
		labelCategoryMaterial.grid(row=0, column=0, sticky=W, pady=(0, 10))

		self.defaultMaterial = tk.StringVar(self.root, value="Default Material")
		dropdownDefaultMaterial = ttk.OptionMenu(
			frameParameters, 
			self.defaultMaterial, 
			"",
			*dpv.defaultMaterials.keys(), 
			command=self._set_default_material_parameters,
			bootstyle=""
		)
		dropdownDefaultMaterial.grid(row=0, column=1, sticky=W, pady=(0, 10))

		labelCategoryMeasurement = ttk.Label(frameParameters, text="Measurement", font="bold")
		labelCategoryMeasurement.grid(row=0, column=2, sticky=W, pady=(0, 10))

		self.defaultMeasurement = tk.StringVar(self.root, value="Default Measurement")
		dropdownDefaultMeasurement = ttk.OptionMenu(
			frameParameters, 
			self.defaultMeasurement, 
			"",
			*dpv.defaultMeasurements.keys(), 
			command=self._set_default_measurement_parameters,
			bootstyle=""
		)
		dropdownDefaultMeasurement.grid(row=0, column=3, sticky=W, pady=(0, 10))

		labelCategoryForceVolume = ttk.Label(frameParameters, text="Force Volume", font="bold")
		labelCategoryForceVolume.grid(row=0, column=4, columnspan=2, sticky=W, pady=(0, 10))

		# Second row
		labelKc = ttk.Label(frameParameters, text="kc:")
		labelKc.grid(row=1, column=0, sticky=W, pady=(0, 5))

		entryKc = ttk.Entry(frameParameters, textvariable=self.kc)
		entryKc.grid(row=1, column=1, pady=(0, 5))

		labelZ0 = ttk.Label(frameParameters, text="z0:")
		labelZ0.grid(row=1, column=2, sticky=W, pady=(0, 5))

		entryZ0 = ttk.Entry(frameParameters, textvariable=self.z0)
		entryZ0.grid(row=1, column=3, pady=(0, 5))

		labelNumberOfCurves = ttk.Label(frameParameters, text="Number of Curves:")
		labelNumberOfCurves.grid(row=1, column=4, sticky=W, pady=(0, 5))

		entryNumberOfCurves = ttk.Entry(frameParameters, textvariable=self.numberOfCurves)
		entryNumberOfCurves.grid(row=1, column=5, pady=(0, 5))

		# Third row
		labelRadius = ttk.Label(frameParameters, text="Radius:")
		labelRadius.grid(row=2, column=0, sticky=W, pady=(0, 5))

		entryRadius = ttk.Entry(frameParameters, textvariable=self.radius)
		entryRadius.grid(row=2, column=1, pady=(0, 5))

		labelDZ = ttk.Label(frameParameters, text="dZ:")
		labelDZ.grid(row=2, column=2, sticky=W, pady=(0, 5))

		entryDZ = ttk.Entry(frameParameters, textvariable=self.dZ)
		entryDZ.grid(row=2, column=3, pady=(0, 5))

		labelNoise = ttk.Label(frameParameters, text="Noise:")
		labelNoise.grid(row=2, column=4, sticky=W, pady=(0, 5))

		entryNoise = ttk.Entry(frameParameters, textvariable=self.noise)
		entryNoise.grid(row=2, column=5, pady=(0, 5))

		# Fourth row
		labelESample = ttk.Label(frameParameters, text="ESample:")
		labelESample.grid(row=3, column=0, sticky=W, pady=(0, 5))

		entryESample = ttk.Entry(frameParameters, textvariable=self.eSample)
		entryESample.grid(row=3, column=1, pady=(0, 5))

		labelETip = ttk.Label(frameParameters, text="ETip:")
		labelETip.grid(row=3, column=2, sticky=W, pady=(0, 5))

		entryETip = ttk.Entry(frameParameters, textvariable=self.eTip)
		entryETip.grid(row=3, column=3, pady=(0, 5))

		labelVirtualDeflection = ttk.Label(frameParameters, text="Virtual Deflection:")
		labelVirtualDeflection.grid(row=3, column=4, sticky=W, pady=(0, 5))

		entryVirtualDeflection = ttk.Entry(frameParameters, textvariable=self.virtualDeflection)
		entryVirtualDeflection.grid(row=3, column=5, pady=(0, 5))

		# Fifth row
		labelPossionRatioSample = ttk.Label(frameParameters, text="Possion Ratio:")
		labelPossionRatioSample.grid(row=4, column=0, sticky=W, pady=(0, 5))

		entryPossionRatioSample = ttk.Entry(frameParameters, textvariable=self.possionRatioSample)
		entryPossionRatioSample.grid(row=4, column=1, pady=(0, 5))

		labelPossionRatioTip = ttk.Label(frameParameters, text="Possion Ratio:")
		labelPossionRatioTip.grid(row=4, column=2, sticky=W, pady=(0, 5))

		entryPossionRatioTip = ttk.Entry(frameParameters, textvariable=self.possionRatioTip)
		entryPossionRatioTip.grid(row=4, column=3, pady=(0, 5))

		labelTopography = ttk.Label(frameParameters, text="Topography:")
		labelTopography.grid(row=4, column=4, sticky=W, pady=(0, 5))

		entryTopography = ttk.Entry(frameParameters, textvariable=self.topography)
		entryTopography.grid(row=4, column=5)

		# Sixth row
		labelHamaker = ttk.Label(frameParameters, text="Hamaker:")
		labelHamaker.grid(row=5, column=0, sticky=W, pady=(0, 5))

		entryHamaker = ttk.Entry(frameParameters, textvariable=self.hamaker)
		entryHamaker.grid(row=5, column=1, pady=(0, 5))

		labelMaximumDeflection = ttk.Label(frameParameters, text="Maximum Deflection:")
		labelMaximumDeflection.grid(row=5, column=2, sticky=W, pady=(0, 5))

		entryMaximumDeflection = ttk.Entry(frameParameters, textvariable=self.maximumDeflection)
		entryMaximumDeflection.grid(row=5, column=3, pady=(0, 5))

	def _create_frame_lineplot(self) -> None:
		"""Define all elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(self.root, text="Presentation", padding=15)
		frameLinePlot.pack(side=LEFT, padx=15, pady=15)

		figureLinePlot = Figure(figsize=(6, 5), facecolor=("#d3d3d3"))
		self.holderFigureLinePlot = FigureCanvasTkAgg(figureLinePlot, frameLinePlot)
		self.holderFigureLinePlot.get_tk_widget().pack()

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

		self.forceVolume = tk.StringVar(self.root, value="Force Volumes")
		self.activeForveVolumes = []
		
		dropdownForceVolumes = ttk.OptionMenu(
			frameControl, 
			self.forceVolume, 
			"",
			*self.activeForveVolumes, 
			command=self._update_force_volume,
			bootstyle=""
		)
		dropdownForceVolumes.pack()

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

	def _set_default_material_parameters(self, defaultMerial) -> None:
		""""""
		self.kc.set(dpv.defaultMaterials[defaultMerial]["kc"])
		self.radius.set(dpv.defaultMaterials[defaultMerial]["radius"])
		self.eSample.set(dpv.defaultMaterials[defaultMerial]["eTip"])
		self.possionRatioSample.set(dpv.defaultMaterials[defaultMerial]["possionRatio"])
		self.hamaker.set(dpv.defaultMaterials[defaultMerial]["hamaker"])

	def _set_default_measurement_parameters(self, defaultMeasurement) -> None:
		""""""
		self.z0.set(dpv.defaultMeasurements[defaultMeasurement]["z0"])
		self.dZ.set(dpv.defaultMeasurements[defaultMeasurement]["dZ"])
		self.eTip.set(dpv.defaultMeasurements[defaultMeasurement]["eSample"])
		self.possionRatioTip.set(dpv.defaultMeasurements[defaultMeasurement]["possionRatio"])
		self.maximumDeflection.set(dpv.defaultMeasurements[defaultMeasurement]["maximumDeflection"])

	def _create_force_volume(self) -> None:
		""""""
		validParameters = self._check_parameters()
		if not validParameters:
			return 
		parameterMaterial, parameterMeasurement, parameterForcevolume = self._get_parameters()

	def _check_parameters(self) -> bool:
		"""

		"""
		for parameter in self.parameters:
			try:
				float(parameter.get())
			except ValueError:
				self._reset_parameters()
				messagebox.showerror(
					"Error", 
					"Invalid parameter inputs."
				)
				return False

		return True

	def _reset_parameters(self):
		""""""
		for parameter in self.parameters:
			parameter.set("")

		self.defaultMaterial.set("Default Materials")

	def _get_parameters(self) -> Tuple:
		"""
		
		Returns:
			parameterMaterial(namedtuple):
			parameterMeasurement(namedtuple):
			parameterForcevolume(namedtuple):
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
		jtc = - (
			(
				(float(self.hamaker.get())*float(self.radius.get()))
				/(3*float(self.kc.get()))
			)**(1/3)
		)

		etot = (
			4 
			/ (3 * ((1 - float(self.possionRatioTip.get())**2) / float(self.eTip.get()) + (1 - float(self.possionRatioSample.get())**2) / float(self.eSample.get())))
		)

		parameterMaterial = ParameterMaterial(
			kc=float(self.kc.get()),
			radius=float(self.radius.get()),
			Hamaker=float(self.hamaker.get()),
			Etot=etot,
			jtc=jtc,
		)

		parameterMeasurement = ParameterMeasurement(
			Z0=float(self.z0.get()),
			dZ=float(self.dZ.get()),
			maximumdeflection=float(self.maximumdeflection.get()),	
		)

		parameterForcevolume = ParameterForcevolume(
			numberOfCurves=float(self.numberOfCurves.get()),
			noise=float(self.noise.get()),
			virtualDeflection=float(self.virtualDeflection.get()),
			topography=float(self.topography.get())
		)

		return parameterMaterial, parameterMeasurement, parameterForcevolume

	def _save_force_volume(self):
		""""""
		if self.forceVolume.get() not in self.forceVolumes:
			return messagebox.showerror(
				"Error", 
				"Please select a Force Volume."
			)

	def _delete_force_volume(self) -> None:
		""""""
		if self.forceVolume.get() not in self.forceVolumes:
			return messagebox.showerror(
				"Error", 
				"Please select a Force Volume."
			)		

		self.forceVolumes.remove(self.forceVolume.get())
		self.forceVolume.set("Force Volumes")

	def _update_force_volume(self, forceVolume) -> None:
		""""""
		print(forceVolume)

if __name__ == "__main__":
	app = ttk.Window()
	MainWindow(app)
	app.mainloop()