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
	"""Export the currently selected force volume to every selected data format.

	Parameters:
		exportParameters(namedtuple): Contains the selected export parameters and options.
		dataForceVolume(dict): Contains the data of the currently selected force Volume.
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
		update_progressbar("Exporting to CSV")

	if exportParameters.exportToExcel:
		export_to_excel(
			dataFrameMetaData,
			dataFrameForceVolume, 
			exportParameters.pathOutputFile
		)
		update_progressbar("Exporting to Excel")

	update_progressbar(stop=True)

def create_data_frame_force_volume(
	dataForceVolumeCurves: List
) -> pd.DataFrame:
	"""

	Parameters:
		dataForceVolumeCurves(list): Contains the data of the force Volume.

	Returns:
		dataFrameForceVolume(pd.dataframe): .
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
	"""
	
	Parameters:
		numberOfCurves(int): . 

	Returns:
		columnNames(list): .
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
	"""

	Parameter:
		etot(float):
		jtc(float):
		hamaker(float):

	Returns:
		dataFrameMetaData(pd.dataframe): .
	"""
	return pd.DataFrame(
		[[etot, jtc, hamaker]],
		columns=["etot", "jtc", "hamaker"]
	)

def export_to_csv(
	dataFrameForceVolume: pd.DataFrame,
	pathOutputFile: str
) -> None:
	"""

	Parameters:
		dataFrameForceVolume(pd.dataframe): 
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
	"""
	
	Parameters:
		dataFrameForceVolume(pd.dataframe):
		dataFrameMetaData(pd.dataframe):
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