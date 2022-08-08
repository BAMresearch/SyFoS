from collections import namedtuple

import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

def test_compare_input_parameters_and_calculated_parameters():
	""""""
	pass
	"""
	parameterMaterial, parameterMeasurement, parameterForcevolume = get_simple_test_parameters()

	syntheticForcevolume = gen_data.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	extractedParameters = analyse_data.extraxt_parameters(syntheticForcevolume)

	np.testing.assert_allclose(
		[
			parameterMaterial.Hamaker, 
			parameterMaterial.Etot, 
			parameterMaterial.jtc
		], 
		[
			extractedParameters.Hamaker, 
			extractedParameters.Etot, 
			extractedParameters.jtc
		]
	)
	"""