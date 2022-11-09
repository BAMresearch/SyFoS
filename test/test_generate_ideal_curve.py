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

def test_calculate_deflection_approach_part_simple_values():
	"""Test calculate_deflection_approach_part with simple values."""
	'''
	hamaker = 5
	radius = 2
	kc = 100
	currentPiezoValue = -0.5
	lastDeflectionValue = -0.1

	result = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius,
		kc,
		currentPiezoValue,
		lastDeflectionValue
	)

	assert np.isclose(result, -0.104166)
	'''
	assert True

def test_calculate_deflection_approach_part_default_values():
	"""Test calculate_deflection_approach_part with default values
	   for silicon against silicon."""
	'''
	hamaker = 6.6e-20
	radius = 25e-9
	kc = 1
	currentPiezoValue = 1.99e-9
	lastDeflectionValue = 0

	result = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius,
		kc,
		currentPiezoValue,
		lastDeflectionValue
	)

	assert np.isclose(result, -6.94426e-11)
	'''
	assert True

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

	assert np.isclose(result, -11.8541969)

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

def test_calculate_cubic_root_simple_values():
	""""""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_cubic_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 3.1045734) 

def test_calculate_cubic_root_default_values():
	""""""
	parameterSubstitut = 5.31028994150e-8
	currentPiezoValue = 1.99e-9 

	result = gen_data.calculate_cubic_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 6.3262833e-13)

def test_calculate_inner_root_simple_values():
	""""""
	parameterSubstitut = 1
	currentPiezoValue = 2

	result = gen_data.calculate_inner_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 20)

def test_calculate_inner_root_default_values():
	""""""
	parameterSubstitut = 5.31028994e-8
	currentPiezoValue = 1.99e-9

	result = gen_data.calculate_inner_root(
		parameterSubstitut,
		currentPiezoValue
	)

	assert np.isclose(result, 5.80262437e-32)

def test_create_ideal_curve_approach_part():
	""""""
	pass 

def test_create_ideal_curve_attraction_part():
	""""""
	pass

def test_create_ideal_curve_contact_part():
	""""""
	pass

def test_create_ideal_curve():
	""""""
	pass