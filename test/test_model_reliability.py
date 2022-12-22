import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

def test_approach_part_simple_values():
	"""Create a single datapoint in the approach part of the ideal curve,
	   calculate the theoretical input parameters from the value pair
	   and compare the actual with the theoretical values.   
	"""
	# Setup input parameters.
	startDistance = -10e-9
	stepSize = 0.01e-9

	hamaker = 6.6e-20
	radius = 25e-9
	kc = 1

	currentLength = 250
	previousPiezoValue = -7.51e-9
	previousDeflectionValue = 4.869e-12
	# Generate a single datapoint in the approach part of the ideal curve.
	tipSampleDistance = gen_data.calculate_tip_sample_distance(
		previousPiezoValue,
		previousDeflectionValue
	)
	piezoApproach = gen_data.calculate_piezo_value(
		startDistance,
		stepSize,
		currentLength
	)
	deflectionApproach = gen_data.calculate_deflection_approach_part(
		hamaker,
		radius, 
		kc, 
		tipSampleDistance
	)
	datapoint = [piezoApproach, deflectionApproach]
	# Calculate the theoretical parameters using the generated data point.
	trueDistance = analyse_data.calculate_true_distance(datapoint)
	pseudoForce = analyse_data.calculate_adjusted_pseudo_force(datapoint)
	force = analyse_data.calculate_adjusted_force(datapoint, kc)

	theoreticalKc = analyse_data.calculate_kc_approach(
		trueDistance,
		pseudoForce,
		hamaker,
		radius
	)
	theoreticalRadius = analyse_data.calculate_radius_approach(
		trueDistance,
		pseudoForce,
		hamaker,
		kc
	)
	theoreticalHamaker = analyse_data.calculate_hamaker_approach(
		trueDistance,
		pseudoForce,
		radius,
		kc
	)
	# Check if the parameter values coincide with the calculated theoretical values.
	kcIsClose = np.isclose(kc, theoreticalKc, rtol=1e-2)
	radiusIsClose = np.isclose(radius, theoreticalRadius)
	hamakerIsClose = np.isclose(hamaker, theoreticalHamaker)

	assert np.asarray([kcIsClose, radiusIsClose, hamakerIsClose]).all()

def test_contact_part_simple_values():
	"""Create a single datapoint in the contact part of the ideal curve,
	   calculate the theoretical input parameters from the value pair
	   and compare the actual with the theoretical values.   
	"""
	# Setup input parameters.
	startDistance = -10e-9
	stepSize = 0.01e-9

	etot = 1.191e+11
	radius = 25e-9
	kc = 1

	currentLength = 1500
	# Generate a single datapoint in the approach part of the ideal curve.
	parameterSubstitut = kc / (np.sqrt(radius) * etot)
	piezoContact = gen_data.calculate_piezo_value(
		startDistance,
		stepSize,
		currentLength
	)
	deflectionContact = gen_data.calculate_deflection_contact_part(
		parameterSubstitut,
		piezoContact
	)
	datapoint = [piezoContact, deflectionContact]
	# Calculate the theoretical parameters using the generated data point.
	pseudoForce = analyse_data.calculate_adjusted_pseudo_force(datapoint)
	deformation = analyse_data.calculate_deformation(datapoint)

	theoreticalKc = analyse_data.calculate_kc_contact(
		pseudoForce,
		deformation,
		etot,
		radius
	)
	theoreticalRadius = analyse_data.calculate_radius_contact(
		pseudoForce,
		deformation,
		etot,
		kc
	)
	theoreticalEtot = analyse_data.calculate_etot_contact(
		pseudoForce,
		deformation,
		radius,
		kc
	)
	# Check if the parameter values coincide with the calculated theoretical values.
	kcIsClose = np.isclose(kc, theoreticalKc, rtol=1e-2)
	radiusIsClose = np.isclose(radius, theoreticalRadius)
	etotIsClose = np.isclose(etot, theoreticalEtot)

	assert np.array([kcIsClose, radiusIsClose, etotIsClose]).all()

def test_contact_part_critical_values():
	"""Create a single datapoint in the contact part of the ideal curve,
	   calculate the theoretical input parameters from the value pair
	   and compare the actual with the theoretical values.   
	"""
	# Setup input parameters.
	startDistance = -10e-9
	stepSize = 0.01e-9

	etot = 3.296566e+9
	radius = 25e-9
	kc = 40

	currentLength = 1002
	# Generate a single datapoint in the approach part of the ideal curve.
	parameterSubstitut = kc / (np.sqrt(radius) * etot)
	piezoContact = gen_data.calculate_piezo_value(
		startDistance,
		stepSize,
		currentLength
	)
	deflectionContact = gen_data.calculate_deflection_contact_part(
		parameterSubstitut,
		piezoContact
	)
	datapoint = [piezoContact, deflectionContact]
	# Calculate the theoretical parameters using the generated data point.
	pseudoForce = analyse_data.calculate_adjusted_pseudo_force(datapoint)
	deformation = analyse_data.calculate_deformation(datapoint)

	theoreticalKc = analyse_data.calculate_kc_contact(
		pseudoForce,
		deformation,
		etot,
		radius
	)
	theoreticalRadius = analyse_data.calculate_radius_contact(
		pseudoForce,
		deformation,
		etot,
		kc
	)
	theoreticalEtot = analyse_data.calculate_etot_contact(
		pseudoForce,
		deformation,
		radius,
		kc
	)
	# Check if the parameter values coincide with the calculated theoretical values.
	kcIsClose = np.isclose(kc, theoreticalKc, rtol=1e-2)
	radiusIsClose = np.isclose(radius, theoreticalRadius)
	etotIsClose = np.isclose(etot, theoreticalEtot)

	assert np.array([kcIsClose, radiusIsClose, etotIsClose]).all()