import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data

def test_calculate_piezo_simple_values():
	"""Test calculate_piezo_value with simple values."""
	startDistance = 2
	stepSize = 1
	index = 3

	result = gen_data.calculate_piezo_value(
		startDistance, 
		stepSize, 
		index
	)
	
	assert np.isclose(result, 5.0)

def test_calculate_piezo_default_values():
	"""Test calculate_piezo_value with default values."""
	startDistance = -10e-9
	stepSize = 0.2e-9
	index = 60

	result = gen_data.calculate_piezo_value(
		startDistance, 
		stepSize, 
		index
	)
	
	assert np.isclose(result, 1.99e-9)

def test_calculate_tip_sample_distance_simple_values():
	"""Test calculate_tip_sample_distance with simple values."""
	piezo = 4
	deflection = 2

	result = gen_data.calculate_tip_sample_distance(
		piezo, 
		deflection
	)
	
	assert np.isclose(result, 2)

def test_calculate_tip_sample_distance_default_values():
	"""Test calculate_tip_sample_distance with default values."""
	piezo = 1e-11
	deflection = 3.88352e-13

	result = gen_data.calculate_tip_sample_distance(
		piezo, 
		deflection
	)
	
	assert np.isclose(result, 9.612e-12)

def test_calculate_deflection_approach_part_simple_values():
	"""Test calculate_deflection_approach_part with simple values."""
	hamaker = 5
	radius = 2
	kc = 100
	tipSampleDistance = -0.4

	result = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius,
		kc,
		tipSampleDistance
	)

	assert np.isclose(result, -0.104166)
	

def test_calculate_deflection_approach_part_default_values():
	"""Test calculate_deflection_approach_part with default values
	   for silicon against silicon."""
	hamaker = 6.6e-20
	radius = 25e-9
	kc = 1
	tipSampleDistance = 1.99e-9

	result = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius,
		kc,
		tipSampleDistance
	)

	assert np.isclose(result, -6.94426e-11)

def test_calculate_deflection_attraction_part_simple_values():
	"""Test calculate_deflection_attraction_part with simple values."""
	currentPiezoValue = -0.5

	result = gen_data.calculate_deflection_attraction_part(
		currentPiezoValue
	)

	assert np.isclose(result, currentPiezoValue)

def test_calculate_deflection_attraction_part_default_values():
	"""Test calculate_deflection_attraction_part with default values."""
	currentPiezoValue = 1.99e-9

	result = gen_data.calculate_deflection_attraction_part(
		currentPiezoValue
	)

	assert np.isclose(result, currentPiezoValue)

def test_calculate_deflection_contact_part_simple_values():
	"""Test calculate_deflection_contact_part with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_deflection_contact_part(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 0.999, rtol=1e-02)

def test_calculate_deflection_contact_part_default_values():
	"""Test calculate_deflection_contact_part with default values
	   for silicon against silicon."""
	parameterSubstitut = 5.31028994150e-8
	currentPiezoValue = 1.99e-9

	result = gen_data.calculate_deflection_contact_part(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 1.9901664e-09)

def test_calculate_deflection_contact_first_term_simple_values():
	"""Test calculate_deflection_contact_first_term with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_deflection_contact_first_term(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 1.6666, rtol=1e-04)

def test_calculate_deflection_contact_second_term_simple_values():
	"""Test calculate_deflection_contact_second_term with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_deflection_contact_second_term(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(np.real(result), 0.8214, rtol=1e-04)

def test_calculate_deflection_contact_third_term_simple_values():
	"""Test calculate_deflection_contact_third_term with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_deflection_contact_third_term(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(np.real(result), 1.488, rtol=1e-04)

def test_calculate_cubic_root_simple_values():
	"""Test calculate_cubic_root with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_cubic_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 3.1045734) 

def test_calculate_cubic_root_default_values():
	"""Test calculate_cubic_root with default values."""
	parameterSubstitut = 5.31028994150e-8
	currentPiezoValue = 1.99e-9 

	result = gen_data.calculate_cubic_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 6.3262833e-13)

def test_calculate_inner_root_simple_values():
	"""Test calculate_inner_root with simple values."""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_inner_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 20)

def test_calculate_inner_root_default_values():
	"""Test calculate_inner_root with default values."""
	parameterSubstitut = 5.31028994e-8
	currentPiezoValue = 1.99e-9

	result = gen_data.calculate_inner_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 5.80262437e-32)
'''
@pytest.mark.parametrize(
    "hamaker, radius, kc, tipSampleDistance, expectedResult",
    [
    	(1, 1, 1, 1, 1), 
    ],
)
def test_create_ideal_curve_approach_part(
	hamaker: float,
	radius: float, 
	kc: float, 
	tipSampleDistance: float,
	expectedResult: float
):
	"""Test calculate_deflection_approach_part with ciritcal values."""
	result = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius,
		kc,
		tipSampleDistance
	)
	
	assert np.isclose(result, expectedResult)
'''
@pytest.mark.parametrize(
    "currentPiezoValue, expectedResult",
    [
    	(1e-11, 1e-11), 
    	(2e-11, 2e-11),
    	(3e-11, 3e-11),
    ],
)
def test_create_ideal_curve_attraction_part(
	currentPiezoValue: float,
	expectedResult: float
):
	"""Test calculate_deflection_attraction_part with ciritcal values."""
	result = gen_data.calculate_deflection_attraction_part(
		currentPiezoValue
	)
	
	assert np.isclose(result, expectedResult)

@pytest.mark.parametrize(
    "parameterSubstitut, currentPiezoValue, expectedResult",
    [
    	(7.6731e-05, 1e-11, 3.88352e-13), 
    	(7.6731e-05, 2e-11, 1.07312e-12),
    	(7.6731e-05, 3e-11, 1.93741e-12),
    	(7.6731e-05, 4e-11, 2.94024e-12),
    	(7.6731e-05, 5e-11, 4.05826e-12),
    	(7.6731e-05, 6e-11, 5.2759e-12)
    ],
)
def test_create_ideal_curve_contact_part_critical_values(
	parameterSubstitut: float,
	currentPiezoValue: float,
	expectedResult: float
):
	"""Test calculate_deflection_contact_part with ciritcal values."""
	result = gen_data.calculate_deflection_contact_part(
		parameterSubstitut,
		currentPiezoValue
	)
	
	assert np.isclose(result, expectedResult)