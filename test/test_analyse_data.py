import pytest
import numpy as np

import syfos.data_handling.analyse_data as analyse_data

def test_get_approach_part_simple_ideal_curve(
	simple_ideal_curve,
	simple_ideal_curve_approach_part
):
	""""""
	piezoApproach, deflectionApproach = analyse_data.get_ideal_approach_part(
		simple_ideal_curve
	)

	np.testing.assert_array_equal(
		[piezoApproach, deflectionApproach],
		simple_ideal_curve_approach_part
	)

def test_get_contact_part_simple_ideal_curve(
	simple_ideal_curve,
	simple_ideal_curve_contact_part
):
	""""""
	piezoContact, deflectionContact = analyse_data.get_ideal_contact_part(
		simple_ideal_curve
	)

	np.testing.assert_array_equal(
		[piezoContact, deflectionContact],
		simple_ideal_curve_contact_part
	)

def test_calculate_true_distance(
	simple_ideal_curve_approach_part
):
	""""""
	trueDistance = analyse_data.calculate_true_distance(
		simple_ideal_curve_approach_part
	)

	expectedTrueDistance = np.array([-6.0, -4.9, -4.2])

	np.testing.assert_array_equal(
		trueDistance,
		expectedTrueDistance
	)

def test_calculate_adjusted_force(
	simple_ideal_curve_approach_part
):
	""""""
	force = analyse_data.calculate_adjusted_force(
		simple_ideal_curve_approach_part,
		2
	)

	expectedForce = np.array([0.0, -0.2, 0.4])

	np.testing.assert_array_equal(
		force,
		expectedForce
	)

def test_calculate_adjusted_pseudo_force(
	simple_ideal_curve_contact_part
):
	""""""
	pseudoForce = analyse_data.calculate_adjusted_pseudo_force(
		simple_ideal_curve_contact_part
	)

	expectedPseudoForce = np.array([0.0, 1.0, 2.5, 4.0])

	np.testing.assert_array_equal(
		pseudoForce,
		expectedPseudoForce
	)

def test_calculate_deformation(
	simple_ideal_curve_contact_part
):
	""""""
	deformation = analyse_data.calculate_deformation(
		simple_ideal_curve_contact_part
	)

	expectedDeformation = np.array([0.0, 0.0, -0.5, -1.0])

	np.testing.assert_array_equal(
		deformation,
		expectedDeformation
	)

def test_calculate_kc_approach(
	trueDistance,
	forceApproach,
	hamaker,
	radius
):
	""""""
	kc = analyse_data.calculate_kc_approach(
		trueDistance,
		forceApproach,
		hamaker,
		radius
	)

	expectedKc = 0

	assert np.isclose(kc, expectedKc)

def test_calculate_radius_approach(
	trueDistance,
	forceApproach,
	hamaker,
	kc
):
	""""""
	radius = analyse_data.calculate_radius_approach(
		trueDistance,
		forceApproach,
		hamaker,
		kc
	)

	expectedRadius = 0

	assert np.isclose(radius, expectedRadius)

def test_calculate_hamaker_approach(
	trueDistance,
	forceApproach,
	radius,
	kc
):
	""""""
	hamaker = analyse_data.calculate_hamaker_approach(
		trueDistance,
		forceApproach,
		radius,
		kc
	)

	expectedHamaker = 0

	assert np.isclose(hamaker, expectedHamaker)

def test_calculate_kc_contact(
	forceContact,
	deformation,
	etot,
	radius
):
	""""""
	kc = analyse_data.calculate_kc_contact(
		forceContact,
		deformation,
		etot,
		radius
	)

	expectedKc = 17474895.76

	assert np.isclose(kc, expectedKc)

def test_calculate_radius_contact(
	forceContact,
	deformation,
	etot,
	kc
):
	""""""
	radius = analyse_data.calculate_radius_contact(
		forceContact,
		deformation,
		etot,
		kc
	)

	expectedRadius = 4.44e-23

	assert np.isclose(radius, expectedRadius)

def test_calculate_etot_contact(
	forceContact,
	deformation,
	radius,
	kc
):
	""""""
	etot = analyse_data.calculate_etot_contact(
		forceContact,
		deformation,
		radius,
		kc
	)

	expectedEtot = 3200

	assert np.isclose(etot, expectedEtot)

def test_wrapper_calculate_parameter():
	""""""
	pass