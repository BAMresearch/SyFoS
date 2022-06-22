from collections import namedtuple

import pytest
import numpy as np

import syfos.generate_data as gen_data

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

	extractedParameters = gen_data.extraxt_parameters(syntheticForcevolume)

	np.testing.assert_allclose(
		[parameterMaterial.Hamaker, parameterMaterial.Etot, parameterMaterial.jtc], 
		[extractedParameters.Hamaker, extractedParameters.Etot, extractedParameters.jtc], 
		rtol=1e-5, 
		atol=0
	)
	"""