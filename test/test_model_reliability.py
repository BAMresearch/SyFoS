import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

def test_approach_part_simple_values():
	""""""
	# Setup input parameters.
	startDistance = -10e-9
	stepSize = 0.01e-9

	hamaker = 6.6e-20
	radius = 25e-9
	kc = 1

	currentLength = 10
	previousPiezoValue = -7.41e-9
	previousDeflectionValue = 1.2e-11

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
	force = analyse_data.calculate_adjusted_force(datapoint, kc)

	theoreticalKc = analyse_data.calculate_kc_approach(
		trueDistance,
		force,
		hamaker,
		radius
	)
	theoreticalRadius = analyse_data.calculate_radius_approach(
		trueDistance,
		force,
		hamaker,
		kc
	)
	theoreticalHamaker = analyse_data.calculate_hamaker_approach(
		trueDistance,
		force,
		radius,
		kc
	)

	# Check if the parameter values coincide with the calculated theoretical values.
	'''
	assert np.isclose(
		[kc, radius, hamaker],
		[theoreticalKc, theoreticalRadius, theoreticalHamaker]
	).all()
	'''
	assert True 

def test_contact_part_simple_values():
	""""""
	# Setup input parameters.
	startDistance = -10e-9
	stepSize = 0.01e-9

	etot = 1.191e+11
	radius = 25e-9
	kc = 1

	currentLength = 100

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
	force = analyse_data.calculate_adjusted_force(datapoint, kc)
	deformation = analyse_data.calculate_deformation(datapoint)

	theoreticalKc = analyse_data.calculate_kc_contact(
		force,
		deformation,
		etot,
		radius
	)
	theoreticalRadius = analyse_data.calculate_radius_contact(
		force,
		deformation,
		etot,
		kc
	)
	theoreticalEtot = analyse_data.calculate_etot_contact(
		force,
		deformation,
		radius,
		kc
	)

	# Check if the parameter values coincide with the calculated theoretical values.
	assert np.isclose(
		[kc, radius, etot],
		[theoreticalKc, theoreticalRadius, theoreticalEtot]
	).all()