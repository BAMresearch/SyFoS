from collections import namedtuple
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

class MainWindow(ttk.Frame):
	"""A GUI to create and compare synthetic force volumes."""
	def __init__(self, root):
		self.root = root
		self.root.title("Create Synthetic Force Volumes")

		self._init_parameter_variables()
		self._create_main_window()

	def _init_parameter_variables(self):
		"""Initialise all parameter variables."""
		# Material parameters
		self.kc = tk.StringVar(self.root, value="")
		self.raidus = tk.StringVar(self.root, value="")
		self.etot = tk.StringVar(self.root, value="")
		self.hamaker = tk.StringVar(self.root, value="")
		self.jtc = tk.StringVar(self.root, value="")

		# Measurement parameters
		self.z0 = tk.StringVar(self.root, value="")
		self.dZ = tk.StringVar(self.root, value="")
		self.maximumDeflection = tk.StringVar(self.root, value="")

		# Force Volume parameters
		self.numberOfCurves = tk.StringVar(self.root, value="")
		self.noise = tk.StringVar(self.root, value="")
		self.virtualDeflection = tk.StringVar(self.root, value="")
		self.topography = tk.StringVar(self.root, value="")

	def _create_main_window(self): 
		"""Define all elements within the main window."""
		self._create_frame_parameters()
		self._create_frame_lineplot()
		self._create_frame_control()

	def _create_frame_parameters(self):
		"""Define all elements within the parameter frame."""
		frameParameters = ttk.Labelframe(
			self.root, 
			text="Parameters", 
			padding=15
		)
		frameParameters.pack(fill=X, expand=YES, padx=15, pady=15)

		# First row
		labelCategoryMaterial = ttk.Label(frameParameters, text="Material", font="bold")
		labelCategoryMaterial.grid(row=0, column=0, columnspan=2, sticky=W, pady=(0, 10))

		labelCategoryMeasurement = ttk.Label(frameParameters, text="Measurement", font="bold")
		labelCategoryMeasurement.grid(row=0, column=2, columnspan=2, sticky=W, pady=(0, 10))

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

		entryRadius = ttk.Entry(frameParameters, textvariable=self.raidus)
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
		labelEtot = ttk.Label(frameParameters, text="Etot:")
		labelEtot.grid(row=3, column=0, sticky=W, pady=(0, 5))

		entryEtot = ttk.Entry(frameParameters, textvariable=self.etot)
		entryEtot.grid(row=3, column=1, pady=(0, 5))

		labelMaximumDeflection = ttk.Label(frameParameters, text="Maximum Deflection:")
		labelMaximumDeflection.grid(row=3, column=2, sticky=W, pady=(0, 5))

		entryMaximumDeflection = ttk.Entry(frameParameters, textvariable=self.maximumDeflection)
		entryMaximumDeflection.grid(row=3, column=3, pady=(0, 5))

		labelVirtualDeflection = ttk.Label(frameParameters, text="Virtual Deflection:")
		labelVirtualDeflection.grid(row=3, column=4, sticky=W, pady=(0, 5))

		entryVirtualDeflection = ttk.Entry(frameParameters, textvariable=self.virtualDeflection)
		entryVirtualDeflection.grid(row=3, column=5, pady=(0, 5))

		# Fifth row
		labelHamaker = ttk.Label(frameParameters, text="Hamaker:")
		labelHamaker.grid(row=4, column=0, sticky=W, pady=(0, 5))

		entryHamaker = ttk.Entry(frameParameters, textvariable=self.hamaker)
		entryHamaker.grid(row=4, column=1, pady=(0, 5))

		labelTopography = ttk.Label(frameParameters, text="Topography:")
		labelTopography.grid(row=4, column=4, sticky=W, pady=(0, 5))

		entryTopography = ttk.Entry(frameParameters, textvariable=self.topography)
		entryTopography.grid(row=4, column=5)

	def _create_frame_lineplot(self):
		"""Define all elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(self.root, text="Presentation", padding=15)
		frameLinePlot.pack(side=LEFT, padx=15, pady=15)

		figureLinePlot = Figure(figsize=(6, 5), facecolor=("#d3d3d3"))
		self.holderFigureLinePlot = FigureCanvasTkAgg(figureLinePlot, frameLinePlot)
		self.holderFigureLinePlot.get_tk_widget().pack()

	def _create_frame_control(self):
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

	def _create_force_volume(self):
		""""""
		pass

	def _save_force_volume(self):
		""""""
		pass

	def _compare_force_volume(self):
		""""""
		pass

	def _delete_force_volume(self):
		""""""
		pass

	def _update_force_volume(self):
		""""""
		pass

if __name__ == "__main__":
	app = ttk.Window()
	MainWindow(app)
	app.mainloop()