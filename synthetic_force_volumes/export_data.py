import os 
import csv
from typing import List, Tuple, NamedTuple, Dict

import numpy as np
import pandas as pd

def export_data(
	exportParameters: NamedTuple,
	dataForceVolume: Dict,
	progressbar,
	progressbarLabel
) -> None:
	""""""
	progressbar.start()

	progressbarLabel.set("Preparing data")
	dataFrameForceVolume = create_data_frame(dataForceVolume)

	if exportParameters.exportToCSV:
		export_to_csv(
			dataFrameForceVolume, 
			exportParameters.pathOutputFile
		)
		progressbarLabel.set("Exporting to CSV")

	if exportParameters.exportToExcel:
		export_to_excel(
			dataFrameForceVolume, 
			exportParameters.pathOutputFile
		)
		progressbarLabel.set("Exporting to Excel")

	progressbar.stop()

def create_data_frame(
	dataForceVolume: Dict
) -> pd.DataFrame:
	""""""
	pass

def export_to_csv(
	dataFrameForceVolume: pd.DataFrame,
	pathOutputFile: str
) -> None:
	""""""
	pass 

def export_to_excel(
	dataFrameForceVolume: pd.DataFrame,
	pathOutputFile: str
) -> None:
	""""""
	pass