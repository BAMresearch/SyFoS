from collections import namedtuple

import pytest
import numpy as np

import syfos.generate_data as gen_data
import syfos.analyse_data as analyse_data

def test_compare_actual_and_synthetic_data():
	""""""
	pass
	"""
	parameterMaterial, parameterMeasurement, parameterForcevolume = get_simple_test_parameters()

	syntheticForcevolume = gen_data.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	realForcevolume = [] 

	extractedSyntheticParameters = analyse_data.extraxt_parameters(syntheticForcevolume)
	extractedRealParameters = analyse_data.extraxt_parameters(realForcevolume)

	np.testing.assert_allclose(
		[
			extractedRealParameters.Hamaker, 
			extractedRealParameters.Etot, 
			extractedRealParameters.jtc
		], 
		[
			extractedSyntheticParameters.Hamaker, 
			extractedSyntheticParameters.Etot, 
			extractedSyntheticParameters.jtc
		]
	)
	"""