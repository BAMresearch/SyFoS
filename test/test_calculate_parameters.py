import pytest
import numpy as np

import synthetic_force_volumes.generate_synthetic_force_volumes as gsfv

def test_calculate_jtc():
	"""."""
	hamaker = 6
	radius = 4
	kd = 1

	result = gsfv.calculate_jtc(
		hamaker, 
		radius, 
		kd
	)
	
	assert np.isclose(result, -2.0)

def test_calculate_etot():
	"""."""
	possionRatioTip = 1
	eTip = 1
	possionRatioSample = 0.75 
	eSample = 1

	result = gsfv.calculate_etot(
		possionRatioTip, 
		eTip,
		possionRatioSample,
		eSample
	)

	assert np.isclose(result, 2,37)

def test_calculate_hamaker():
	"""."""
	hamakerTip = 9 
	hamakerSample = 16 

	result = gsfv.calculate_hamaker(
		hamakerTip, 
		hamakerSample
	)

	assert np.isclose(result, 12)