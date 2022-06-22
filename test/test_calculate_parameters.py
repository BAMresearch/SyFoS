import pytest
import numpy as np

import syfos.generate_data as gen_data

def test_calculate_jtc_simple_values():
	"""."""
	hamaker = 6
	radius = 4
	kd = 1

	result = gen_data.calculate_jtc(
		hamaker, 
		radius, 
		kd
	)
	
	assert np.isclose(result, -2.0)

def test_calculate_jtc_small_values():
	"""."""
	pass

def test_calculate_etot_simple_values():
	"""."""
	possionRatioTip = 1
	eTip = 1
	possionRatioSample = 0.75 
	eSample = 1

	result = gen_data.calculate_etot(
		possionRatioTip, 
		eTip,
		possionRatioSample,
		eSample
	)

	assert np.isclose(result, 2,37)

def test_calculate_etot_small_values():
	"""."""
	pass

def test_calculate_hamaker_simple_values():
	"""."""
	hamakerTip = 9 
	hamakerSample = 16 

	result = gen_data.calculate_hamaker(
		hamakerTip, 
		hamakerSample
	)

	assert np.isclose(result, 12)

def test_calculate_hamaker_small_values():
	"""."""
	pass