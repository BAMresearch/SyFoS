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
from typing import Tuple, List, Dict
import os
import functools
import platform 

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

import gui.default_parameters as dp
from gui.tkinter_utility import LabeledParameterInput, ParameterLabel
from gui.export_window import ExportWindow

import data_handling.generate_data as gen_data
import data_visualisation.plot_data as plot_data
from data_visualisation.toolbars.toolbar_line_plot import ToolbarLinePlot

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
		super().__init__(root, padding=5)

		self.pack(fill=BOTH, expand=YES)

		self.forceVolumes = {}

		self._init_style_parameters()
		self._init_parameter_variables()
		
		self._create_main_window()

		self._combine_parameter_inputs()
		self._set_default_setup_parameters()

	def _init_style_parameters(self) -> None:
		"""Initialise all style related parameters."""
		if platform.system() == "Windows":
			self.smallLabelLength = 4
			self.normalLabelLength = 8
			self.wideLabelLength = 20

		else:
			self.smallLabelLength = 3
			self.normalLabelLength = 7
			self.wideLabelLength = 15

		self.colorPlot = "#e6f7f4"

	def _init_parameter_variables(self) -> None:
		"""Initialise all parameter variables."""
		# Calculated parameters
		self.etot = ttk.StringVar(self, value="")
		self.jtc = ttk.StringVar(self, value="")
		self.hamaker = ttk.StringVar(self, value="")

	def _create_main_window(self) -> None: 
		"""Define all elements within the main window."""
		self._create_frame_parameters()
		self._create_frame_lineplot()
		self._create_frame_control()

	def _create_frame_parameters(self) -> None:
		"""Define all elements within the parameter frame."""
		frameParameters = ttk.Labelframe(
			self, 
			text="Parameters", 
			padding=15
		)
		frameParameters.pack(fill=X, expand=YES, padx=15, pady=15)

		numberOfColumns = 6
		numberOfRows = 6

		for index in range(numberOfColumns):
			frameParameters.columnconfigure(index, weight=1)
		for index in range(numberOfRows):
			frameParameters.rowconfigure(index, weight=1)

		paddingColumns = (0, 10)
		paddingRows = (0, 8)

		# Probe Section
		labelProbeSection = ttk.Label(
			frameParameters, 
			text="Probe", 
			font="bold"
		)
		labelProbeSection.grid(
			row=0, 
			column=0, 
			sticky=W, 
			pady=paddingRows
		)

		self.defaultProbe = tk.StringVar(self, value="Default Probe")
		dropdownProbe = ttk.OptionMenu(
			frameParameters, 
			self.defaultProbe, 
			"",
			*dp.defaultMaterials.keys(), 
			command=self._set_default_probe_parameters,
			bootstyle=""
		)
		dropdownProbe.grid(
			row=0, 
			column=1, 
			sticky=W, 
			padx=paddingColumns, 
			pady=paddingRows
		)

		self.inputEProbe = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsProbe["e"],
			self.smallLabelLength
		)
		self.inputEProbe.grid(
			row=1, 
			column=0, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns, 
			pady=paddingRows
		)

		self.inputPoissonRatioProbe = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsProbe["poissonRatio"],
			self.smallLabelLength
		)
		self.inputPoissonRatioProbe.grid(
			row=2, 
			column=0, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputHamakerProbe = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsProbe["hamaker"],
			self.smallLabelLength,
		)
		self.inputHamakerProbe.grid(
			row=3, 
			column=0, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputSpringConstant = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsProbe["springConstant"],
			self.smallLabelLength
		)
		self.inputSpringConstant.grid(
			row=4, 
			column=0, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputRadius = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsProbe["radius"],
			self.smallLabelLength
		)
		self.inputRadius.grid(
			row=5, 
			column=0, 
			columnspan=2, 
			sticky=W,
			padx=paddingColumns 
		)

		# Sample Section
		labelSampleSection = ttk.Label(
			frameParameters, 
			text="Sample", 
			font="bold"
		)
		labelSampleSection.grid(
			row=0, 
			column=2, 
			sticky=W, 
			pady=paddingRows
		)

		self.defaultSample = tk.StringVar(self, value="Default Sample")
		dropdownSample = ttk.OptionMenu(
			frameParameters, 
			self.defaultSample, 
			"",
			*dp.defaultMaterials.keys(), 
			command=self._set_default_sample_parameters,
			bootstyle=""
		)
		dropdownSample.grid(
			row=0, 
			column=3, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputESample = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsSample["e"],
			self.normalLabelLength
		)
		self.inputESample.grid(
			row=1, 
			column=2, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputPoissonRatioSample = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsSample["poissonRatio"],
			self.normalLabelLength
		)
		self.inputPoissonRatioSample.grid(
			row=2, 
			column=2, 
			columnspan=2, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputHamakerSample = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsSample["hamaker"],
			self.normalLabelLength
		)
		self.inputHamakerSample.grid(
			row=3, 
			column=2, 
			columnspan=2, 
			sticky=W,
			padx=paddingColumns
		)

		# Force Spectroscopy Experiment section
		labelExperiment = ttk.Label(
			frameParameters, 
			text="Force Spectroscopy Experiment", 
			font="bold"
		)
		labelExperiment.grid(
			row=0, 
			column=4, 
			sticky=W, 
			pady=paddingRows
		)

		self.inputStartDistance = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsExperiment["startDistance"],
			self.wideLabelLength
		)
		self.inputStartDistance.grid(
			row=1, 
			column=4, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputStepSize = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsExperiment["stepSize"],
			self.wideLabelLength
		)
		self.inputStepSize.grid(
			row=2, 
			column=4, 
			sticky=W,
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputMaximumPiezo = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsExperiment["maximumPiezo"],
			self.wideLabelLength
		)
		self.inputMaximumPiezo.grid(
			row=3, 
			column=4, 
			sticky=W, 
			padx=paddingColumns,  
			pady=paddingRows
		)

		self.inputNumberOfCurves = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsExperiment["numberOfCurves"],
			self.wideLabelLength
		)
		self.inputNumberOfCurves.grid(
			row=4, 
			column=4, 
			sticky=W,
			padx=paddingColumns
		)

		# Artefact section
		labelArtefact = ttk.Label(
			frameParameters, 
			text="Artefacts", 
			font="bold"
		)
		labelArtefact.grid(
			row=0, 
			column=5, 
			sticky=W, 
			pady=paddingRows
		)

		self.inputVirtualDeflection = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsArtefacts["virtualDeflection"],
			self.wideLabelLength
		)
		self.inputVirtualDeflection.grid(
			row=1, 
			column=5, 
			sticky=W, 
			pady=paddingRows
		)

		self.inputTopographyOffset = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsArtefacts["topographyOffset"],
			self.wideLabelLength
		)
		self.inputTopographyOffset.grid(
			row=2, 
			column=5, 
			sticky=W, 
			pady=paddingRows
		)

		self.inputNoise = LabeledParameterInput(
			frameParameters,
			dp.parameterInputsArtefacts["noise"],
			self.wideLabelLength
		)
		self.inputNoise.grid(
			row=3,
			column=5, 
			sticky=W
		)

	def _create_frame_lineplot(self) -> None:
		"""Define all elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(self, text="Presentation", padding=15)
		frameLinePlot.pack(side=LEFT, fill=X, expand=YES, padx=15, pady=15)

		rowVariables = ttk.Frame(frameLinePlot)
		rowVariables.pack(fill=X, expand=YES, padx=(15, 0), pady=(0, 10))

		labelEtot = ParameterLabel(
			rowVariables,
			"",
			"E",
			"total",
			self.smallLabelLength,
		)
		labelEtot.pack(side=LEFT, fill=X, expand=YES)
		
		entryEtot = ttk.Entry(
			rowVariables, 
			textvariable=self.etot, 
			state="readonly", 
			bootstyle="light"
		)
		entryEtot.pack(side=LEFT, fill=X, expand=YES, padx=(0, 20))

		labelJtc = ParameterLabel(
			rowVariables,
			"JTC",
			"",
			"",
			self.smallLabelLength,
		)
		labelJtc.pack(side=LEFT, fill=X, expand=YES)

		entryJtc = ttk.Entry(
			rowVariables, 
			textvariable=self.jtc, 
			state="readonly", 
			bootstyle="light"
		)
		entryJtc.pack(side=LEFT, fill=X, padx=(0, 15), expand=YES)

		labelHamaker = ParameterLabel(
			rowVariables,
			"",
			"A",
			"total",
			self.smallLabelLength,
		)
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
		frameControl = ttk.Labelframe(self, text="Control", padding=15)
		frameControl.pack(side=RIGHT, fill=X, expand=YES, anchor=N, padx=15, pady=15)

		buttonCreateForceVolume = ttk.Button(
			frameControl,
			text="Create Force Volume",
			command=self._create_force_volume
		)
		buttonCreateForceVolume.pack(pady=(0, 10))

		seperator = ttk.Separator(frameControl)
		seperator.pack(fill=X, expand=YES, pady=(0, 50))

		self.activeForceVolume = tk.StringVar(self, value="Force Volumes")
		
		self.dropdownForceVolumes = ttk.OptionMenu(
			frameControl, 
			self.activeForceVolume, 
			"",
			*self.forceVolumes.keys(), 
			command=self._update_active_force_volume,
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

	def _combine_parameter_inputs(self):
		"""Combine the parameter inputs to check and get all values."""
		self.parameterInputs = {
			"e Probe": self.inputEProbe,
			"Poisson Ratio Probe": self.inputPoissonRatioProbe,
			"Hamaker Probe": self.inputHamakerProbe,
			"kc": self.inputSpringConstant,
			"Radius": self.inputRadius,
			"e Sample": self.inputESample,
			"Poisson Ratio Sample": self.inputPoissonRatioSample,
			"Hamaker Sample": self.inputHamakerSample,	
			"Start Distance": self.inputStartDistance,
			"Step Size": self.inputStepSize,
			"Maximum Piezo": self.inputMaximumPiezo,
			"Number Of Curves": self.inputNumberOfCurves,
			"Virtual Deflection": self.inputVirtualDeflection,
			"Topography Offset": self.inputTopographyOffset,
			"Noise": self.inputNoise
		}

	def _set_default_setup_parameters(self) -> None:
		"""Set parameters to a standard setup."""
		self.inputSpringConstant.set("1")
		self.inputRadius.set("25e-9")

		self.inputNumberOfCurves.set("4")
		self.inputMaximumPiezo.set("30e-9")
		self.inputStartDistance.set("-10e-9")
		self.inputStepSize.set("0.2e-9")
		self.inputNoise.set("1e-10")
		self.inputVirtualDeflection.set("3e-9")		
		self.inputTopographyOffset.set("10e-9")

	def _set_default_probe_parameters(self, defaultProbe:str) -> None:
		"""Set the parameters of a selected default probe material.

		Parameter:
			defaultProbe(str): Name of the chosen default probe material.
		"""
		self.inputEProbe.set(dp.defaultMaterials[defaultProbe]["e"])
		self.inputPoissonRatioProbe.set(dp.defaultMaterials[defaultProbe]["poissonRatio"])
		self.inputHamakerProbe.set(dp.defaultMaterials[defaultProbe]["hamaker"])

	def _set_default_sample_parameters(self, defaultSample:str) -> None:
		"""Set the parameters of a selected default sample material.

		Parameter:
			defaultSample(str): Name of the chosen default sample material.
		"""
		self.inputESample.set(dp.defaultMaterials[defaultSample]["e"])
		self.inputPoissonRatioSample.set(dp.defaultMaterials[defaultSample]["poissonRatio"])
		self.inputHamakerSample.set(dp.defaultMaterials[defaultSample]["hamaker"])

	def _create_force_volume(self) -> tk.messagebox:
		"""Create a synthetic force volume with the selected parameters, chache and display it.

		Returns:
			userFeedback(tk.messagebox): Informs the user whether the force volume could be created or not.
		"""
		try:
			self._check_parameters()
		except ValueError as e:
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

		identifierForceVolume = self._create_identifier_force_volume(
			self.defaultProbe.get(),
			self.defaultSample.get()
		)
		self._cache_force_volume(
			identifierForceVolume,
			forceVolume,
			parameterMaterial.Etot,
			parameterMaterial.jtc,
			parameterMaterial.Hamaker
		)
		self._update_dropdown_force_volumes()
		self._set_active_identifier(identifierForceVolume)
		self._set_active_auxilary_parameters()

		plot_data.plot_force_volume(
			self.holderFigureLinePlot,
			self.forceVolumes[self.activeForceVolume.get()]["lineCollection"]
		)
		self._update_plot()

		return messagebox.showinfo(
			"Success", 
			"Added synthetic force volume."
		)

	def _update_active_force_volume(self, activeIdentifier:str) -> None:
		"""Update the auxilary parameters and the 
		   presentation of the new active force volume.

		Parameters:
			activeIdentifier(str): Identifier of the new active force volume.
		"""
		self._set_active_identifier(activeIdentifier)
		self._set_active_auxilary_parameters()
		self._update_plot()

	@decorator_check_if_force_volume_selected
	def _delete_force_volume(self) -> None:
		"""Delete the data and presentation of the active force volume."""	
		plot_data.delete_force_volume_from_plot(
			self.holderFigureLinePlot,
			self.forceVolumes[self.activeForceVolume.get()]["lineCollection"]
		)

		del self.forceVolumes[self.activeForceVolume.get()]

		self._update_dropdown_force_volumes()
		self._set_active_identifier("Force Volumes")
		self._reset_auxilary_parameters()

	def _check_parameters(self) -> None:
		"""Check wether all input parameters are valid.

		Raises:
			ValueError: If a parameter is not a number.
		"""
		for parameterName, parameterInput in self.parameterInputs.items():
			if parameterInput.check_for_valid_value() == False:
				raise ValueError(
					"Invalid value for " + parameterName + "."
				)

	def _get_parameters(self) -> Tuple:
		"""Group all input parameters into namedtuples.
		
		Returns:
			parameterMaterial(namedtuple): Contains every material parameter.
			parameterMeasurement(namedtuple): Contains every measurment parameter.
			parameterForceVolume(namedtuple): Contains every force volume parameter.
		"""
		ParameterMaterial, ParameterMeasurement, ParameterForceVolume = gen_data.get_parameter_tuples()

		hamaker = gen_data.calculate_hamaker(
			float(self.inputHamakerProbe.get()),
			float(self.inputHamakerSample.get())
		)
		jtc = gen_data.calculate_jtc(
			hamaker,
			float(self.inputRadius.get()),
			float(self.inputSpringConstant.get())
		)
		etot = gen_data.calculate_etot(
			float(self.inputPoissonRatioProbe.get()),
			float(self.inputEProbe.get()),
			float(self.inputPoissonRatioSample.get()),
			float(self.inputESample.get())
		)

		parameterMaterial = ParameterMaterial(
			kc=float(self.inputSpringConstant.get()),
			radius=float(self.inputRadius.get()),
			Hamaker=hamaker,
			Etot=etot,
			jtc=jtc,
		)
		parameterMeasurement = ParameterMeasurement(
			startDistance=float(self.inputStartDistance.get()),
			stepSize=float(self.inputStepSize.get()),
			maximumPiezo=float(self.inputMaximumPiezo.get()),	
		)
		parameterForceVolume = ParameterForceVolume(
			numberOfCurves=int(self.inputNumberOfCurves.get()),
			noise=float(self.inputNoise.get()),
			virtualDeflection=float(self.inputVirtualDeflection.get()),
			topographyOffset=float(self.inputTopographyOffset.get())
		)

		return parameterMaterial, parameterMeasurement, parameterForceVolume

	def _create_identifier_force_volume(
		self,
		probeMaterial: str, 
		sampleMaterial: str
	) -> str: 
		"""Create a identifier for a new force volume.

		Parameters:
			probeMaterial(str): Type of probe used to create the force volume.
			sampleMaterial(str): Type of sample used to create the force volume.
	
		Returns:
			identifier(str): Identifier for the new force volume containing
							 information about the type of probe and sample
							 used to create the force volume.
		"""
		return probeMaterial + "|" + sampleMaterial + " " + str(len(self.forceVolumes) + 1)

	def _cache_force_volume(
		self,
		identifier: str,
		forceVolume: np.ndarray, 
		etot: float, 
		jtc: float,
		hamaker: float
	) -> None:
		"""Cache the data of a force volume.

		Parameters:
			identifier(str): Identifier of the force volume.
			forceVolume(np.ndarray): Data of the force volume.
			etot(float): etot value of the force volume.
			jtc(float): jtc value of the force volume.
			hamaker(float): hamaker value of the force volume.
		"""
		self.forceVolumes[identifier] = {
			"data": forceVolume,
			"lineCollection": plot_data.create_line_collection(forceVolume),
			"etot": etot,
			"jtc": jtc,
			"hamaker": hamaker
		}

	def _update_dropdown_force_volumes(self) -> None:
		"""Update the dropdown menu options."""
		self.dropdownForceVolumes.set_menu("", *self.forceVolumes.keys())

	def _set_active_identifier(self, identifier:str) -> None:
		"""Update the identifier of the active force volume.

		Parameters:
			identifier(str): Identifier of the force volume.
		"""
		self.activeForceVolume.set(identifier)
	
	def _update_plot(self) -> None:
		"""Update the presentation of the active force volume."""
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

	def _set_active_auxilary_parameters(self) -> None:
		"""Set the auxilary parameters of the active force volume."""
		self.etot.set(
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["etot"]
			)
		)
		self.jtc.set(
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["jtc"]
			)
		)
		self.hamaker.set(
			self._round_parameter_presentation(
				self.forceVolumes[self.activeForceVolume.get()]["hamaker"]
			)
		)

	def _reset_auxilary_parameters(self) -> None:
		"""Reset the auxilary parameters."""
		self.etot.set("")
		self.jtc.set("")
		self.hamaker.set("")
	
	@decorator_check_if_force_volume_selected
	def _export_force_volume(self) -> None:
		"""Open a window to export the data of the active force volume."""
		exportWindow = ttk.Toplevel("Export Force Curve")
		ExportWindow(
			exportWindow,
			self.forceVolumes[self.activeForceVolume.get()]
		)