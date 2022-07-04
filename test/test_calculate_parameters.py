import pytest
import numpy as np

import syfos.generate_data as gen_data

def test_calculate_jtc_simple_values():
	"""Test calculate_jtc with simple values."""
	hamaker = 6
	radius = 4
	kc = 1

	result = gen_data.calculate_jtc(
		hamaker, 
		radius, 
		kc
	)
	
	assert np.isclose(result, -2.0)

def test_calculate_jtc_gold_values():
	"""Test calculate_jtc with default values for gold."""
	hamaker = 90e-21
	radius = 25e-9
	kc = 1

	result = gen_data.calculate_jtc(
		hamaker, 
		radius, 
		kc
	)
	
	assert np.isclose(result, -9.0856e-10)

def test_calculate_etot_simple_values():
	"""Test calculate_etot with simple values."""
	possionRatioProbe = 1
	eProbe = 1
	possionRatioSample = 0.75 
	eSample = 1

	result = gen_data.calculate_etot(
		possionRatioProbe, 
		eProbe,
		possionRatioSample,
		eSample
	)

	assert np.isclose(result, 2,37)

def test_calculate_etot_gold_silicon_values():
	"""Test calculate_etot with default values for gold and silicon."""
	possionRatioProbe = 0.42
	eProbe = 78e9
	possionRatioSample = 0.22 
	eSample = 170e9

	result = gen_data.calculate_etot(
		possionRatioProbe, 
		eProbe,
		possionRatioSample,
		eSample
	)

	assert np.isclose(result, 82525504488.49124)

def test_calculate_hamaker_simple_values():
	"""Test calculate_hamaker with simple values."""
	hamakerProbe = 9 
	hamakerSample = 16 

	result = gen_data.calculate_hamaker(
		hamakerProbe, 
		hamakerSample
	)

	assert np.isclose(result, 12)

def test_calculate_hamaker_gold_silicon_values():
	"""Test calculate_hamaker with default values for gold and silicon."""
	hamakerProbe = 90e-21
	hamakerSample = 66e-21

	result = gen_data.calculate_hamaker(
		hamakerProbe, 
		hamakerSample
	)

	assert np.isclose(result, 7.70714e-20)