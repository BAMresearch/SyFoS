"""
This file is part of SOFA.
SOFA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SOFA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SOFA.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import namedtuple
import os
from typing import NamedTuple

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ExportWindow(ttk.Frame):
	"""A subwindow to handle the data export."""
	def __init__(self):
		self.window = tk.Toplevel()
		self.window.title("Export Force Curve")

		self._create_window()

	def _create_window(self) -> None:
		"""Define all elements within the export window."""
		self._create_frame_data_location()
		self._create_frame_data_types()
		self._create_export_button()
		self._create_progressbar()

	def _create_frame_data_location(self) -> None:
		"""Define all elements within the data location frame."""
		frameDataLocation = ttk.Labelframe(self.window, text="Data Location", padding=15)
		frameDataLocation.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		self.fileName = tk.StringVar(self.window, value="")
		self.filePath = tk.StringVar(self.window, value="")

		# Folder name
		rowFileName = ttk.Frame(frameDataLocation)
		rowFileName.pack(fill=X, expand=YES, pady=(10, 15))

		labelFileName = ttk.Label(rowFileName, text="Filename", width=12)
		labelFileName.pack(side=LEFT, padx=(15, 0))

		entryFileName = ttk.Entry(rowFileName, textvariable=self.fileName)
		entryFileName.pack(side=LEFT, fill=X, expand=YES, padx=5)

		# Folder path
		rowFilePath= ttk.Frame(frameDataLocation)
		rowFilePath.pack(fill=X, expand=YES, pady=(10, 15))

		labelFilePath = ttk.Label(rowFilePath, text="Filepath", width=12)
		labelFilePath.pack(side=LEFT, padx=(15, 0))

		entryFilePath = ttk.Entry(rowFilePath, textvariable=self.filePath)
		entryFilePath.pack(side=LEFT, fill=X, expand=YES, padx=5)

		buttonBrowseFilePath = ttk.Button(
			rowFilePath,
			text="Browse",
			command=self._browse_file_path
		)
		buttonBrowseFilePath.pack(side=LEFT, padx=5)

	def _create_frame_data_types(self) -> None:
		"""Define all elements within the data types frame."""
		frameDataTypes = ttk.Labelframe(self.window, text="Data Types", padding=15)
		frameDataTypes.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		self.exportToTxt = tk.BooleanVar(self.window, value=0)
		self.exportToHdf5 = tk.BooleanVar(self.window, value=0)
		self.exportToExcel = tk.BooleanVar(self.window, value=0)

		# Export to txt
		rowExportToTxt = ttk.Frame(frameDataTypes)
		rowExportToTxt.pack(fill=X, expand=YES)

		checkbuttonExportToTxt = ttk.Checkbutton(
			rowExportToTxt,
			text="export to txt",
			variable=self.exportToTxt,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToTxt.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to hdf5
		rowExportToHdf5 = ttk.Frame(frameDataTypes)
		rowExportToHdf5.pack(fill=X, expand=YES)

		checkbuttonExportToHdf5 = ttk.Checkbutton(
			rowExportToHdf5,
			text="export to hdf5",
			variable=self.exportToHdf5,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToHdf5.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to excel
		rowExportToExcel = ttk.Frame(frameDataTypes)
		rowExportToExcel.pack(fill=X, expand=YES)

		checkbuttonExportToExcel = ttk.Checkbutton(
			rowExportToExcel,
			text="export to excel",
			variable=self.exportToExcel,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToExcel.pack(side=LEFT, padx=(15, 0), pady=5)

	def _create_export_button(self) -> None:
		"""Define the export button."""
		rowExportButton = ttk.Frame(self.window)
		rowExportButton.pack(fill=X, expand=YES, pady=(20, 10))

		buttonExportData = ttk.Button(
			rowExportButton,
			text="Export Data",
			command=self._export_data
		)
		buttonExportData.pack(side=LEFT, padx=15)

	def _create_progressbar(self) -> None:
		"""Define the progressbar."""	
		rowLabelProgressbar = ttk.Frame(self.window)
		rowLabelProgressbar.pack(fill=X, expand=YES)

		self.progressbarCurrentLabel = tk.StringVar(self.window, value="")

		labelProgressbar = ttk.Label(rowLabelProgressbar, textvariable=self.progressbarCurrentLabel)
		labelProgressbar.pack(side=RIGHT, padx=15)

		self.progressbar = ttk.Progressbar(
			self.window,
			mode=INDETERMINATE, 
            bootstyle=SUCCESS
		)
		self.progressbar.pack(fill=X, expand=YES, padx=15, pady=(5, 15))

	def _browse_file_path(self) -> None:
		"""Select the directory in which the data will be saved."""
		filePath = fd.askdirectory(
			title="Select directory",
			parent=self.window
		)

		if filePath:
			self.filePath.set(filePath)

	def _export_data(self) -> messagebox:
		"""Export the current state of the data with the selected options.

		Returns:
			userFeedback(messagebox): Informs the user whether the data could be saved or not.
		"""
		# Check if a folder name is selected.
		if not self.folderName.get():
			return messagebox.showerror(
				"Error", 
				"Please specify a name for the ouput folder.", 
				parent=self.window
			)

		# Check if a output folder is selected.
		if not os.path.isdir(self.folderPath.get()):
			return messagebox.showerror(
				"Error", 
				"Please specify a location to save your data.", 
				parent=self.window
			)

		selectedExportParameters = self._create_selected_export_parameters()

		exp_data.export_data(
			self.dataHandler,
			selectedExportParameters,
			self.progressbar,
			self.progressbarCurrentLabel
		)
		# Close window
		self.window.destroy()

		return messagebox.showinfo("Success", "Data is saved.")

	def _create_selected_export_parameters(self) -> NamedTuple:
		"""Summarize the selected export options for easier use.

		Returns:
			ExportOptions(namedtuple): Contains the selected export opotions.
		"""
		ExportOptions = namedtuple(
			"ExportOptions",
			[
				"folderName",
				"folderPath",
				"exportToTxt",
				"exportToHdf5",
				"exportToExcel"
			]	
		)

		return ExportOptions(
			folderName=self.folderName.get(),
			folderPath=self.folderPath.get(),
			exportToTxt=self.exportToTxt.get(),
			exportToHdf5=self.exportToHdf5.get(),
			exportToExcel=self.exportToExcel.get()
		)