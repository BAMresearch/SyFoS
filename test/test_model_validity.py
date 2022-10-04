import pytest
import numpy as np

import syfos.data_handling.generate_data as gen_data
import syfos.data_handling.analyse_data as analyse_data

#ToDo: Analyse only the ideal calculate average of real curves as ideal curve?

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

def import_real_force_volume():
	""""""
	realForceVolume = 0

	return realForceVolume

def compare_real_and_synthetic_data():
	""""""
	syntheticForcevolume = create_synthetic_test_force_volume()
	realForcevolume = import_real_force_volume() 

	test_compare_actual_and_synthetic_values(
		syntheticForcevolume,
		realForcevolume
	)
	compare_characteristic_values(
		syntheticForcevolume,
		realForcevolume
	)

def test_compare_actual_and_synthetic_values(
	syntheticForcevolume,
	realForcevolume
):
	""""""


def compare_characteristic_values(
	syntheticForcevolume,
	realForcevolume
):
	""""""
	
	syntheticApproachParameters, syntheticContactParameters = analyse_data.extraxt_parameters(syntheticForcevolume)
	realApproachParameters, realContactParameters = analyse_data.extraxt_parameters(realForcevolume)

	test_compare_approach_hamaker(
		syntheticApproachParameters.hamaker,
		realApproachParameters.hamaker
	)
	test_compare_approach_etot(
		syntheticApproachParameters.etot,
		realApproachParameters.etot
	)
	test_compare_approach_jtc(
		syntheticApproachParameters.jtc,
		realApproachParameters.jtc
	)

	test_compare_contact_hamaker(
		syntheticContactParameters.hamaker,
		realContactParameters.hamaker
	)
	test_compare_contact_etot(
		syntheticContactParameters.etot,
		realContactParameters.etot
	)
	test_compare_contact_jtc(
		syntheticContactParameters.jtc,
		realContactParameters.jtc
	)

def test_compare_approach_hamaker(
	syntheticApproachHamaker: float,
	realApproachHamaker: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachHamaker,
		realApproachHamaker
	)

def test_compare_approach_etot(
	syntheticApproachEtot: float,
	realApproachEtot: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachEtot,
		realApproachEtot
	)

def test_compare_approach_jtc(
	syntheticApproachjtc: float,
	realApproachJtc: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticApproachJtc,
		realApproachJtc
	)

def test_compare_contact_hamaker(
	syntheticContactHamaker: float,
	realContactHamaker: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticContactHamaker,
		realContactHamaker
	)

def test_compare_contact_etot(
	syntheticContactEtot: float,
	realContactEtot: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticContactEtot,
		realContactEtot
	)

def test_compare_contact_jtc(
	syntheticContactjtc: float,
	realContactJtc: float
):
	""""""
	np.testing.assert_almost_equal(
		syntheticContactjtc,
		realContactJtc
	)