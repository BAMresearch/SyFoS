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
import os 
import csv
from typing import List, NamedTuple, Dict, Callable

import numpy as np
import pandas as pd

def export_data(
	exportParameters: NamedTuple,
	dataForceVolume: Dict,
	update_progressbar: Callable,
) -> None:
	"""Export the active force volume to every selected data format.

	Parameters:
		exportParameters(namedtuple): Contains the selected export parameters and options.
		dataForceVolume(dict): Contains the data of the selected force Volume.
		update_progressbar(function): Indicates the export progress.
	"""
	update_progressbar(start=True, newLabel="Preparing data")
	
	dataFrameForceVolume = create_data_frame_force_volume(
		dataForceVolume["data"]
	)
	dataFrameMetaData = create_data_frame_meta_data(
		dataForceVolume["etot"],
		dataForceVolume["jtc"],
		dataForceVolume["hamaker"]
	)

	if exportParameters.exportToCSV:
		export_to_csv(
			dataFrameForceVolume, 
			exportParameters.pathOutputFile
		)
		update_progressbar(newLabel="Exporting to CSV")

	if exportParameters.exportToExcel:
		export_to_excel(
			dataFrameForceVolume,
			dataFrameMetaData, 
			exportParameters.pathOutputFile
		)
		update_progressbar(newLabel="Exporting to Excel")

	update_progressbar(stop=True)

def create_data_frame_force_volume(
	dataForceVolumeCurves: np.ndarray
) -> pd.DataFrame:
	"""Create a data frame from the curve data of a force volume. 

	Parameters:
		dataForceVolumeCurves(np.ndarray): Contains the data of every curve of the force Volume.

	Returns:
		dataFrameForceVolume(pd.dataframe): Contains the data of every curve of the force Volume.
	"""
	dataForceVolumeCurvesStacked = np.column_stack(
		[
			np.column_stack((curve[0], curve[1]))
			for curve 
			in dataForceVolumeCurves
		]
	)
	columnNames = create_column_names(len(dataForceVolumeCurves))

	return pd.DataFrame(dataForceVolumeCurvesStacked, columns=columnNames)

def create_column_names(
	numberOfCurves: int
) -> List[str]:
	"""Create a label for each curve in a force volume.
	
	Parameters:
		numberOfCurves(int): The number of curves in the force volume. 

	Returns:
		columnNames(list): Contains a label for each curve in the force volume.
	"""
	columnNames = []

	for index in range(numberOfCurves):
		if index == 0:
			columnNames.append("ideal_curve_x_values")
			columnNames.append("ideal_curve_y_values")
		elif index == 1:
			columnNames.append("ideal_curve_shifted_x_values")
			columnNames.append("ideal_curve_shifted_y_values")
		else:
			columnNames.append("curve_" + str(index - 1) + "_x_values")
			columnNames.append("curve_" + str(index - 1) + "_y_values")

	return columnNames

def create_data_frame_meta_data(
	etot: float,
	jtc: float,
	hamaker: float
) -> pd.DataFrame:
	"""Create a data frame from the meta data of a force volume.

	Parameter:
		etot(float): The calculated etot value of the force volume.
		jtc(float): The calculated jtc value of the force volume.
		hamaker(float): The calculated hamaker value of the force volume.

	Returns:
		dataFrameMetaData(pd.dataframe): Contains the meta data of the force Volume.
	"""
	return pd.DataFrame(
		[[etot, jtc, hamaker]],
		columns=["etot", "jtc", "hamaker"]
	)

def export_to_csv(
	dataFrameForceVolume: pd.DataFrame,
	pathOutputFile: str
) -> None:
	"""Export the curve data of a force volume to the csv file format.

	Parameters:
		dataFrameForceVolume(pd.dataframe): Contains the data of every curve of the force Volume.
		pathOutputFile(str): Path of the output file.
	"""
	pathOutputFileAsCsv = pathOutputFile + ".csv"

	dataFrameForceVolume.to_csv(
		pathOutputFileAsCsv,
	)

def export_to_excel(
	dataFrameForceVolume: pd.DataFrame,
	dataFrameMetaData: pd.DataFrame,
	pathOutputFile: str
) -> None:
	"""Export the data of a force volume to the xlsx file format.
	
	Parameters:
		dataFrameForceVolume(pd.dataframe): Contains the data of every curve of the force Volume.
		dataFrameMetaData(pd.dataframe): Contains the meta data of the force Volume.
		pathOutputFile(str): Path of the output file.
	"""
	pathOutputFileAsExcel = pathOutputFile + ".xlsx"

	with pd.ExcelWriter(pathOutputFileAsExcel) as writer:  
		dataFrameForceVolume.to_excel(
			writer, 
			sheet_name="Data Force Volume"
		)
		dataFrameMetaData.to_excel(
			writer, 
			sheet_name="Meta Data"
		)