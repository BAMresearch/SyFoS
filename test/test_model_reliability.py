import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

def get_parameters_for_synthetic_force_volume():
	""""""
	ParameterMaterial, ParameterMeasurement, ParameterForceVolume = gen_data.get_parameter_tuples()

	hamaker = gen_data.calculate_hamaker(
		hamkerProbe=0,
		hamakerSample=0
	)
	jtc = gen_data.calculate_jtc(
		hamaker,
		radius=0,
		kc=0
	)
	etot = gen_data.calculate_etot(
		poissonRatioProbe=0,
		eProbe=0,
		poissonRatioSample=0,
		eSample=0
	)

	parameterMaterial = ParameterMaterial(
		kc=0,
		radius=0,
		Hamaker=hamaker,
		Etot=etot,
		jtc=jtc,
	)
	parameterMeasurement = ParameterMeasurement(
		initialDistance=0,
		distanceInterval=0,
		maximumdeflection=0,	
	)
	parameterForceVolume = ParameterForceVolume(
		numberOfCurves=4,
		noise=0,
		virtualDeflection=0,
		topography=0
	)

	return parameterMaterial, parameterMeasurement, parameterForceVolume

def create_synthetic_test_force_volume():
	""""""
	parameterMaterial, parameterMeasurement, parameterForcevolume = get_parameters_for_synthetic_force_volume()

	syntheticForcevolume = gen_data.create_synthetic_force_volume(
		parameterMaterial, 
		parameterMeasurement, 
		parameterForcevolume
	)

	return syntheticForcevolume

def compare_input_parameters_and_calculated_parameters():
	""""""
	syntheticForcevolume = create_synthetic_test_force_volume()

	approachParameters, contactParameters = analyse_data.extraxt_parameters(syntheticForcevolume)

	test_compare_approach_hamaker()
	test_compare_approach_etot()
	test_compare_approach_jtc()

	test_compare_contact_hamaker()
	test_compare_contact_etot()
	test_compare_contact_jtc()

def test_compare_approach_hamaker(
	syntheticApproachHamaker: float,
	hamaker: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachHamaker,
		hamaker
	)

def test_compare_approach_etot(
	syntheticApproachEtot: float,
	etot: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachEtot,
		etot
	)

def test_compare_approach_jtc(
	syntheticApproachJtc: float,
	jtc: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachJtc,
		jtc
	)

def test_compare_contact_hamaker(
	syntheticContactHamaker: float,
	hamaker: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachHamaker,
		hamaker
	)

def test_compare_contacth_etot(
	syntheticContactEtot: float,
	etot: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachEtot,
		etot
	)

def test_compare_contact_jtc(
	syntheticContactJtc: float,
	jtc: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachJtc,
		jtc
	)