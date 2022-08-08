import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data

##################### Unit Testing #####################

def test_calculate_piezo_simple_values():
	"""Test calculate_piezo_value with simple values."""
	initialDistance = 2
	distanceInterval = 1
	index = 3

	result = gen_data.calculate_piezo_value(
		initialDistance, 
		distanceInterval, 
		index
	)
	
	assert np.isclose(result, 5.0)

def test_calculate_piezo_default_values():
	"""Test calculate_piezo_value with default values."""
	initialDistance = -10e-9
	distanceInterval = 0.2e-9
	index = 60

	result = gen_data.calculate_piezo_value(
		initialDistance, 
		distanceInterval, 
		index
	)
	
	assert np.isclose(result, 1.99e-9)

def test_calculate_deflection_approach_part_simple_values():
	""""""
	pass

def test_calculate_deflection_approach_part_default_values():
	""""""
	pass

def test_calculate_deflection_attraction_part_simple_values():
	""""""
	pass

def test_calculate_deflection_attraction_part_default_values():
	""""""
	pass

def test_calculate_deflection_contact_part_simple_values():
	""""""
	pass

def test_calculate_deflection_contact_part_default_values():
	""""""
	pass

################# Integration Testing ##################

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